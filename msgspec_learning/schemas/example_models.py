from __future__ import annotations

from typing import Union, Optional, Iterable, Set, TYPE_CHECKING
from pathlib import Path
from datetime import datetime, timedelta

import uuid

import msgspec

## Import BaseStruct object.
from base import BaseStruct


class User(BaseStruct):
    """Struct descrbing a User."""

    ## Generate a uuid with default_factory, if no ID passed.
    #  This is a "dynamic" default value. Uses msgspec.field,
    #  which creates a new default value dynamically for each
    #  instance of class.
    id: uuid.UUID = msgspec.field(default_factory=uuid.uuid4)
    name: str = None
    email: Optional[str] = None
    groups: Set[str] = set()
    enabled: bool = False


if __name__ == "__main__":
    alice = User(
        name="Alice",
        email="alice@example.com",
        groups={"Administrators", "Publishers", "ReportingGroup1"},
        enabled=True,
    )

    bob = User(name="Bob", groups={"Sales", "ReportingGroup3", "RestrictUSB"})

    print(f"[DEBUG] Test User: {alice}")
    print(f"[DEBUG] Groups: {alice.groups}")

    print(f"[DEBUG] Test User: {bob}")
    print(f"[DEBUG] Groups: {bob.groups}")

    print(f"[DEBUG] Alice Fields:\n{alice.__struct_fields__}")
    print(f"[DEBUG] Bob Fields:\n{bob.__struct_fields__}")

    print(f"[DEBUG] Alice Dict: {alice.to_dict()}")
    print(f"[DEBUG] Bob Dict: {bob.to_dict()}")
