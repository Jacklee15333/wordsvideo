# -*- coding: utf-8 -*-
"""Windows 剪贴板：写（把提示词放进去）、读（看你从网页 AI 复制了什么）。来自出题助手 chuti_helper 里测过的写法。"""
import os, subprocess, sys, tempfile, time

WIN = os.name == "nt"


def _u32():
    import ctypes
    from ctypes import wintypes
    u32 = ctypes.WinDLL("user32", use_last_error=True)
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    u32.OpenClipboard.argtypes = [wintypes.HWND]; u32.OpenClipboard.restype = wintypes.BOOL
    u32.EmptyClipboard.restype = wintypes.BOOL
    u32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]; u32.SetClipboardData.restype = wintypes.HANDLE
    u32.GetClipboardData.argtypes = [wintypes.UINT]; u32.GetClipboardData.restype = wintypes.HANDLE
    u32.CloseClipboard.restype = wintypes.BOOL
    u32.GetClipboardSequenceNumber.restype = wintypes.DWORD
    k32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]; k32.GlobalAlloc.restype = wintypes.HANDLE
    k32.GlobalLock.argtypes = [wintypes.HANDLE]; k32.GlobalLock.restype = ctypes.c_void_p
    k32.GlobalUnlock.argtypes = [wintypes.HANDLE]; k32.GlobalUnlock.restype = wintypes.BOOL
    return ctypes, u32, k32


def _open(u32):
    for _ in range(20):
        if u32.OpenClipboard(None):
            return True
        time.sleep(0.1)
    return False


def seq():
    """剪贴板变一次这个数就加一（不读内容，很便宜）。不是 Windows 返回 0。"""
    if not WIN:
        return 0
    try:
        return int(_u32()[1].GetClipboardSequenceNumber())
    except Exception:
        return 0


def set_text(text):
    if not WIN:
        return False
    try:
        ctypes, u32, k32 = _u32()
        data = text.encode("utf-16-le") + b"\x00\x00"
        if not _open(u32):
            raise OSError("剪贴板被别的程序占着")
        try:
            u32.EmptyClipboard()
            h = k32.GlobalAlloc(0x0002, len(data))
            p = k32.GlobalLock(h)
            ctypes.memmove(p, data, len(data))
            k32.GlobalUnlock(h)
            if u32.SetClipboardData(13, h):
                return True
        finally:
            u32.CloseClipboard()
    except Exception:
        pass
    fd, p = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        r = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                            "Get-Content -Raw -Encoding UTF8 -LiteralPath '%s' | Set-Clipboard" % p.replace("'", "''")],
                           capture_output=True, timeout=60, creationflags=0x08000000)
        return r.returncode == 0
    except Exception:
        return False
    finally:
        os.remove(p)


def get_text():
    if not WIN:
        return ""
    try:
        ctypes, u32, k32 = _u32()
        if not _open(u32):
            return ""
        try:
            h = u32.GetClipboardData(13)
            if not h:
                return ""
            p = k32.GlobalLock(h)
            try:
                return ctypes.wstring_at(p) if p else ""
            finally:
                k32.GlobalUnlock(h)
        finally:
            u32.CloseClipboard()
    except Exception:
        return ""


def beep():
    if WIN:
        try:
            import winsound
            winsound.MessageBeep(0x40)
        except Exception:
            pass
