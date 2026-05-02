"""Tag operations: create/get/update tags, batch-tag users, blacklist."""

from typing import Any, Dict, List, Optional, Union

from .auth import WeChatAuth
from .utils import dispatch


class TagOps:
    """Wraps `client.tag`."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    # ---------- tags ----------

    def create(self, name: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.create(name)
        return {"success": True, "data": data}

    def list(self) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.get()
        return {"success": True, "data": data}

    def update(self, tag_id: int, name: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.update(int(tag_id), name)
        return {"success": True, "data": data}

    def delete(self, tag_id: int) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.delete(int(tag_id))
        return {"success": True, "data": data}

    # ---------- members ----------

    def tag_users(
        self, tag_id: int, openid_list: Union[str, List[str]]
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.tag_user(int(tag_id), openid_list)
        return {"success": True, "data": data}

    def untag_users(
        self, tag_id: int, openid_list: Union[str, List[str]]
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.untag_user(int(tag_id), openid_list)
        return {"success": True, "data": data}

    def user_tags(self, openid: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.get_user_tag(openid)
        return {"success": True, "data": data}

    def tag_members(
        self, tag_id: int, next_openid: Optional[str] = None
    ) -> Dict[str, Any]:
        """One page of users under a tag."""
        client = self.auth.to_client()
        data = client.tag.get_tag_users(int(tag_id), first_user_id=next_openid)
        return {"success": True, "data": data}

    def tag_members_all(
        self, tag_id: int, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Walk all pages under a tag."""
        client = self.auth.to_client()
        collected: List[str] = []
        for openid in client.tag.iter_tag_users(int(tag_id)):
            collected.append(openid)
            if limit and len(collected) >= int(limit):
                break
        return {"success": True, "count": len(collected), "openids": collected}

    # ---------- blacklist ----------

    def blacklist(self, begin_openid: Optional[str] = None) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.get_black_list(begin_openid=begin_openid)
        return {"success": True, "data": data}

    def block(self, openid_list: List[str]) -> Dict[str, Any]:
        """Blacklist up to 20 users."""
        client = self.auth.to_client()
        data = client.tag.batch_black_list(openid_list)
        return {"success": True, "data": data}

    def unblock(self, openid_list: List[str]) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.tag.batch_unblack_list(openid_list)
        return {"success": True, "data": data}
