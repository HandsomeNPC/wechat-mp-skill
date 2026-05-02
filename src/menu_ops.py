"""Menu operations: create / update / delete custom menus (including
conditional/personalized menus).
"""

from typing import Any, Dict, List, Optional

from .auth import WeChatAuth
from .utils import dispatch


class MenuOps:
    """Wrapper around `client.menu`."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    def get(self) -> Dict[str, Any]:
        """Fetch the active menu, or None when no menu has been published."""
        client = self.auth.to_client()
        data = client.menu.get()
        return {"success": True, "data": data}

    def get_info(self) -> Dict[str, Any]:
        """Fetch the current self-menu configuration (from MP backend)."""
        client = self.auth.to_client()
        data = client.menu.get_menu_info()
        return {"success": True, "data": data}

    def create(self, buttons: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create or replace the top-level menu.

        `buttons` is the same shape WeChat expects, e.g.
        [{"type": "click", "name": "..", "key": ".."}, ...]
        """
        client = self.auth.to_client()
        data = client.menu.create({"button": buttons})
        return {"success": True, "data": data}

    def update(self, buttons: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Alias for create — WeChat does not have a separate update endpoint."""
        return self.create(buttons=buttons)

    def delete(self) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.menu.delete()
        return {"success": True, "data": data}

    def add_conditional(
        self, buttons: List[Dict[str, Any]], matchrule: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a personalized (conditional) menu.

        `matchrule` may include tag_id, sex, country, province, city,
        client_platform_type, language.
        """
        client = self.auth.to_client()
        data = client.menu.add_conditional(
            {"button": buttons, "matchrule": matchrule}
        )
        return {"success": True, "data": data}

    def del_conditional(self, menu_id: str) -> Dict[str, Any]:
        client = self.auth.to_client()
        data = client.menu.del_conditional(menu_id)
        return {"success": True, "data": data}

    def try_match(self, user_id: str) -> Dict[str, Any]:
        """Test which conditional menu an openid (or wx-id) would see."""
        client = self.auth.to_client()
        data = client.menu.try_match(user_id)
        return {"success": True, "data": data}
