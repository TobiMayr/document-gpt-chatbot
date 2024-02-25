from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.schemas import FilePathSchema
from app.services import generate_query_vector, generate_and_store_embeddings, get_most_relevant_file_paths, \
    get_file_texts, ask_gpt_with_context
from app.dependencies import get_db
from app.models import Base, engine
from app.config import origins
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process-file-paths/")
async def create_embeddings_from_paths(file_paths: FilePathSchema, background_tasks: BackgroundTasks,
                                       db: Session = Depends(get_db)):
    for path in file_paths.filePaths:
        background_tasks.add_task(generate_and_store_embeddings, path, db)
    return {"processed_files": file_paths}


@app.post("/message")
async def chat(message: dict, db: Session = Depends(get_db)):
    user_message = message['message']

    query_vector = await generate_query_vector(user_message)

    file_paths = await get_most_relevant_file_paths(query_vector, db)

    file_data = await get_file_texts(file_paths)

    response = await ask_gpt_with_context(user_message, file_data)

    return {"reply": response, "filePaths": file_paths}
