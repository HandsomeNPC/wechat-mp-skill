"""Data analytics (datacube): user growth, article reads, messages, interfaces.

All endpoints take a date range. WeChat enforces:
- max 7-day window per request
- begin_date must be ≥ today − 180 days
"""

import datetime
from typing import Any, Dict, Optional

from .auth import WeChatAuth
from .utils import dispatch


def _default_range(days: int = 7) -> tuple[str, str]:
    today = datetime.date.today()
    begin = today - datetime.timedelta(days=days)
    end = today - datetime.timedelta(days=1)
    return begin.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


class DataOps:
    """Wraps `client.datacube`."""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        return await dispatch(self, action, **kwargs)

    def _range(self, begin_date: Optional[str], end_date: Optional[str]):
        if begin_date and end_date:
            return begin_date, end_date
        return _default_range()

    # ---------- 用户分析 ----------

    def user_summary(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Daily new/lost followers."""
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_user_summary(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def user_cumulate(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cumulative follower count by day."""
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_user_cumulate(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    # ---------- 图文分析 ----------

    def article_summary(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_article_summary(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def article_total(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_article_total(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def user_read(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_user_read(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def user_read_hour(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_user_read_hour(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def user_share(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_user_share(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def user_share_hour(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_user_share_hour(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    # ---------- 消息分析 ----------

    def upstream_msg(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_upstream_msg(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def upstream_msg_hour(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_upstream_msg_hour(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def upstream_msg_week(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_upstream_msg_week(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def upstream_msg_month(
        self,
        begin_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_upstream_msg_month(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def upstream_msg_dist(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_upstream_msg_dist(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    # ---------- 接口分析 ----------

    def interface_summary(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_interface_summary(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}

    def interface_summary_hour(
        self, begin_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self.auth.to_client()
        b, e = self._range(begin_date, end_date)
        data = client.datacube.get_interface_summary_hour(b, e)
        return {"success": True, "begin": b, "end": e, "data": data}
