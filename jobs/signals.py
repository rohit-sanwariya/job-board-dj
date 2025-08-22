from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from jobs.models import Job
from jobs.search_service import es_service

@receiver(post_save, sender=Job)
def index_job_on_save(sender, instance, **kwargs):
    es_service.index_job(instance)

@receiver(post_delete, sender=Job)
def delete_job_from_index(sender, instance, **kwargs):
    try:
        es_service.es.delete(index=es_service.index_name, id=instance.id)
        logger.info(f"Deleted job {instance.id} from index")
    except Exception as e:
        logger.error(f"Failed to delete job {instance.id} from index: {e}")