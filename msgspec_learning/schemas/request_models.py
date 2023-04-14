from __future__ import annotations

from typing import (
    Union,
    Optional,
    Iterable,
    Set,
    TYPE_CHECKING,
    Any,
    OrderedDict,
    Annotated,
)
from pathlib import Path
from datetime import datetime, timedelta

from schemas.base import BaseStruct

import uuid
import json

import msgspec

if TYPE_CHECKING:
    ...

import requests
import requests_cache

from requests_cache import CachedSession, SQLiteCache


class ClientCacheBackend(BaseStruct):
    __schema_name__ = "ClientCacheBackend"

    cache_name: str = "default_cache"
    cache_dir: str = ".cache"
    backend: str = "sqlite"

    @property
    def cache_path(self) -> str:
        if self.cache_dir:
            cache_path = f"{self.cache_dir}/{self.cache_name}"

            return cache_path

    @property
    def cache(self) -> Union[SQLiteCache, None]:
        if self.backend == "sqlite":
            _cache = SQLiteCache(self.cache_path)
        else:
            raise ValueError(f"Unrecognized backend type: {self.backend}")
        return _cache


class ClientCacheSettings(BaseStruct):
    __schema_name__ = "ClientCacheSettings"

    cache_name: str = "default_cache"
    cache_dir: str = ".cache"
    backend: str = "sqlite"
    expire_after: int = 900
    url: str = None
    use_cache: bool = True


class ClientResponse(BaseStruct):
    __schema_name__ = "ClientResponse"

    original_res: Union[
        requests.Response,
        requests_cache.CachedResponse,
        requests_cache.OriginalResponse,
    ] = None
    status_code: int = None
    # content: bytes = None
    content: Union[bytes, str, dict[str, Any]] = None
    next: Union[requests_cache.CachedRequest, requests.Request] = None
    created_at: Union[datetime, timedelta] = None
    elapsed: Union[datetime, timedelta] = None
    encoding: Union[bytes, str] = None
    expires: Union[datetime, timedelta] = None
    headers: Union[dict, OrderedDict] = None
    history: list = None
    reason: str = None
    request: Union[
        requests_cache.Request, requests_cache.CachedRequest, requests.PreparedRequest
    ] = None
    url: str = None
    from_cache: bool = None
    ok: bool = None
    revalidated: bool = None
    size: int = None

    @property
    def _json(self) -> list[dict]:
        return_json = self.original_res.json()

        return return_json

    class Config:
        arbitrary_types_allowed = True


class RequestClient(BaseStruct):
    __schema_name__ = "RequestClient"

    url: str = None
    use_cache: bool = None
    cache_name: str = "default_cache"
    cache_dir: str = ".cache"
    backend: str = "sqlite"
    expire_after: int = 900

    @property
    def session(self) -> CachedSession:
        _backend = ClientCacheBackend(
            cache_name=self.cache_name,
            cache_dir=self.cache_dir,
            backend=self.backend,
        )

        _session = CachedSession(backend=_backend.cache, expire_after=self.expire_after)

        return _session

    def build_response_object(
        self,
        res: Union[
            requests_cache.CachedResponse,
            requests_cache.Request,
            requests_cache.OriginalResponse,
        ],
    ) -> ClientResponse:
        if self.use_cache == True:
            _created_at = res.created_at
            _expires = res.expires
            _from_cache = res.from_cache
        else:
            _created_at = None
            _expires = None
            _from_cache = False

        ## Headers is a special Requests dict type.
        #  Convert to regular Python dict by accessing
        #  response dict's dunder method & key "_store"
        _headers = res.headers.__dict__["_store"]

        if res.content:
            ## If there is content, decode from bytes & load into JSON/dict
            _content = json.loads(res.content.decode("utf-8"))
        else:
            _content = None

        _res = ClientResponse(
            # original_res=res,
            url=res.url,
            status_code=res.status_code,
            content=_content,
            next=res.next,
            created_at=_created_at,
            elapsed=res.elapsed,
            encoding=res.encoding,
            expires=_expires,
            headers=_headers,
            history=res.history,
            request=res.request,
            from_cache=_from_cache,
            ok=res.ok,
        )

        return _res

    def get(self) -> ClientResponse:
        try:
            res = self.session.get(self.url)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception making GET request. Exception details:\n{exc}"
            )
        finally:
            self.session.close()

        return_obj = self.build_response_object(res=res)

        return return_obj

    def post(self, data: Union[dict, None]) -> ClientResponse:
        try:
            res = self.session.post(url=self.url, data=data)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception making POST request. Exception details:\n{exc}"
            )
        finally:
            self.session.close()

        return_obj = self.build_response_object(res=res)

        return return_obj


class RequestClientSession(BaseStruct):
    url: str = None
    use_cache: bool = True
    expire_after: Union[int, datetime, timedelta] = timedelta(days=3)
    stale_if_error: bool = True
    cache_dir: str = ".cache"
    cache_name: str = "default_cache"
    backend_type: Annotated[
        str, msgspec.Meta(min_length=1, pattern="sqlite|redis")
    ] = "sqlite"
    backend_timeout: int = 30
    res: Any = None

    @property
    def cache_path(self) -> str:
        """Build path property from cache_dir and cache_name."""

        cache_path = f"{self.cache_dir}/{self.cache_name}"
        # print(
        #     f"[DEBUG] [classes] [RequestClientSession.backend] Cache path: {cache_path}"
        # )

        return cache_path

    @property
    def backend(self) -> Union[SQLiteCache, None]:
        """Build a requests_cache backend."""

        if self.backend_type == "sqlite":
            # print(
            #     f"[DEBUG] [classes] [RequestClientSession.backend] SQLite database detected"
            # )
            # print(
            #     f"[DEBUG] [classes] [RequestClientSession.backend] Creating cache at {self.cache_dir}"
            # )
            backend = SQLiteCache(db_path=self.cache_path, timeout=self.backend_timeout)

        return backend

    @property
    def session(self) -> CachedSession:
        """Build a requests_cache.CachedSession object."""
        # print(
        # f"[DEBUG] [get_req_session] Setting cache path to [dir: {self.cache_dir}], [name: {self.cache_name}]"
        # )
        # print(f"[DEBUG] [get_req_session] getting backend of type: {self.backend_type}")
        _backend = self.backend

        # print(f"[DEBUG] [get_req_session] Creating CachedSession instance")
        session = CachedSession(
            self.cache_path,
            expire_after=self.expire_after,
            stale_if_error=self.stale_if_error,
            backend=_backend,
        )

        return session

    @property
    def json(self) -> json:
        """Convert a request's response to JSON."""
        _json = self.res.json()

        return _json

    def set_res(
        self, resp: Union[requests_cache.CachedResponse, requests.Response, None]
    ) -> Union[requests_cache.CachedResponse, requests.Response, None]:
        """Set .res param on class instance."""
        self.res = resp

    def get(self) -> Union[requests_cache.CachedResponse, requests.Response, None]:
        """Make a GET request to class instance's URL."""

        if self.url:
            # print(f"[DEBUG] [make_request] Making GET request to {self.url}")

            try:
                if not self.use_cache:
                    ## use_cache is false, disable cache
                    with self.session.cache_disabled():
                        _response = self.session.get()

                else:
                    ## use_cache is true, use cache for request
                    with self.session as session:
                        _response = session.get(self.url)

            except:
                raise Exception(f"There was an error with the request to {self.url}.")

            ## Set RequestClient's .res object to request _response
            self.set_res(resp=_response)

            print(
                f"Request: [{self.res.reason}: {self.res.status_code}] [From Cache: {self.res.from_cache}] to {self.url}"
            )

            return self.res

        else:
            raise ValueError("URL cannot be null")


if __name__ == "__main__":
    ...
