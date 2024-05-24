from typing import Optional
# from llama_index.core.llms import ChatMessage
import logging
from elasticsearch import Elasticsearch
from llama_index.core import Settings
import numpy as np
import json

logger = logging.getLogger(__name__)


def handle_chat_service(es: Elasticsearch, prompt: str) -> Optional[str]:
    try:
        embeddings = Settings.embed_model._get_text_embeddings(prompt)[0]
        # Create embeddings to a json for testing
        # embeddings = np.array(embeddings)

        # # Convert the array to a list of lists
        # embeddings_list = embeddings.tolist()

        # # Create a JSON object
        # embeddings_json = json.dumps(embeddings_list, indent=2)

        # # Save the JSON object to a file
        # file_path = "embeddings_output.json"
        # with open(file_path, "w") as file:
        #     file.write(embeddings_json)

        # print(f"The embeddings have been saved to {file_path}.")

        search_query = {
            "size": 3,
            "_source": {
                "excludes": ["embeddings", "ImgUrl"]
            },
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": """
                    if (doc['embeddings'].size() == 0) {
                        return 0;
                    }
                    return cosineSimilarity(params.query_vector, 'embeddings') + 1.0;
                    """,
                        "params": {
                            "query_vector": embeddings
                        }
                    }
                }
            },
            "sort": {
                "_score": {
                    "order": "desc"
                }
            }

        }

        response = es.search(
            index='walmart_elastic_items_vector', body=search_query)

        items_data = response['hits']['hits']
        formatted_items_data = "\n".join([
            json.dumps(item['_source'])
            for item in items_data
        ])
        compiled_prompt = "Act custom ai, and answer the " + prompt + \
            " with the data sourced from the store's inventory " + formatted_items_data
        response = Settings.llm.complete(compiled_prompt)

        if hasattr(response, 'text'):
            response_text = response.text.strip()
        else:
            response_text = response.raw['choices'][0].message.content.strip()

        return response_text
    except Exception as e:
        logger.error(f"Error chat text: {e}")
        raise RuntimeError("Failed to chat text") from e
