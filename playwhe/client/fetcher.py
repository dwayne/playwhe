import requests

from ..common import Settings
from ..errors import BadStatusCodeError, ServiceUnavailableError


def fetch(params, settings=Settings(), post=requests.post):
    try:
        response = post(settings.url, data={ 'year': params.yy, 'month': params.mmm }, timeout=settings.timeout)
    except requests.RequestException:
        raise ServiceUnavailableError
    else:
        if response.status_code == 200:
            return response.text
        else:
            raise BadStatusCodeError(response.status_code)
