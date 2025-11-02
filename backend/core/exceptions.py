"""
Custom exception classes for the university dashboard project.
Following the common-modules.md specification.
"""


class BaseAPIException(Exception):
    """Base API exception class"""
    default_message = "An error occurred"
    default_code = "error"
    status_code = 400

    def __init__(self, message=None, code=None, status_code=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)


class ValidationError(BaseAPIException):
    """Data validation failed"""
    default_message = "Validation failed"
    default_code = "validation_error"
    status_code = 400


class AuthenticationError(BaseAPIException):
    """Authentication failed"""
    default_message = "Authentication failed"
    default_code = "authentication_error"
    status_code = 401


class PermissionDeniedError(BaseAPIException):
    """Permission denied"""
    default_message = "Permission denied"
    default_code = "permission_denied"
    status_code = 403


class NotFoundError(BaseAPIException):
    """Resource not found"""
    default_message = "Resource not found"
    default_code = "not_found"
    status_code = 404


class FileProcessingError(BaseAPIException):
    """File processing error"""
    default_message = "File processing failed"
    default_code = "file_processing_error"
    status_code = 422
