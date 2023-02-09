"""
Different custom Exceptions
"""

class Custom404Exception(Exception):
    """Creating a 400 or 404 depending on the situation"""
    def __init__(self, status_code: int, detail: str):
        self.detail = detail
        self.status_code = status_code

    def __str__(self) -> str:
        return self.detail