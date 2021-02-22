from celery.schedules import crontab

from celery import shared_task
from .services import extract_urls


@shared_task(name="initiate_crawler", bind=True)
def initiate_crawler_async(self, **kwargs):

    if kwargs.get('kwargs'):
        kwargs = kwargs.get('kwargs')

    input_url = kwargs.get('input_url')
    id = kwargs.get('id')

    # Call the Url Extractor Service
    if input_url:
        extract_urls(input_url, id)
    else:
        print('No Url Provided -- {}'.format(kwargs))


@shared_task(name="scheduled_job")
def _scheduled_crawler_job(object):
    """
    TODO -- This can be used as a schedule job which 
    will run everysec and check for URL in Warehouse
    Warehouse contains all the URL's that were extracted from the Url entered by User.
    
    Now this Extraction Job will see every URL which have `is_processed` set `False` and 
    apply the Initiate Crawler to it.
    """

    pass
