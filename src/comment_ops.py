"""Comment operations on already-published MP articles.

WeChat's comment API is a bit quirky: articles have a `msg_data_id` (the mass
message id) plus an `index` for multi-article posts. Supports open/close,
list, elect/unelect, delete, reply, delete-reply.
"""

from typing import Any, Dict

from .auth import WeChatAuth
from .utils import dispatch


class CommentOps:
    """Wraps the comment endpoints on `client.material`."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    def open(self, msg_data_id: int, index: int = 1) -> Dict[str, Any]:
        """Re-enable comments on a published article."""
        client = self.auth.to_client()
        data = client.material.open_comment(msg_data_id, index=int(index))
        return {"success": True, "data": data}

    def close(self, msg_data_id: int, index: int = 1) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.material.close_comment(msg_data_id, index=int(index))
        return {"success": True, "data": data}

    def list(
        self,
        msg_data_id: int,
        index: int = 1,
        begin: int = 0,
        count: int = 50,
        type: int = 0,
    ) -> Dict[str, Any]:
        """List comments. type: 0=all, 1=featured, 2=not-featured."""
        client = self.auth.to_client()
        data = client.material.list_comment(
            msg_data_id,
            index=int(index),
            begin=int(begin),
            count=int(count),
            type=int(type),
        )
        return {"success": True, "data": data}

    def mark_elect(
        self, msg_data_id: int, index: int, user_comment_id: int
    ) -> Dict[str, Any]:
        """Mark a comment as 精选."""
        client = self.auth.to_client()
        data = client.material.markelect_comment(
            msg_data_id, index=int(index), user_comment_id=int(user_comment_id)
        )
        return {"success": True, "data": data}

    def unmark_elect(
        self, msg_data_id: int, index: int, user_comment_id: int
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.material.unmarkelect_comment(
            msg_data_id, index=int(index), user_comment_id=int(user_comment_id)
        )
        return {"success": True, "data": data}

    def delete(
        self, msg_data_id: int, index: int, user_comment_id: int
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.material.delete_comment(
            msg_data_id, index=int(index), user_comment_id=int(user_comment_id)
        )
        return {"success": True, "data": data}

    def reply(
        self,
        msg_data_id: int,
        index: int,
        user_comment_id: int,
        content: str,
    ) -> Dict[str, Any]:
        """Reply to a user comment as the 公众号."""
        client = self.auth.to_client()
        data = client.material.add_reply_comment(
            msg_data_id,
            index=int(index),
            user_comment_id=int(user_comment_id),
            content=content,
        )
        return {"success": True, "data": data}

    def delete_reply(
        self, msg_data_id: int, index: int, user_comment_id: int
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.material.delete_reply_comment(
            msg_data_id, index=int(index), user_comment_id=int(user_comment_id)
        )
        return {"success": True, "data": data}
