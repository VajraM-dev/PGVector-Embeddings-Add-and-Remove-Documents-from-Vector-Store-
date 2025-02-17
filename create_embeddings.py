from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
from source_id_data_mapping import insert_source_ids
from connect_to_vs import vector_store

# # Example usage:
# unique_ids = generate_unique_ids(5)
# print(unique_ids)

# from langchain_pinecone import PineconeVectorStore

# index_name = os.environ["PINECONE_INDEX_NAME"] 
separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ]

class doc_loader:
    def __init__(self, path, metadata: dict = None):
        self.path = path
        self.metadata = metadata

    def identify_file_type(self):
        extension = os.path.splitext(self.path)[1].lower()
        if extension == '.pdf':
            return "pdf"
        elif extension == '.docx':
            return "docx"
        else:
            return None
        

    def load_pdf(self):
        loader = PyMuPDFLoader(self.path)
        data = loader.load()

        return data

    def load_word_file(self):
        loader = Docx2txtLoader(self.path)
        data = loader.load()

        return data
    
    def create_splits(self, data):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                    chunk_overlap=100,
                                                    separators=separators)
        texts = text_splitter.split_documents(data)

        return texts

    def generate_unique_ids(self, n: int):
        """
        Generate n unique UUIDs.
        
        :param n: Number of unique IDs to generate
        :return: List of unique UUIDs as strings
        """
        return [str(uuid.uuid4()) for _ in range(n)]
    
    def create_embeddings(self):
        try:
            file_type = self.identify_file_type()
            if file_type == 'pdf':
                data = self.load_pdf()
            if file_type == 'docx':
                data = self.load_word_file()
            if file_type is None:
                return "Please input a valid file format. Accepted file formats are .pdf and .docx"
        except Exception as e:
            return {"message":"Error parsing and loading the documents.", "error_message": e}
        # print(data)
        
        try:
            if self.metadata is not None:
                for item in data:
                    item.metadata.update(self.metadata)
        except Exception as e:
            print(f"Error adding metadata to docs. Error: {e}")

        # return data
        try:
            splits = self.create_splits(data)
        except Exception as e:
            return {"message":"Error spliting the the documents.", "error_message": e}

        try:
            ids = self.generate_unique_ids(len(splits))
            
            source_id_map = {
                "source": splits[-1].metadata['source'],
                "associated_ids": ids
            }
            print(source_id_map)
            insert_source_ids(source_id_map["source"], source_id_map['associated_ids'])
        except Exception as e:
            return {"message":"Error creating ids and storing to db", "error_message": e}
        
        try:
            for i, item in enumerate(splits):
                item.metadata.update({"id": ids[i]})
        except Exception as e:
            print(f"Error adding ids to metadata in splits. Error: {e}")

        try:
            vector_store.add_documents(splits, ids=[doc.metadata["id"] for doc in splits])
            return {"message":"Document pushed to vectorstore successfully", "error_message": None}
        except Exception as e:
            return {"message":"Error uploading the documents to vectorstore.", "error_message": e}
        
