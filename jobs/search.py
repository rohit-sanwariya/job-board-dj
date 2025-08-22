from jobs.search_service import es_service

def search_jobs(query):
    return es_service.search_jobs(query)