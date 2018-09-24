import requests

from ..error import FetchError


DEFAULT_URL = 'http://nlcb.co.tt/app/index.php/pwresults/playwhemonthsum'
DEFAULT_TIMEOUT = 5


def fetch(yy, mmm, url=DEFAULT_URL, timeout=DEFAULT_TIMEOUT, post=requests.post):
    try:
        resp = post(url, data={ 'year': yy, 'month': mmm }, timeout=timeout)
    except requests.RequestException:
        raise FetchError('POST failed')
    else:
        if resp.status_code == 200:
            return resp.text
        else:
            raise FetchError('Bad status code: %d' % resp.status_code)
