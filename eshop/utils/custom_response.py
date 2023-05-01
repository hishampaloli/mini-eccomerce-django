from rest_framework.response import Response

class CustomResponse(Response):
    def __init__(self, statusCode, message=None, details=None, data=None, **kwargs):
        response_data = {
            'status': True,
            'message': message or 'no message',
            'details': details or {},
            'data': data or {},
            'statusCode': statusCode or 500,
            'error': error or {}
            # 'error'
        }
        super().__init__(response_data, **kwargs)

