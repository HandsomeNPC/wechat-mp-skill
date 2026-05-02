"""Callback-message parsing and auto-reply construction.

公众号 server-side message handling:

- `verify`     — validate the signature on the initial URL verification ping
- `parse`      — decrypt (if enabled) + parse an incoming XML message, returning
                 a structured dict describing the event / message
- `reply_text` — build a plain-text XML reply (optionally re-encrypting)
- `reply_articles` — build a news (图文) reply

Useful when running a Flask/FastAPI/Django hook that receives callbacks.
"""

from typing import Any, Dict, List, Optional

from .auth import WeChatAuth
from .utils import dispatch


def _msg_to_dict(msg: Any) -> Dict[str, Any]:
    """Convert a wechatpy message/event object into a JSON-safe dict."""
    if msg is None:
        return {}
    out: Dict[str, Any] = {}
    for attr in dir(msg):
        if attr.startswith("_"):
            continue
        try:
            val = getattr(msg, attr)
        except Exception:
            continue
        if callable(val):
            continue
        # Only keep JSON-friendly primitives
        if isinstance(val, (str, int, float, bool)) or val is None:
            out[attr] = val
        elif isinstance(val, (list, tuple)):
            out[attr] = [str(x) for x in val]
    return out


class CallbackOps:
    """Verify + decrypt + parse incoming WeChat 公众号 callbacks."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    def verify(
        self, signature: str, timestamp: str, nonce: str, echostr: str
    ) -> Dict[str, Any]:
        """URL validation during 服务器配置 setup."""
        from wechatpy.utils import check_signature
        from wechatpy.exceptions import InvalidSignatureException

        if not self.auth.token:
            return {"success": False, "message": "callback token not configured"}
        try:
            check_signature(self.auth.token, signature, timestamp, nonce)
        except InvalidSignatureException as e:
            return {"success": False, "message": f"signature invalid: {e}"}
        return {"success": True, "echostr": echostr}

    def parse(
        self,
        xml: str,
        signature: Optional[str] = None,
        timestamp: Optional[str] = None,
        nonce: Optional[str] = None,
        msg_signature: Optional[str] = None,
        mode: str = "plain",
    ) -> Dict[str, Any]:
        """Parse an incoming XML body.

        `mode`: "plain" (普通模式), "compat" (兼容模式), or "safe" (安全模式).
        safe/compat require aes_key+token+appid and all three signature args.
        """
        from wechatpy import parse_message

        if mode in ("safe", "compat"):
            crypto = self.auth.to_crypto()
            decrypted = crypto.decrypt_message(
                xml, msg_signature or signature, timestamp, nonce
            )
            msg = parse_message(decrypted)
        else:
            msg = parse_message(xml)
        return {"success": True, "message": _msg_to_dict(msg), "type": getattr(msg, "type", None)}

    def reply_text(
        self,
        from_user: str,
        to_user: str,
        content: str,
        encrypt: bool = False,
        timestamp: Optional[str] = None,
        nonce: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build the XML body for a text auto-reply.

        `from_user` is the 公众号 (received as ToUserName of the inbound msg)
        and `to_user` is the fan (received as FromUserName). Set
        `encrypt=True` to re-encrypt for 安全模式.
        """
        from wechatpy.replies import TextReply

        # Build a fake source object with source/target so TextReply can fill
        # the XML skeleton. A SimpleNamespace is enough for wechatpy.
        from types import SimpleNamespace
        src = SimpleNamespace(source=to_user, target=from_user)
        reply = TextReply(message=src, content=content)
        xml = reply.render()
        if encrypt:
            crypto = self.auth.to_crypto()
            xml = crypto.encrypt_message(xml, nonce or "", timestamp or "")
        return {"success": True, "xml": xml}

    def reply_articles(
        self,
        from_user: str,
        to_user: str,
        articles: List[Dict[str, str]],
        encrypt: bool = False,
        timestamp: Optional[str] = None,
        nonce: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build a news (图文) reply. Each article: {title, description, image, url}."""
        from wechatpy.replies import ArticlesReply
        from types import SimpleNamespace

        src = SimpleNamespace(source=to_user, target=from_user)
        reply = ArticlesReply(message=src)
        for a in articles:
            reply.add_article({
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "image": a.get("image") or a.get("picurl") or "",
                "url": a.get("url", ""),
            })
        xml = reply.render()
        if encrypt:
            crypto = self.auth.to_crypto()
            xml = crypto.encrypt_message(xml, nonce or "", timestamp or "")
        return {"success": True, "xml": xml}
