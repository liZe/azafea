from typing import Any, Optional, Text


class Bytes:
    @classmethod
    def new(cls, data: bytes) -> Bytes: ...

    def get_data(self) -> bytes: ...


class Variant:
    @classmethod
    def new_from_bytes(cls, type: VariantType, bytes: Bytes, trusted: bool) -> Variant: ...

    def __new__(cls, format_string: str, value: Any) -> 'Variant': ...

    def get_boolean(self) -> bool: ...
    def get_byte(self) -> int: ...
    def get_child_value(self, index_: int) -> Variant: ...
    def get_data_as_bytes(self) -> Bytes: ...
    def get_double(self) -> float: ...
    def get_int32(self) -> int: ...
    def get_int64(self) -> int: ...
    def get_maybe(self) -> Optional[Variant]: ...
    def get_string(self) -> str: ...
    def get_type_string(self) -> str: ...
    def get_uint16(self) -> int: ...
    def get_uint32(self) -> int: ...
    def get_variant(self) -> Variant: ...
    def is_normal_form(self) -> bool: ...
    def n_children(self) -> int: ...


class VariantType:
    def __init__(self, type_string: Text) -> None: ...
