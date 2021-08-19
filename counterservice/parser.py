import requests
from bs4 import BeautifulSoup
from counterservice.models import URLs
from requests.exceptions import Timeout, ConnectTimeout, ConnectionError
from requests.adapters import HTTPAdapter
from datetime import datetime


def parse(request_id):
    url_model = URLs.objects.get(id=request_id)
    session = requests.Session()
    session.mount(url_model.url, HTTPAdapter(max_retries=3))
    try:
        reqs = requests.get(url_model.url, timeout=5)
        if reqs.status_code != 200:
            url_model.result = {'error': 'Response has {} status code'.format(reqs.status_code), 'timestamp': str(datetime.now())}
            url_model.save()
            return
    except (Timeout, ConnectionError, ConnectTimeout) as e:
        url_model.result = {'error': type(e).__name__, 'timestamp': str(datetime.now())}
        url_model.save()
        return

    soup = BeautifulSoup(reqs.text, features="html.parser")

    dictionary = {}

    for tag in soup.find_all(True):
        if tag.name not in dictionary:
            dictionary[tag.name] = {'count': 1, 'nested': len(tag.findChildren())}
        else:
            dictionary[tag.name]['count'] += 1
            dictionary[tag.name]['nested'] += len(tag.findChildren())

    url_model.result = dictionary
    url_model.save()
