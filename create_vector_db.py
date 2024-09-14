import os
import pandas as pd
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

DATA_PATH = 'data/MedicalAtlas.pdf'
DB_FAISS_PATH = 'vector_db/db_faiss.json'

def create_vector_db():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"The file {DATA_PATH} does not exist.")

    loader = DirectoryLoader(
        os.path.dirname(DATA_PATH),
        glob='*.pdf',
        loader_cls=PyPDFLoader
    )
    documents = loader.load()

    # Load and process CSV files
    csv_files = ['data/Training.csv', 'data/Testing.csv']
    csv_documents = []
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                text = ' '.join([f"{col}: {row[col]}" for col in df.columns])
                csv_documents.append(Document(page_content=text))
        else:
            print(f"CSV file {csv_file} not found.")

    all_documents = documents + csv_documents

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(all_documents)

    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)
    print(f"Vector database created and saved to {DB_FAISS_PATH}")

if __name__ == "__main__":
    create_vector_db()
