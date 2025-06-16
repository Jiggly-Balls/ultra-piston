class BasePistonError(Exception):
    """The base exception to all ultra-piston errors."""


class MissingDataError(BasePistonError):
    """Raised when the required data is not set or is missing."""
