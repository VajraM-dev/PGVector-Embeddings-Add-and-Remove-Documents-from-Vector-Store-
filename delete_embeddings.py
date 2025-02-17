from source_id_data_mapping import get_ids_by_source, delete_source
from connect_to_vs import vector_store

def delete_document_from_vs(source: str):
    ids = get_ids_by_source(source)
    vector_store.delete(ids=ids)
    delete_source(source)