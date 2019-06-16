class NoResultsFound(Exception):
    """
    API request did not find any results.
    """
    pass


class InvalidValue(ValueError):
    """
    Given value is invalid.
    """
    pass


class StatusCodeError(Exception):
    """
    There was an request that did not return an 200 status code.

    Expects body to be formatted as described in:
    https://developer.spotify.com/documentation/web-api/#response-schema
    """
    def __init__(self, response):
        if response.status_code is 204:
            super().__init__("204 NO CONTENT")

        body = response.json()
        # Spotify authentication Error
        if 'error' and 'error_description' in body:
            super().__init__(f"Error {body['error']}: {body['error_description']}")
        # Regular spotify Error
        if 'status' and 'message' in body:
            super().__init__(f"Status {body['status']}: {body['message']}")