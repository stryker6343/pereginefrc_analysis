class AuthError(Exception):
    def __init__(self, response):
        message = f"Authentication Error: {response.text} Code {response.status_code}"
        super().__init__(message)
