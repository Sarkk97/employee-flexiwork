from django.core.files.storage import FileSystemStorage
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = {}
        customized_response['errors'] = []

        for key, value in response.data.items():
            customized_response['errors'].append({key: value})

        response.data = customized_response

    return response


class CustomFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name