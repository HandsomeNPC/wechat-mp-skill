"""Customer-service (多客服) account & session management.

Wraps `client.customservice` — separate from `MessageOps.send_*` which is the
"send a single 客服消息" path. This module covers ACCOUNT MANAGEMENT and
SESSION CONTROL: add/list/delete kf accounts, transfer chats, fetch records.
"""

from typing import Any, Dict, Optional

from .auth import WeChatAuth
from .utils import dispatch, open_file


class CustomServiceOps:
    """Wraps `client.customservice`."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    # ---------- accounts ----------

    def add_account(
        self, account: str, nickname: str, password: str
    ) -> Dict[str, Any]:
        """`account` format: `prefix@gh_name`."""
        client = self.auth.to_client()
        data = client.customservice.add_account(account, nickname, password)
        return {"success": True, "data": data}

    def update_account(
        self, account: str, nickname: str, password: str
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.customservice.update_account(account, nickname, password)
        return {"success": True, "data": data}

    def delete_account(self, account: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.customservice.delete_account(account)
        return {"success": True, "data": data}

    def list_accounts(self) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.customservice.get_accounts()
        return {"success": True, "data": data}

    def list_online(self) -> Dict[str, Any]:
        """Currently-online kf accounts."""
        client = self.auth.to_client()
        data = client.customservice.get_online_accounts()
        return {"success": True, "data": data}

    def upload_avatar(self, account: str, file_path: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        with open_file(file_path, "rb") as fh:
            data = client.customservice.upload_headimg(account, fh)
        return {"success": True, "data": data}

    # ---------- sessions ----------

    def create_session(
        self, openid: str, account: str, text: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.customservice.create_session(openid, account, text=text)
        return {"success": True, "data": data}

    def close_session(
        self, openid: str, account: str, text: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.customservice.close_session(openid, account, text=text)
        return {"success": True, "data": data}

    def get_session(self, openid: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.customservice.get_session(openid)
        return {"success": True, "data": data}

    def list_sessions(self, account: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.customservice.get_session_list(account)
        return {"success": True, "data": data}

    def waiting(self) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.customservice.get_wait_case()
        return {"success": True, "data": data}

    def records(
        self,
        start_time: int,
        end_time: int,
        msgid: int = 1,
        number: int = 10000,
    ) -> Dict[str, Any]:
        """Fetch chat records (within a single calendar day). UNIX seconds."""
        client = self.auth.to_client()
        data = client.customservice.get_records(
            int(start_time), int(end_time), msgid=int(msgid), number=int(number)
        )
        return {"success": True, "data": data}
