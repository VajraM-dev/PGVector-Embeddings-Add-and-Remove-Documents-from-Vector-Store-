from connect_to_vs import vector_store

# file_path = r"C:\Users\Prathamesh\Downloads\The Pointlessness of IT Projects (2).pdf"
# dl = doc_loader(path=file_path)
# print(dl.create_embeddings())

results = vector_store.similarity_search(
    "what is wrapper syndrome", k=1
)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")