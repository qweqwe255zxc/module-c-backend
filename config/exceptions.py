from django.http import Http404

from rest_framework.exceptions import ValidationError, NotAuthenticated, AuthenticationFailed, PermissionDenied, \
    NotFound, MethodNotAllowed
from rest_framework.views import exception_handler

from .utils import error


# def handler(exc, ctx):
#     if isinstance(exc, ValidationError):
#         return error('Invalid data', exc.detail, 422)
#     if isinstance(exc, (NotAuthenticated, AuthenticationFailed, PermissionDenied)):
#         return error('Forbidden for you', status=403)
#     if isinstance(exc, (NotFound, Http404)):
#         return error('Not found', status=404)
#     if isinstance(exc, MethodNotAllowed):
#         return error('Method Not Allowed', status=405)
#
#     return exception_handler(exc, ctx)

def handler(exc, ctx):
    response = exception_handler(exc, ctx)
    if response is None: return None
    if isinstance(exc, ValidationError):
        response.status_code = 422
        response.data = {'message': 'Invalid fields', 'errors': response.data}
    else:
        if response.status_code in (401, 403):
            response.status_code = 403
            response.headers.pop('WWW-Authenticate', None)
            response.data = {"message": "Forbidden for you"}

        elif response.status_code == 404:
            response.data = {"message": "Not found"}

        else:
            response.data = {'message': response.data['detail']}

    return response
