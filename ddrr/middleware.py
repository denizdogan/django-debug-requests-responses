from ddrr.loggers import request_logger
from ddrr.loggers import response_logger


class DebugRequestsResponses:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_logger.debug(request)
        response = self.get_response(request)
        response_logger.debug(response)
        return response
