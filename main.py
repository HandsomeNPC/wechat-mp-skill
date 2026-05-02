"""WeChat Official Account Skill — Main Entry Point.

A 公众号 (Subscription/Service Account) management toolkit powered by
wechatpy. Modules:

- login        — appid/secret credential management & access_token refresh
- article      — draft box + free-publish (modern article workflow)
- material     — permanent + temporary assets (image/voice/video/thumb)
- menu         — custom menus, including conditional/personalized menus
- message      — customer service / mass-send / template / subscribe
- comment      — published-article comment management
- user         — followers, profiles, remarks
- tag          — user tagging + blacklist
- data         — datacube analytics (users/articles/messages/interfaces)
- qrcode       — parametric scene QR codes
- customservice— 多客服 account & session control
- callback     — 服务器配置 message verification + parsing

Run: `python main.py <module> <action> '<json-args>'`
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, Optional

from src.auth import WeChatAuth
from src.login_manager import LoginManager
from src.article_ops import ArticleOps
from src.material_ops import MaterialOps
from src.menu_ops import MenuOps
from src.message_ops import MessageOps
from src.comment_ops import CommentOps
from src.user_ops import UserOps
from src.tag_ops import TagOps
from src.data_ops import DataOps
from src.qrcode_ops import QRCodeOps, MiscOps
from src.customservice_ops import CustomServiceOps
from src.callback_ops import CallbackOps


class WeChatAllInOne:
    """Unified interface across all 公众号 capabilities."""

    def __init__(
        self,
        appid: Optional[str] = None,
        secret: Optional[str] = None,
        access_token: Optional[str] = None,
        token: Optional[str] = None,
        aes_key: Optional[str] = None,
        credential_file: Optional[str] = None,
        persist: Optional[bool] = None,
    ):
        self.auth = WeChatAuth(
            appid=appid,
            secret=secret,
            access_token=access_token,
            token=token,
            aes_key=aes_key,
            credential_file=credential_file,
            persist=persist,
        )

        self.login = LoginManager(auth=self.auth)
        self.article = ArticleOps(auth=self.auth)
        self.material = MaterialOps(auth=self.auth)
        self.menu = MenuOps(auth=self.auth)
        self.message = MessageOps(auth=self.auth)
        self.comment = CommentOps(auth=self.auth)
        self.user = UserOps(auth=self.auth)
        self.tag = TagOps(auth=self.auth)
        self.data = DataOps(auth=self.auth)
        self.qrcode = QRCodeOps(auth=self.auth)
        self.misc = MiscOps(auth=self.auth)
        self.customservice = CustomServiceOps(auth=self.auth)
        self.callback = CallbackOps(auth=self.auth)

    async def execute(self, skill_name: str, action: str, **kwargs) -> Dict[str, Any]:
        skill_map = {
            # login / credentials
            "login": lambda: self.login,
            "auth": lambda: self.login,

            # articles
            "article": lambda: self.article,
            "article_ops": lambda: self.article,
            "draft": lambda: self.article,
            "publish": lambda: self.article,

            # material
            "material": lambda: self.material,
            "material_ops": lambda: self.material,
            "media": lambda: self.material,

            # menu
            "menu": lambda: self.menu,
            "menu_ops": lambda: self.menu,

            # message
            "message": lambda: self.message,
            "message_ops": lambda: self.message,
            "msg": lambda: self.message,

            # comment
            "comment": lambda: self.comment,
            "comment_ops": lambda: self.comment,

            # user
            "user": lambda: self.user,
            "user_ops": lambda: self.user,

            # tag
            "tag": lambda: self.tag,
            "tag_ops": lambda: self.tag,

            # data
            "data": lambda: self.data,
            "data_ops": lambda: self.data,
            "analytics": lambda: self.data,
            "datacube": lambda: self.data,

            # qrcode
            "qrcode": lambda: self.qrcode,
            "qr": lambda: self.qrcode,

            # misc
            "misc": lambda: self.misc,

            # customer service
            "customservice": lambda: self.customservice,
            "kf": lambda: self.customservice,

            # callback
            "callback": lambda: self.callback,
            "server": lambda: self.callback,
        }
        skill_factory = skill_map.get(skill_name)
        if not skill_factory:
            return {
                "success": False,
                "message": f"Unknown module: {skill_name}",
                "available": sorted(set(skill_map.keys())),
            }
        try:
            skill = skill_factory()
        except Exception as e:  # noqa: BLE001
            return {"success": False, "message": str(e)}
        return await skill.execute(action=action, **kwargs)


async def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <module> <action> [params_json]")
        print()
        print("Modules:")
        print("  login           - appid/secret 凭证管理")
        print("  article         - 草稿 + 发布")
        print("  material        - 永久/临时素材")
        print("  menu            - 自定义菜单")
        print("  message         - 客服/群发/模板/订阅消息")
        print("  comment         - 已发布文章评论管理")
        print("  user            - 用户/粉丝管理")
        print("  tag             - 标签 + 黑名单")
        print("  data            - 数据分析（datacube）")
        print("  qrcode          - 带参二维码")
        print("  customservice   - 多客服账号/会话")
        print("  callback        - 服务器配置回调验证 & 消息解析")
        print("  misc            - 服务器IP / 网络检测")
        print()
        print("Examples:")
        print('  python main.py login set_credentials \'{"appid": "wx...", "secret": "..."}\'')
        print('  python main.py login verify \'{}\'')
        print('  python main.py article draft_list \'{"count": 5}\'')
        print('  python main.py menu get \'{}\'')
        print('  python main.py user list_followers \'{}\'')
        print('  python main.py message send_text \'{"openid": "o...", "content": "hi"}\'')
        return

    skill_name = sys.argv[1]
    action = sys.argv[2]
    params_raw = sys.argv[3] if len(sys.argv) > 3 else "{}"
    try:
        params = json.loads(params_raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in arguments: {e}")
        print(f"  Raw input: {params_raw}")
        sys.exit(1)

    cred_file = os.path.expanduser(
        os.environ.get("WECHAT_CREDENTIAL_FILE", "~/.hermes/wechat-credentials.json")
    )
    credential_file = cred_file if os.path.exists(cred_file) else None

    app = WeChatAllInOne(credential_file=credential_file)
    result = await app.execute(skill_name=skill_name, action=action, **params)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
