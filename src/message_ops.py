"""Message operations: customer service (客服) + mass-send + template + subscribe.

- `send_*`   — 客服消息（48h 内粉丝）
- `mass_*`   — 群发消息（按标签/openid 列表/全员）
- `template` — 模板消息（服务号）
- `subscribe`— 订阅通知
- `auto_reply_info` — 读取已配置的自动回复规则
"""

from typing import Any, Dict, List, Optional, Union

from .auth import WeChatAuth
from .utils import dispatch


class MessageOps:
    """Wraps `client.message` (customer service + mass + template)."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    # ---------- 客服消息 ----------

    def send_text(
        self, openid: str, content: str, kf_account: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_text(openid, content, account=kf_account)
        return {"success": True, "data": data}

    def send_image(
        self, openid: str, media_id: str, kf_account: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_image(openid, media_id, account=kf_account)
        return {"success": True, "data": data}

    def send_voice(
        self, openid: str, media_id: str, kf_account: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_voice(openid, media_id, account=kf_account)
        return {"success": True, "data": data}

    def send_video(
        self,
        openid: str,
        media_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        kf_account: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_video(
            openid, media_id, title=title, description=description, account=kf_account
        )
        return {"success": True, "data": data}

    def send_articles(
        self,
        openid: str,
        articles: Union[List[Dict[str, Any]], str],
        kf_account: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send an 图文消息 — either a list of external links (news) or a
        media_id for an MP-hosted news (mpnews).
        """
        client = self.auth.to_client()
        data = client.message.send_articles(openid, articles, account=kf_account)
        return {"success": True, "data": data}

    def send_link(
        self,
        openid: str,
        title: str,
        description: str,
        url: str,
        thumb_url: str,
        kf_account: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_link(
            openid,
            {"title": title, "description": description, "url": url, "thumb_url": thumb_url},
            account=kf_account,
        )
        return {"success": True, "data": data}

    def send_card(
        self,
        openid: str,
        card_id: str,
        card_ext: Optional[Dict[str, Any]] = None,
        kf_account: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_card(openid, card_id, card_ext=card_ext, account=kf_account)
        return {"success": True, "data": data}

    def send_miniprogram(
        self,
        openid: str,
        miniprogrampage: Dict[str, Any],
        kf_account: Optional[str] = None,
    ) -> Dict[str, Any]:
        """`miniprogrampage`: {title, appid, pagepath, thumb_media_id}."""
        client = self.auth.to_client()
        data = client.message.send_mini_program_page(
            openid, miniprogrampage, account=kf_account
        )
        return {"success": True, "data": data}

    def send_menu(
        self,
        openid: str,
        head_content: str,
        list_items: List[Dict[str, str]],
        tail_content: str = "",
        kf_account: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Menu message: `list_items` like [{"id": "101", "content": "option"}]."""
        client = self.auth.to_client()
        msgmenu = {
            "head_content": head_content,
            "list": list_items,
            "tail_content": tail_content,
        }
        data = client.message.send_msg_menu(openid, msgmenu, account=kf_account)
        return {"success": True, "data": data}

    # ---------- 群发 ----------

    def mass_text(
        self,
        content: str,
        tag_or_users: Optional[Union[int, List[str]]] = None,
        is_to_all: bool = False,
        preview: bool = False,
        send_ignore_reprint: int = 0,
        client_msg_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Mass-send text. `tag_or_users`: int=tag, list=openids, None+is_to_all."""
        client = self.auth.to_client()
        data = client.message.send_mass_text(
            content,
            tag_or_users=tag_or_users,
            is_to_all=is_to_all,
            preview=preview,
            send_ignore_reprint=int(send_ignore_reprint),
            client_msg_id=client_msg_id,
        )
        return {"success": True, "data": data}

    def mass_image(
        self,
        media_id: str,
        tag_or_users: Optional[Union[int, List[str]]] = None,
        is_to_all: bool = False,
        preview: bool = False,
        send_ignore_reprint: int = 0,
        client_msg_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_mass_image(
            media_id,
            tag_or_users=tag_or_users,
            is_to_all=is_to_all,
            preview=preview,
            send_ignore_reprint=int(send_ignore_reprint),
            client_msg_id=client_msg_id,
        )
        return {"success": True, "data": data}

    def mass_voice(
        self,
        media_id: str,
        tag_or_users: Optional[Union[int, List[str]]] = None,
        is_to_all: bool = False,
        preview: bool = False,
        send_ignore_reprint: int = 0,
        client_msg_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_mass_voice(
            media_id,
            tag_or_users=tag_or_users,
            is_to_all=is_to_all,
            preview=preview,
            send_ignore_reprint=int(send_ignore_reprint),
            client_msg_id=client_msg_id,
        )
        return {"success": True, "data": data}

    def mass_video(
        self,
        media_id: str,
        tag_or_users: Optional[Union[int, List[str]]] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_to_all: bool = False,
        preview: bool = False,
        send_ignore_reprint: int = 0,
        client_msg_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.send_mass_video(
            media_id,
            tag_or_users=tag_or_users,
            title=title,
            description=description,
            is_to_all=is_to_all,
            preview=preview,
            send_ignore_reprint=int(send_ignore_reprint),
            client_msg_id=client_msg_id,
        )
        return {"success": True, "data": data}

    def mass_article(
        self,
        media_id: str,
        tag_or_users: Optional[Union[int, List[str]]] = None,
        is_to_all: bool = False,
        preview: bool = False,
        send_ignore_reprint: int = 0,
        client_msg_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Mass-send图文 using mpnews media_id."""
        client = self.auth.to_client()
        data = client.message.send_mass_article(
            media_id,
            tag_or_users=tag_or_users,
            is_to_all=is_to_all,
            preview=preview,
            send_ignore_reprint=int(send_ignore_reprint),
            client_msg_id=client_msg_id,
        )
        return {"success": True, "data": data}

    def mass_status(self, msg_id: Union[int, str]) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.get_mass(msg_id)
        return {"success": True, "data": data}

    def mass_delete(self, msg_id: Union[int, str]) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.message.delete_mass(msg_id)
        return {"success": True, "data": data}

    # ---------- 模板消息 ----------

    def send_template(
        self,
        openid: str,
        template_id: str,
        data: Dict[str, Any],
        url: Optional[str] = None,
        mini_program: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        res = client.message.send_template(
            openid, template_id, data=data, url=url, mini_program=mini_program
        )
        return {"success": True, "data": res}

    # ---------- 订阅通知 ----------

    def send_subscribe(
        self,
        openid: str,
        template_id: str,
        data: Dict[str, Any],
        page: Optional[str] = None,
        miniprogram: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Service-account subscribe-message. Needs user opt-in first."""
        client = self.auth.to_client()
        res = client.message.send_subscribe_message(
            openid, template_id, data=data, page=page, miniprogram=miniprogram
        )
        return {"success": True, "data": res}

    def send_subscribe_one_time(
        self,
        openid: str,
        template_id: str,
        scene: int,
        title: str,
        data: Dict[str, Any],
        url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """One-time subscription message."""
        client = self.auth.to_client()
        res = client.message.send_subscribe_template(
            openid, template_id, int(scene), title, data, url=url
        )
        return {"success": True, "data": res}

    def auto_reply_info(self) -> Dict[str, Any]:
        """Read the currently-configured auto-reply rules from MP backend."""
        client = self.auth.to_client()
        data = client.message.get_autoreply_info()
        return {"success": True, "data": data}
