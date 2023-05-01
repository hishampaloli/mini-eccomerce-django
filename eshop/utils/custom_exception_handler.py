from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(response)
    if response is not None:
        response.data = {
            'status': False,
            'statusCode': response.status_code,
            'ip': context['request'].META.get('REMOTE_ADDR', None),
            'error': response.data.get('detail', 'Unknown Error'),
            'details': response.data
        }
    return Response(response.data, status=response.status_code)