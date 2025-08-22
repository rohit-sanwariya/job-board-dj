from django.core.management.base import BaseCommand
from jobs.models import Job
from jobs.search_service import es_service


class Command(BaseCommand):
    help = 'Reindex all data in Elasticsearch'

    def handle(self, *args, **options):
        self.stdout.write('Reindexing Elasticsearch...')
        es_service.reindex_all(Job)
        self.stdout.write(
            self.style.SUCCESS('Successfully reindexed all jobs')
        )