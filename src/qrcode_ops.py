"""QR-code, customer-service accounts, and misc helpers (server IPs, network)."""

from typing import Any, Dict, Optional

from .auth import WeChatAuth
from .utils import dispatch


class QRCodeOps:
    """Wraps `client.qrcode` (parametric scene QR codes)."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    def temp_id(self, scene_id: int, expire_seconds: int = 1800) -> Dict[str, Any]:
        """Temporary scene QR (numeric scene_id, 1..100000)."""
        client = self.auth.to_client()
        res = client.qrcode.create({
            "expire_seconds": int(expire_seconds),
            "action_name": "QR_SCENE",
            "action_info": {"scene": {"scene_id": int(scene_id)}},
        })
        url = client.qrcode.get_url(res.get("ticket", ""))
        return {"success": True, "data": res, "url": url}

    def temp_str(
        self, scene_str: str, expire_seconds: int = 1800
    ) -> Dict[str, Any]:
        """Temporary scene QR with string scene."""
        client = self.auth.to_client()
        res = client.qrcode.create({
            "expire_seconds": int(expire_seconds),
            "action_name": "QR_STR_SCENE",
            "action_info": {"scene": {"scene_str": scene_str}},
        })
        url = client.qrcode.get_url(res.get("ticket", ""))
        return {"success": True, "data": res, "url": url}

    def perm_id(self, scene_id: int) -> Dict[str, Any]:
        """Permanent scene QR (1..100000)."""
        client = self.auth.to_client()
        res = client.qrcode.create({
            "action_name": "QR_LIMIT_SCENE",
            "action_info": {"scene": {"scene_id": int(scene_id)}},
        })
        url = client.qrcode.get_url(res.get("ticket", ""))
        return {"success": True, "data": res, "url": url}

    def perm_str(self, scene_str: str) -> Dict[str, Any]:
        """Permanent scene QR with string scene."""
        client = self.auth.to_client()
        res = client.qrcode.create({
            "action_name": "QR_LIMIT_STR_SCENE",
            "action_info": {"scene": {"scene_str": scene_str}},
        })
        url = client.qrcode.get_url(res.get("ticket", ""))
        return {"success": True, "data": res, "url": url}

    def show_url(self, ticket: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        url = client.qrcode.get_url(ticket)
        return {"success": True, "url": url}

    def download(self, ticket: str, output_path: str) -> Dict[str, Any]:
        """Download the QR PNG to disk."""
        import os

        client = self.auth.to_client()
        resp = client.qrcode.show(ticket)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(resp.content)
        return {"success": True, "path": output_path, "bytes": len(resp.content)}


class MiscOps:
    """Server IPs / network probe / short-URL (deprecated)."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    def server_ips(self) -> Dict[str, Any]:
        client = self.auth.to_client()
        return {"success": True, "data": client.misc.get_wechat_ips()}

    def check_network(
        self, action: str = "all", operator: str = "DEFAULT"
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.misc.check_network(action=action, operator=operator)
        return {"success": True, "data": data}

    def short_url(self, long_url: str) -> Dict[str, Any]:
        """Deprecated by WeChat — kept for completeness."""
        client = self.auth.to_client()
        data = client.misc.short_url(long_url)
        return {"success": True, "data": data}
