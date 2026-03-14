"""
Custom exception handler for DRF
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error format
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response = {
            'success': False,
            'error': {
                'code': exc.__class__.__name__,
                'message': str(exc),
            }
        }
        
        # Add field errors if validation error
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                custom_response['error']['details'] = exc.detail
            elif isinstance(exc.detail, list):
                custom_response['error']['details'] = exc.detail
        
        response.data = custom_response
    
    return response


def success_response(data, message=None, status_code=status.HTTP_200_OK):
    """
    Helper function to return consistent success responses
    """
    response_data = {
        'success': True,
        'data': data,
    }
    
    if message:
        response_data['message'] = message
    
    return Response(response_data, status=status_code)


def paginated_response(queryset, serializer_class, request, message=None):
    """
    Helper function to return paginated responses
    """
    from rest_framework.pagination import PageNumberPagination
    
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        serializer = serializer_class(page, many=True, context={'request': request})
        return paginator.get_paginated_response({
            'success': True,
            'data': serializer.data,
            'message': message,
        })
    
    serializer = serializer_class(queryset, many=True, context={'request': request})
    return success_response(serializer.data, message)