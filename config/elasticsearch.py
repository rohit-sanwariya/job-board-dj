# config/elasticsearch.py
from elasticsearch import Elasticsearch
from django.conf import settings

# Connect to Elasticsearch service
es = Elasticsearch(
    hosts=[settings.ELASTICSEARCH_URL],
    headers={
        "Accept": "application/vnd.elasticsearch+json; compatible-with=9",
        "Content-Type": "application/vnd.elasticsearch+json; compatible-with=9"
    }
)
