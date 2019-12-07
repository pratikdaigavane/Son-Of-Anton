"""
Middleware to log all requests and responses.
Uses a logger configured by the name of django.request
to log all requests and responses according to configuration
specified for django.request.
"""
# import json
import logging
from django.utils.deprecation import MiddlewareMixin

import socket
import time
import json

request_logger = logging.getLogger('customLog')


class RequestLogMiddleware(MiddlewareMixin):
    """Request Logging Middleware."""

    def __init__(self, *args, **kwargs):
            """Constructor method."""
            super().__init__(*args, **kwargs)

    # def __call__(self, request):
    #     self.process_request()

    def process_request(self, request):
        """Set Request Start Time to measure time taken to service request."""
        if request.method in ['POST', 'PUT', 'PATCH']:
            request.req_body = request.body
        request.start_time = time.time()

    def extract_log_info(self, request, response=None, exception=None):
        """Extract appropriate log info from requests/responses/exceptions."""
        log_data = {
            'remote_address': request.META['REMOTE_ADDR'],
            'hostname': socket.gethostname(),
            'method': request.method,
            'path': request.get_full_path(),
            'response_time': round(((time.time() - request.start_time) * 1000), 3),
        }
        if request.method in ['PUT', 'POST', 'PATCH']:
            log_data['request_data'] = json.loads(
                str(request.req_body, 'utf-8'))
        else:
            log_data['request_data'] = ''
        log_data['response'] = ''
        if response['content-type'] == 'application/json':
            response_body = response.content.decode()
            log_data['response'] = response_body
        log_data['status_code'] = response.status_code
        return json.dumps(log_data)

    def process_response(self, request, response):
        """Log data using logger."""
        if not str(request.get_full_path()).startswith('/static/') and not str(request.get_full_path()).startswith('/admin/'):
            log_data = self.extract_log_info(request=request,
                                             response=response)
            request_logger.info(log_data)
        return response

    def process_exception(self, request, exception):
        """Log Exceptions."""
        try:
            raise exception
        except Exception:
            request_logger.exception(msg="Unhandled Exception")
        return exception
