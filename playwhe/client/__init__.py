from . import fetcher, parser
from ..common import Params


def fetch(year, month, settings=None, post=None):
    params = Params(year, month)

    kwargs = {}

    if settings is not None:
        kwargs['settings'] = settings

    if post is not None:
        kwargs['post'] = post

    return parser.parse(fetcher.fetch(params, **kwargs), params)
