"""User operations: follower list, profile, remark, union IDs."""

from typing import Any, Dict, List, Optional, Union

from .auth import WeChatAuth
from .utils import dispatch


class UserOps:
    """Wraps `client.user`."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    def get(self, openid: str, lang: str = "zh_CN") -> Dict[str, Any]:
        """Fetch a single user's profile."""
        client = self.auth.to_client()
        data = client.user.get(openid, lang=lang)
        return {"success": True, "data": data}

    def batch_get(
        self, openid_list: List[Union[str, Dict[str, str]]]
    ) -> Dict[str, Any]:
        """Fetch up to 100 users. Items may be raw openids or {openid, lang}."""
        client = self.auth.to_client()
        data = client.user.get_batch(openid_list)
        return {"success": True, "data": data}

    def list_followers(self, next_openid: Optional[str] = None) -> Dict[str, Any]:
        """One page of follower openids (WeChat returns up to 10000 per page)."""
        client = self.auth.to_client()
        data = client.user.get_followers(first_user_id=next_openid)
        return {"success": True, "data": data}

    def list_all_followers(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Walk the follower pages and return the full openid list."""
        client = self.auth.to_client()
        collected: List[str] = []
        for openid in client.user.iter_followers():
            collected.append(openid)
            if limit and len(collected) >= int(limit):
                break
        return {"success": True, "count": len(collected), "openids": collected}

    def update_remark(self, openid: str, remark: str) -> Dict[str, Any]:
        """Set a remark name for a user (visible only in the 后台)."""
        client = self.auth.to_client()
        data = client.user.update_remark(openid, remark)
        return {"success": True, "data": data}

    def change_openid(
        self, from_appid: str, openid_list: List[str]
    ) -> Dict[str, Any]:
        """Translate openids from another appid after an MP-subject migration."""
        client = self.auth.to_client()
        data = client.user.change_openid(from_appid, openid_list)
        return {"success": True, "data": data}
