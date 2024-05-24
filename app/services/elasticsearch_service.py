from elasticsearch import Elasticsearch
from ..settings import settings

def get_elasticSearch() -> Elasticsearch:
    es = Elasticsearch(
        hosts=[settings.ELASTICSEARCH_HOST],
        http_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)
    )
    return es
