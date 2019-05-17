import logging


class DebugRequestsResponses(object):
    request_log = logging.getLogger("ddrr-request-logger")
    response_log = logging.getLogger("ddrr-response-logger")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request_log.debug(request)
        response = self.get_response(request)
        self.response_log.debug(response)
        return response
