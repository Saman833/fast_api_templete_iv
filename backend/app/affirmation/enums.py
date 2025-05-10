from enum import Enum


class UserAffirmationStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    BAD_REQUEST = "bad_request"
    SERVER_ERROR = "server_error"
    FAIL = "fail"