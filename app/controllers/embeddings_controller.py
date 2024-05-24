from app.models.embeddings import EmbeddingsResponse
from llama_index.core import Settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan, parallel_bulk
import logging

def create_embeddings(es: Elasticsearch, index_name: str) -> EmbeddingsResponse:
    try:
        # Initialize logging
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        query = {
            "query": {
                "bool": {
                    "must_not": [
                        {
                            "exists": {
                                "field": "embeddings"
                            }
                        }
                    ]
                }
            }
        }
        batch_size = 1000

        # Generator function to yield actions
        def generate_actions():
            for doc in scan(es, index=index_name, query=query, size=batch_size):
                try:
                    embeddings = Settings.embed_model._get_text_embeddings(doc)[0]
                    action = {
                        "_op_type": "update",
                        "_index": index_name,
                        "_id": doc['_id'],
                        "doc": {"embeddings": embeddings}
                    }
                    logging.debug(f"Prepared update for document ID: {doc['_id']}")
                    yield action
                except Exception as e:
                    logging.error(f"Error processing document ID {doc['_id']}: {str(e)}")

        # Execute updates in parallel, using detailed logging to monitor successes and failures
        results = parallel_bulk(es, generate_actions(), thread_count=4, chunk_size=batch_size, max_chunk_bytes=10485760)
        for success, info in results:
            if not success:
                logging.error(f"Failed to update document {info}")
            else:
                logging.debug(f"Successfully updated document ID: {info['update']['_id']}")

        logging.info("Embedding update process completed successfully.")
        return EmbeddingsResponse(
            status=True,
            message="Embeddings updated successfully",
            data={}
        )
    except Exception as e:
        logging.error(f"An error occurred during the embedding update process: {str(e)}")
        return EmbeddingsResponse(
            status=False,
            message="An error occurred during the embedding update.",
            data={}
        )
