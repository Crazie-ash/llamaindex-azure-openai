import json
from app.models.embeddings import  EmbeddingsResponse
from app.services.elasticsearch_service import get_elasticSearch
from llama_index.core import Settings
# from pinecone import Pinecone, ServerlessSpec


def create_embeddings() -> EmbeddingsResponse:
    response = index_documents_with_embeddings()
    return response
    # return EmbeddingsResponse(
    #     status=True,
    #     message="Indexed successful",
    #     data={"response": "Hello World"}
    # )

def fetch_documents_from_elasticsearch(index_name, size=25):
    es = get_elasticSearch()
    search_query = {
        "size": size,
        "query": {
            "match_all": {}  
        }
    }
    response = es.search(index=index_name, body=search_query)
    documents = []
    for hit in response['hits']['hits']:
        documents.append(hit['_source'])
    return documents

# def index_documents_with_embeddings():
#     try:
#         pc = Pinecone(api_key="028d2203-dbac-47ad-99b1-8853c61ac69d")
#         index_name = "walmart-elastic-items-embeddings"
#         # if index_name not in pc.list_indexes():
#         #     pc.create_index(index_name, dimension=1536)  # Adjust the dimension based on your embedding size
#         pinecone_index = pc.Index(index_name)


#         # Fetch documents from the existing Elasticsearch index
#         documents = fetch_documents_from_elasticsearch('walmart_elastic_items')

#         # Create embeddings for each document's 'Description'
#         document_embeddings = []
#         for doc in documents:
#             embedding = Settings.embed_model._get_text_embeddings(doc['Description'])
#             # print(f"Embedding for document ID {doc['ID']}: {embedding}")

#             # print(isinstance(embedding, list) and all(isinstance(x, float) for x in embedding[0]))
#             document_embeddings.append({
#                 "id": str(doc['ID']),  # Use the document ID as the vector ID in Pinecone
#                 "values": embedding[0],
#                 "metadata": {
#                     "ItemLookupCode": doc['ItemLookupCode'],
#                     "CategoryID": doc['CategoryID'],
#                     "SupplierID": doc['SupplierID'],
#                     "ImgUrl": doc['ImgUrl']
#                 }
#             })

#         # Index embeddings in Pinecone
#         pinecone_index.upsert(vectors=document_embeddings)
        
#         from app.models.embeddings import EmbeddingsResponse
#         return EmbeddingsResponse(
#             status=True,
#             message="Indexed successfully",
#             data={"response": "Hello World"}
#         )
#     except Exception as e:
#         from app.models.embeddings import EmbeddingsResponse
#         return EmbeddingsResponse(
#             status=False,
#             message=str(e),
#             data={}
#         )

def index_documents_with_embeddings():
    try:
        # Fetch documents from the existing Elasticsearch index
        documents = fetch_documents_from_elasticsearch('walmart_elastic_items')

        # Create embeddings for each document
        document_embeddings = []
        for doc in documents:
            # embedding = Settings.embed_model._get_text_embeddings(doc['Description'])
            embedding = Settings.embed_model._get_text_embeddings(doc)
            document_embeddings.append({
                "embedding": embedding[0],
                "metadata": {
                    "ID": doc['ID'],
                    "Description": doc['Description'],
                    "ItemLookupCode": doc['ItemLookupCode'],
                    "CategoryID": doc['CategoryID'],
                    "SupplierID": doc['SupplierID'],
                    "ImgUrl": doc['ImgUrl']
                }
            })

        # Index embeddings in Elasticsearch
        es = get_elasticSearch()
        index_name = 'walmart_elastic_items_embeddings'
        
        # Create the index if it doesn't exist
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name)

        # Index each document with its embedding
        for doc in document_embeddings:
            # es.index(index=index_name, body=doc)
            body = json.dumps(doc)  # Serialize the document to JSON
            body_size = len(body)  # Get the size of the JSON string
            print(f"Document size: {body_size} bytes")  # Print the size of the document
            
            # Log or handle the document size before indexing
            if body_size < 100000000:  # Example size limit: 100MB
                es.index(index=index_name, body=doc)
            else:
                print(f"Document is too large to index: {body_size} bytes")


        print(f"Indexed {len(document_embeddings)} documents in Elasticsearch.")
        from app.models.embeddings import EmbeddingsResponse
        return EmbeddingsResponse(
            status=True,
            message="Indexed successfully",
            data={"response": "Hello World"}
        )
    except Exception as e:
        from app.models.embeddings import EmbeddingsResponse
        return EmbeddingsResponse(
            status=False,
            message=str(e),
            data={}
        )

