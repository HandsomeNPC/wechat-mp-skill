"""Shared utilities for the wechat-skill modules."""

import inspect
from typing import Any, Callable, Dict, Awaitable


async def dispatch(
    instance: Any,
    action: str,
    **kwargs,
) -> Dict[str, Any]:
    """Dispatch `action` to a method on `instance`, awaiting if needed.

    All public modules expose `execute(action, **kwargs)` that funnels through
    here. Coroutines are awaited; sync methods are run directly. Errors are
    captured into a `{success: False, message: ...}` envelope.
    """
    method: Callable | None = getattr(instance, action, None)
    if not method or not callable(method) or action.startswith("_"):
        available = [
            n for n in dir(instance)
            if not n.startswith("_") and callable(getattr(instance, n))
            and n not in {"execute"}
        ]
        return {
            "success": False,
            "message": f"Unknown action: {action}",
            "available": sorted(available),
        }
    try:
        result = method(**kwargs)
        if inspect.isawaitable(result):
            result = await result
    except TypeError as e:
        return {"success": False, "message": f"Bad arguments to {action}: {e}"}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "message": f"{type(e).__name__}: {e}"}

    if isinstance(result, dict) and "success" in result:
        return result
    return {"success": True, "data": result}


def open_file(path: str, mode: str = "rb"):
    """Helper: open a file for upload, with a clearer error than wechatpy."""
    import os
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return open(path, mode)
