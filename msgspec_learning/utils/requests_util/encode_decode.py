from __future__ import annotations

from typing import Type, Any, TYPE_CHECKING
import msgspec
from pathlib import Path

from schemas.request_models import ClientResponse


def encode_clientresponse(res: ClientResponse = None) -> dict[str, Any]:
    encode_msg = {
        "url": res.url,
        "revalidated": res.revalidated,
        "ok": res.ok,
        "status_code": res.status_code,
        "reason": res.reason,
        "from_cache": res.from_cache,
        "expires": res.expires,
        "headers": res.headers,
        "content": res.content,
        "size": res.size,
    }

    msg = msgspec.json.encode(encode_msg)

    return msg


# def decode_clientresponse():
#     _decode = msgspec.json.decode(msg)


if TYPE_CHECKING:
    ...
