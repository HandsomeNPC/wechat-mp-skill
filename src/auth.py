"""Credential container for the WeChat Official Account skill.

This module centralizes credentials for the WeChat 公众号 Open API. All API
calls run through `wechatpy`, so `WeChatAuth` acts as:

- the single source of truth for appid / secret / access_token / token /
  aes_key across the process
- a factory for `wechatpy.WeChatClient` instances (`to_client()`) and
  encrypted-message parsers (`to_crypto()`)
- an optional persistence layer (`~/.hermes/wechat-credentials.json`, 0600)

Credential resolution order (highest priority first):
1. Explicit constructor parameters
2. Explicit `credential_file` (JSON)
3. Persisted `~/.hermes/wechat-credentials.json` (when `persist=True`)
4. Environment variables (`WECHAT_APPID`, `WECHAT_SECRET`,
   `WECHAT_ACCESS_TOKEN`, `WECHAT_TOKEN`, `WECHAT_AES_KEY`)
"""

import json
import os
from typing import Any, Dict, Optional


DEFAULT_CREDENTIAL_FILE = os.path.expanduser(
    os.environ.get("WECHAT_CREDENTIAL_FILE", "~/.hermes/wechat-credentials.json")
)


class WeChatAuth:
    """Credential container + `wechatpy.WeChatClient` factory."""

    def __init__(
        self,
        appid: Optional[str] = None,
        secret: Optional[str] = None,
        access_token: Optional[str] = None,
        token: Optional[str] = None,
        aes_key: Optional[str] = None,
        credential_file: Optional[str] = None,
        persist: Optional[bool] = None,
    ):
        if persist is None:
            persist = os.environ.get("WECHAT_PERSIST", "").lower() in (
                "1", "true", "yes",
            )
        self._persist = persist
        self._credential_path = credential_file or DEFAULT_CREDENTIAL_FILE

        self.appid = appid
        self.secret = secret
        self.access_token = access_token
        self.token = token
        self.aes_key = aes_key

        if credential_file and os.path.exists(credential_file):
            self._load_from_file(credential_file)
        elif self._persist and os.path.exists(DEFAULT_CREDENTIAL_FILE):
            self._load_from_file(DEFAULT_CREDENTIAL_FILE)

        if not self.appid:
            self.appid = os.environ.get("WECHAT_APPID", "") or None
        if not self.secret:
            self.secret = os.environ.get("WECHAT_SECRET", "") or None
        if not self.access_token:
            self.access_token = os.environ.get("WECHAT_ACCESS_TOKEN", "") or None
        if not self.token:
            self.token = os.environ.get("WECHAT_TOKEN", "") or None
        if not self.aes_key:
            self.aes_key = os.environ.get("WECHAT_AES_KEY", "") or None

        if self._persist and self.is_authenticated:
            self.save_to_file(self._credential_path)

        # Lazy-built client cache (invalidated when credentials change)
        self._client = None

    def _load_from_file(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            cred = json.load(f)
        self.appid = cred.get("appid") or self.appid
        self.secret = cred.get("secret") or self.secret
        self.access_token = cred.get("access_token") or self.access_token
        self.token = cred.get("token") or self.token
        self.aes_key = cred.get("aes_key") or self.aes_key

    @property
    def is_authenticated(self) -> bool:
        """True when we have enough to call the API.

        Either a static `access_token` is provided, or both `appid` and
        `secret` are present so wechatpy can fetch one itself.
        """
        if self.access_token:
            return True
        return bool(self.appid and self.secret)

    def to_client(self):
        """Build (or return cached) `wechatpy.WeChatClient`.

        Raises RuntimeError if insufficient credentials are available.
        """
        if not self.is_authenticated:
            raise RuntimeError(
                "WeChat credentials missing. Set appid+secret (or access_token) "
                "via `login set_credentials` or env vars."
            )
        if self._client is not None:
            return self._client
        from wechatpy import WeChatClient

        self._client = WeChatClient(
            appid=self.appid or "",
            secret=self.secret or "",
            access_token=self.access_token,
        )
        return self._client

    def to_crypto(self):
        """Build a `WeChatCrypto` for encrypted callback messages.

        Requires `appid`, `token`, `aes_key`.
        """
        if not (self.appid and self.token and self.aes_key):
            raise RuntimeError(
                "Encrypted callback needs appid + token + aes_key in credentials"
            )
        from wechatpy.crypto import WeChatCrypto

        return WeChatCrypto(self.token, self.aes_key, self.appid)

    def clear(self) -> None:
        """Drop all credentials in-memory and on-disk if persisted."""
        self.appid = None
        self.secret = None
        self.access_token = None
        self.token = None
        self.aes_key = None
        self._client = None
        if self._persist:
            self.clear_persisted()

    def refresh_token(self) -> Dict[str, Any]:
        """Force-fetch a new access_token via `wechatpy`."""
        if not (self.appid and self.secret):
            return {"success": False, "message": "appid+secret required"}
        try:
            client = self.to_client()
            data = client.fetch_access_token()
        except Exception as e:  # noqa: BLE001
            return {"success": False, "message": f"fetch_access_token failed: {e}"}
        self.access_token = data.get("access_token") or self.access_token
        if self._persist:
            self.save_to_file(self._credential_path)
        return {
            "success": True,
            "access_token": data.get("access_token"),
            "expires_in": data.get("expires_in"),
        }

    def verify(self) -> Dict[str, Any]:
        """Confirm credentials are valid by fetching (or reading) a token."""
        if not self.is_authenticated:
            return {"success": False, "message": "No credentials provided"}
        try:
            client = self.to_client()
            tok = client.access_token  # property — auto-fetches when missing
        except Exception as e:  # noqa: BLE001
            return {"success": False, "message": f"verify failed: {e}"}
        return {
            "success": bool(tok),
            "appid": self.appid,
            "access_token_masked": (tok[:8] + "..." if tok else None),
        }

    @property
    def persist(self) -> bool:
        return self._persist

    @persist.setter
    def persist(self, value: bool) -> None:
        self._persist = value
        if value and self.is_authenticated:
            self.save_to_file(self._credential_path)
        elif not value and os.path.exists(self._credential_path):
            os.remove(self._credential_path)

    def clear_persisted(self) -> None:
        if os.path.exists(self._credential_path):
            os.remove(self._credential_path)

    def save_to_file(self, filepath: Optional[str] = None) -> None:
        """Save credentials to disk with 0600 permissions."""
        filepath = filepath or self._credential_path
        cred = {
            "appid": self.appid,
            "secret": self.secret,
            "access_token": self.access_token,
            "token": self.token,
            "aes_key": self.aes_key,
        }
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        fd = os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        f = None
        try:
            f = os.fdopen(fd, "w", encoding="utf-8")
            json.dump(cred, f, indent=2, ensure_ascii=False)
        except Exception:
            if f is None:
                os.close(fd)
            raise
        finally:
            if f is not None:
                f.close()
