from datetime import datetime
from warnings import warn
from functools import partial
from typing import Annotated, TypeAlias
from pydantic import AfterValidator, BaseModel, Field, EmailStr, StringConstraints
from .pretty_errors import CustomErrorMsg, merge_override, merge_override_prev
import string
from pydantic import SecretStr

SHORT_STR_MAX_LENGTH = 30
PASSWORD_MIN_LENGTH = 8
DISPLAY_NAME_MIN_LENGTH = 3

ShortStr: TypeAlias = Annotated[
    str,
    Field(max_length=SHORT_STR_MAX_LENGTH),
    CustomErrorMsg(
        f"Слишком много символов (должно быть не больше {SHORT_STR_MAX_LENGTH})"
    ),
]
Login: TypeAlias = Annotated[
    ShortStr,
    StringConstraints(strip_whitespace=True, pattern="[a-zA-Z0-9_]+"),
    CustomErrorMsg(
        "Логин может содержать только латинские символы, цифры и нижнее подчеркивание"
    ),
]

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
        ), f"Пароль должен содержать один из следующих символов: {special_chars}"
    if includes_numbers:
        assert len(password_char_set & digits) > 0, "Пароль должен содержать цифру"
    if includes_lowercase:
        assert (
            not password_str.isupper()
        ), "Пароль должен содержать как минимум одну прописную букву"
    if includes_uppercase:
        assert (
            not password_str.islower()
        ), "Пароль должен содержать как минимум одну заглавную букву"

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
    SecretStr,
    Field(min_length=PASSWORD_MIN_LENGTH),
    CustomErrorMsg(
        f"Пароль должен состоять из не менее {PASSWORD_MIN_LENGTH} символов",
        merge_strategy=merge_override_prev,
    ),
    get_password_validator(),
]


class UserCreate(BaseModel):
    login: Login
    password: Password
    email: Annotated[
        EmailStr, CustomErrorMsg("Некорректный email", merge_strategy=merge_override)
    ]
    display_name: Annotated[
        str, Field(min_length=DISPLAY_NAME_MIN_LENGTH), CustomErrorMsg("")
    ]
    # display_name: Annotated[
    #     Field(min_length=3),
    #     CustomErrorMsg("Отображаемое имя должно быть не менее"),
    #     ShortStr,
    # ]
