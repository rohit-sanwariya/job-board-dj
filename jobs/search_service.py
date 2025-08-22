# jobs/search_service.py
from elasticsearch import Elasticsearch
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)


class ElasticsearchService:
    def __init__(self):
        # Use the ELASTICSEARCH_URL from your Django settings
        self.es = Elasticsearch(settings.ELASTICSEARCH_URL)
        self.index_name = "jobs"
        self.setup_index()

    def setup_index(self):
        """Create index with proper mapping if it doesn't exist"""
        if not self.es.indices.exists(index=self.index_name):
            try:
                self.es.indices.create(
                    index=self.index_name,
                    body={
                        "mappings": {
                            "properties": {
                                "title": {"type": "text"},
                                "description": {"type": "text"},
                                "company": {"type": "text"},
                                "location": {"type": "text"},
                                "employment_type": {"type": "keyword"},
                                "salary_min": {"type": "integer"},
                                "salary_max": {"type": "integer"},
                                "skills": {"type": "keyword"},
                                "posted_at": {"type": "date"},  # Changed from created_at to posted_at
                                # Add other fields as needed
                            }
                        }
                    }
                )
                logger.info(f"Created Elasticsearch index: {self.index_name}")
            except Exception as e:
                logger.error(f"Failed to create index: {e}")

    def index_job(self, job_instance):
        """Index a single job"""
        try:
            doc = {
                "title": job_instance.title,
                "description": job_instance.description,
                "company": job_instance.company.name if hasattr(job_instance, 'company') else "",
                "location": job_instance.location,
                "employment_type": job_instance.employment_type,
                "salary_min": job_instance.salary_min,
                "salary_max": job_instance.salary_max,
                "skills": [skill.name for skill in job_instance.skills.all()] if hasattr(job_instance,
                                                                                         'skills') else [],
                "posted_at": job_instance.posted_at.isoformat() if job_instance.posted_at else None,
                # Changed from created_at to posted_at
                # Add other fields as needed
            }

            # Remove None values
            doc = {k: v for k, v in doc.items() if v is not None}

            self.es.index(
                index=self.index_name,
                id=job_instance.id,
                document=doc
            )
            logger.info(f"Indexed job {job_instance.id}")
        except Exception as e:
            logger.error(f"Failed to index job {job_instance.id}: {e}")

    def search_jobs(self, query):
        """Search jobs with error handling"""
        try:
            result = self.es.search(
                index=self.index_name,
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["title^3", "description^2", "company", "location", "skills"]
                        }
                    }
                }
            )
            return result["hits"]["hits"]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def reindex_all(self, model):
        """Reindex all instances of a model"""
        count = 0
        for instance in model.objects.all():
            self.index_job(instance)
            count += 1
        logger.info(f"Reindexed {count} {model.__name__} instances")


# Singleton instance
es_service = ElasticsearchService()