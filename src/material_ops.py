"""Material operations: permanent + temporary assets (image/voice/video/thumb).

Also exposes the uploadimg endpoint that returns a public CDN URL — useful
for embedding images inside article HTML content.
"""

import os
from typing import Any, Dict, Optional

from .auth import WeChatAuth
from .utils import dispatch, open_file


class MaterialOps:
    """Wraps `client.material` (permanent) and `client.media` (temporary)."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    # ---------- permanent ----------

    def add(
        self,
        media_type: str,
        file_path: str,
        title: Optional[str] = None,
        introduction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload permanent material. media_type: image/voice/video/thumb.

        `title` + `introduction` are required for video.
        """
        client = self.auth.to_client()
        with open_file(file_path, "rb") as fh:
            data = client.material.add(
                media_type=media_type,
                media_file=fh,
                title=title,
                introduction=introduction,
            )
        return {"success": True, "data": data}

    def get(self, media_id: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.material.get(media_id)
        return {"success": True, "data": data}

    def delete(self, media_id: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.material.delete(media_id)
        return {"success": True, "data": data}

    def list(
        self, media_type: str = "image", offset: int = 0, count: int = 20
    ) -> Dict[str, Any]:
        """List permanent material. media_type: image/voice/video/news."""
        client = self.auth.to_client()
        data = client.material.batchget(
            media_type=media_type, offset=int(offset), count=int(count)
        )
        return {"success": True, "data": data}

    def count(self) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.material.get_count()
        return {"success": True, "data": data}

    # ---------- temporary ----------

    def upload_temp(self, media_type: str, file_path: str) -> Dict[str, Any]:
        """Upload temporary material (3-day expiry). Returns media_id."""
        client = self.auth.to_client()
        with open_file(file_path, "rb") as fh:
            data = client.media.upload(media_type=media_type, media_file=fh)
        return {"success": True, "data": data}

    def download_temp(
        self, media_id: str, output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Download a temporary-material binary. Saves to disk if output_path."""
        client = self.auth.to_client()
        resp = client.media.download(media_id)
        # wechatpy returns a requests.Response for binary payloads
        content = getattr(resp, "content", None)
        if content is None:
            return {"success": True, "data": resp}
        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(content)
            return {
                "success": True,
                "path": output_path,
                "bytes": len(content),
            }
        return {"success": True, "bytes": len(content)}

    def get_temp_url(self, media_id: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        url = client.media.get_url(media_id)
        return {"success": True, "url": url}

    def upload_image(self, file_path: str) -> Dict[str, Any]:
        """Upload an image for embedding in article HTML. Returns a public URL."""
        client = self.auth.to_client()
        with open_file(file_path, "rb") as fh:
            url = client.media.upload_image(fh)
        return {"success": True, "url": url}
