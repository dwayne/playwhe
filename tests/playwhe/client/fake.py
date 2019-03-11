import os


def response(params):
    path = os.path.join(os.path.dirname(__file__), 'fixtures/responses/%s_%s.html' % (params.yy, params.mmm))

    with open(path) as f:
        return f.read()
