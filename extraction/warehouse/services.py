from bs4 import BeautifulSoup
import urllib.request
from .models import CrawledUrls, UserRequest
from celery import group
# 

parser = 'lxml'

def extract_urls(input_url, id=None, ):

    try:
        print('Extracting from Url - {} '.format(
            input_url
        ))
        resp = urllib.request.urlopen(input_url)
    except Exception as e:
        print('Exception Occurred while processing Url - {} -->{}'.format(
            input_url, e
        ))
        return None
    
    # Extract URL's Using Beautiful Soup,
    # We can also use Scrapy for this, But time limitations !! =)
    soup = BeautifulSoup(
        resp, parser, from_encoding=resp.info().get_param('charset'))
    
    _links = [link['href'] for link in soup.find_all('a', href=True)]


    # Filter Valid URLS - with proper Scheme and NetLoc from URLParse Lib
    _links = list(filter(validate_url, _links))

    if _links:
        _commit_to_db(_links, id)

        from .tasks import initiate_crawler_async

        # Reapply the same Process to All Url's
        job = group(initiate_crawler_async.si(
            kwargs={'input_url': link, 'id': id}).set(
            queue="initiate_crawler") for link in _links
        )      
        job.apply_async()

    else:
        print('No Urls found in URL - {}'.format(input_url))


def validate_url(url):
    from urllib.parse import urlparse
    _check_url =  urlparse(url)

    if _check_url.scheme and _check_url.netloc:
        return True
    else:
        return False

def _commit_to_db(_links, id):
    if id:
        id = UserRequest.objects.get(id=id)

    objs = [
        CrawledUrls(
            url=input_url,
            user_request=id
        )
        for input_url in _links
    ]

    print('Writing URL\'s to Database')
    CrawledUrls.objects.bulk_create(objs)

