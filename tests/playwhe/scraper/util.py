import os


def mock_response(yy, mmm):
    path = os.path.join(os.path.dirname(__file__), 'fixtures/responses/%s_%s.html' % (yy, mmm))

    with open(path) as f:
        return f.read()
