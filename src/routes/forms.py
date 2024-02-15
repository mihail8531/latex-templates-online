from typing import Annotated

from fastapi import Form


class PasswordRequestForm:
    """
    This is a dependency class to collect the `username` and `password` as form data
    for an OAuth2 password flow.

    The OAuth2 specification dictates that for a password flow the data should be
    collected using form data (instead of JSON) and that it should have the specific
    fields `username` and `password`.

    All the initialization parameters are extracted from the request.
    """

    def __init__(
        self,
        *,
        username: Annotated[
            str,
            Form(),
        ],
        password: Annotated[
            str,
            Form(),
        ],
    ):
        self.username = username
        self.password = password
