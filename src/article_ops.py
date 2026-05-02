"""Article operations: draft + free-publish.

Covers the modern WeChat 公众号 content flow:

  upload thumb (material) → add draft → submit freepublish → list/delete

Wraps `client.draft` and `client.freepublish` from wechatpy.
"""

from typing import Any, Dict, List, Optional

from .auth import WeChatAuth
from .utils import dispatch


class ArticleOps:
    """Draft-box + free-publish wrapper."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    # ---------- draft box ----------

    def draft_add(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a new draft from one or more articles.

        Each article dict must contain: title, content, thumb_media_id.
        Optional: author, digest, content_source_url, need_open_comment,
        only_fans_can_comment.
        """
        client = self.auth.to_client()
        data = client.draft.add(articles)
        return {"success": True, "data": data}

    def draft_get(self, media_id: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.draft.get(media_id)
        return {"success": True, "data": data}

    def draft_update(
        self, media_id: str, index: int, articles: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Replace a single article (by index, starting at 0) in a draft."""
        client = self.auth.to_client()
        data = client.draft.update(media_id, index, articles)
        return {"success": True, "data": data}

    def draft_delete(self, media_id: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.draft.delete(media_id)
        return {"success": True, "data": data}

    def draft_list(
        self, offset: int = 0, count: int = 20, no_content: int = 0
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.draft.batchget(
            offset=int(offset), count=int(count), no_content=int(no_content)
        )
        return {"success": True, "data": data}

    def draft_count(self) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.draft.count()
        return {"success": True, "data": data}

    # ---------- free-publish ----------

    def publish(self, media_id: str) -> Dict[str, Any]:
        """Submit a draft for publication. Returns a publish_id for polling."""
        client = self.auth.to_client()
        data = client.freepublish.submit(media_id)
        return {"success": True, "data": data}

    def publish_status(self, publish_id: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.freepublish.get(publish_id)
        return {"success": True, "data": data}

    def publish_delete(self, article_id: str, index: int = 0) -> Dict[str, Any]:
        """Delete a published article. index=0 deletes all sub-articles."""
        client = self.auth.to_client()
        data = client.freepublish.delete(article_id, index=int(index))
        return {"success": True, "data": data}

    def publish_get(self, article_id: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.freepublish.getarticle(article_id)
        return {"success": True, "data": data}

    def publish_list(
        self, offset: int = 0, count: int = 20, no_content: int = 0
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.freepublish.batchget(
            offset=int(offset), count=int(count), no_content=int(no_content)
        )
        return {"success": True, "data": data}
