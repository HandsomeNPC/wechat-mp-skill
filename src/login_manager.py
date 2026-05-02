"""Credential management for the WeChat Official Account skill.

Unlike Bilibili there is no QR flow — WeChat 公众号 authentication is just
(appid, secret). This module lets the user *set* them interactively, verify,
and clear; `fetch_access_token` is exposed for debugging.
"""

from typing import Any, Dict, Optional

from .auth import WeChatAuth
from .utils import dispatch


class LoginManager:
    """Configure and validate 公众号 credentials."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    def set_credentials(
        self,
        appid: Optional[str] = None,
        secret: Optional[str] = None,
        access_token: Optional[str] = None,
        token: Optional[str] = None,
        aes_key: Optional[str] = None,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """Store credentials (optionally persist to ~/.hermes/)."""
        if appid:
            self.auth.appid = appid
        if secret:
            self.auth.secret = secret
        if access_token:
            self.auth.access_token = access_token
        if token:
            self.auth.token = token
        if aes_key:
            self.auth.aes_key = aes_key
        # Invalidate cached client so the new creds take effect
        self.auth._client = None
        self.auth.persist = bool(persist)
        if persist and self.auth.is_authenticated:
            self.auth.save_to_file()
        return {
            "success": True,
            "appid": self.auth.appid,
            "has_secret": bool(self.auth.secret),
            "has_access_token": bool(self.auth.access_token),
            "has_callback_token": bool(self.auth.token),
            "has_aes_key": bool(self.auth.aes_key),
            "persisted": bool(persist),
            "file": self.auth._credential_path,
        }

    def verify(self) -> Dict[str, Any]:
        return self.auth.verify()

    def refresh(self) -> Dict[str, Any]:
        """Force-refresh access_token."""
        return self.auth.refresh_token()

    def logout(self) -> Dict[str, Any]:
        """Clear all credentials (memory + disk)."""
        self.auth.clear()
        return {"success": True, "message": "credentials cleared"}

    def show(self) -> Dict[str, Any]:
        """Show masked credential state (does NOT return secrets)."""
        def mask(v: Optional[str]) -> Optional[str]:
            if not v:
                return None
            if len(v) <= 6:
                return "***"
            return v[:4] + "***" + v[-2:]
        return {
            "success": True,
            "appid": self.auth.appid,
            "secret_masked": mask(self.auth.secret),
            "access_token_masked": mask(self.auth.access_token),
            "callback_token_set": bool(self.auth.token),
            "aes_key_set": bool(self.auth.aes_key),
            "persist": self.auth.persist,
            "credential_file": self.auth._credential_path,
        }
