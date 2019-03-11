class PlayWheError(Exception):
    pass


class FetchError(PlayWheError):
    pass


class BadStatusCodeError(FetchError):
    def __init__(self, status_code):
        super().__init__(str(status_code))
        self.status_code = status_code


class ServiceUnavailableError(FetchError):
    pass
