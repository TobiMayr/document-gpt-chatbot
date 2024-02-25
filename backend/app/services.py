from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from typing import List

from app.config import USER_NAME
from app.models import FileVector
from app.extractors import extract_text

client = OpenAI()


async def generate_and_store_embeddings(file_path: str, db: Session):

    text = extract_text(file_path)

    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding

    try:
        file_vector = db.query(FileVector).filter(FileVector.file_path == file_path).one()
        file_vector.embedding = embedding
    except NoResultFound:
        file_vector = FileVector(embedding=embedding, file_path=file_path)
        db.add(file_vector)

    db.commit()


async def generate_query_vector(user_message: str):
    response = client.embeddings.create(
        input=user_message,
        model="text-embedding-ada-002"
    )
    query_vector = response.data[0].embedding
    return query_vector


async def get_file_texts(file_paths: List[str]):
    file_data = []
    for path in file_paths:
        text = extract_text(path)
        file_data.append({'path': path, 'text': text})
    return file_data


async def get_most_relevant_file_paths(query_vector, db: Session):
    stmt = (
        select(
            FileVector.file_path
        )
        .order_by(
            FileVector.embedding.max_inner_product(query_vector)
        )
        .limit(2)
    )
    results = db.execute(stmt).fetchall()
    file_paths = [row[0] for row in results]

    return file_paths

_PROMPT = """
You are looking at files from a specific user called {user_name}. These files can range from documents such as 
certificates, contracts to bank statements and personal text files that capture the life of friends and family.
Based on the users question, analise the following documents to answer that question. The file path could hint at
what content the file is containing.
{combined_text}
Based on these documents, how would you answer the user's question?
User's question: {user_message}
"""

async def ask_gpt_with_context(user_message: str, file_data: List[dict]):
    combined_text = "\n".join(f"File Path: {data['path']}\n File Content START:\n{data['text']}\n File Content END" for data in file_data)

    prompt = (_PROMPT.format(user_name=USER_NAME, combined_text=combined_text, user_message=user_message))



    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    response = chat_completion.choices[0].message.content
    return response
