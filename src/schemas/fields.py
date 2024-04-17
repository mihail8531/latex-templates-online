from __future__ import annotations
from functools import partial
from typing import TYPE_CHECKING, Annotated, TypeAlias
from pydantic import BaseModel, Field, AfterValidator, constr
import string


ShortStr: TypeAlias = Annotated[str, Field(max_length=30)]
Login: TypeAlias = Annotated[
    ShortStr, AfterValidator(lambda s: s.isascii() and s.isidentifier())
]
from pydantic import SecretStr

digits = set(string.digits)


def _validate_password(
    password: SecretStr,
    special_chars: str = "$@#%!^&*()-_+={}[]",
    includes_special_chars: bool = False,
    includes_numbers: bool = False,
    includes_lowercase: bool = False,
    includes_uppercase: bool = False,
) -> SecretStr:
    password_str = password.get_secret_value()
    password_char_set = set(password_str)
    special_char_set = set(special_chars)
    if includes_special_chars:
        assert (
            len(password_char_set & special_char_set) > 0
        ), f"Must contain one of the following special characters: {special_chars}"
    if includes_numbers:
        assert len(password_char_set & digits) > 0, "Must contain at least one digit"
    if includes_lowercase:
        assert password_str.islower(), "Must contain at least one lowercase letter"
    if includes_uppercase:
        assert password_str.isupper(), "Must contain at least one uppercase letter"

    return password


def get_password_validator(
    special_chars: str = "$@#%!^&*()-_+={}[]",
    includes_special_chars: bool = False,
    includes_numbers: bool = False,
    includes_lowercase: bool = False,
    includes_uppercase: bool = False,
) -> AfterValidator:
    return AfterValidator(
        partial(
            _validate_password,
            special_chars=special_chars,
            includes_special_chars=includes_special_chars,
            includes_numbers=includes_numbers,
            includes_lowercase=includes_lowercase,
            includes_uppercase=includes_uppercase,
        )
    )


Password: TypeAlias = Annotated[
    SecretStr, Field(min_length=8), get_password_validator()
]

