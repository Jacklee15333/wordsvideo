"""web_tools.py —— 给 web_model.py 用的最小替身（原版在超能小助里）。
web_model 只用到这里的两个函数：_read_proxy()（AI 池走哪个代理）和 _ssl_ctx()（HTTPS 证书）。"""
import json
from pathlib import Path

_CFG = Path(__file__).resolve().parent.parent / "data" / "config.json"
_SSL = None


def _read_proxy():
    try:
        return (json.loads(_CFG.read_text(encoding="utf-8")).get("aiProxy") or "").strip()
    except Exception:
        return ""


def _ssl_ctx():
    global _SSL
    if _SSL is None:
        import ssl
        ctx = ssl.create_default_context()
        try:
            import certifi
            ctx.load_verify_locations(certifi.where())
        except Exception:
            pass
        _SSL = ctx
    return _SSL
