"""Shared transport for the bom connector.

Mechanism: anonymous FTP to ftp.bom.gov.au (the Bureau's sanctioned automated
channel; the www HTTP site blocks programmatic access). subsets_utils has no
FTP helper, so the stdlib `ftplib` is used for transport here — the HTTP-routing
rule does not apply to FTP.
"""

import ftplib
import io
import socket

from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

FTP_HOST = "ftp.bom.gov.au"
FTP_USER = "anonymous"
FTP_PASS = "subsets@subsets.io"  # anonymous FTP accepts any email as password

# Transient FTP/network failures — retried with backoff. error_perm (permanent
# FTP 5xx) and programming bugs are deliberately NOT here so they surface.
_TRANSIENT_EXC = (
    ftplib.error_temp,
    ftplib.error_reply,
    socket.timeout,
    TimeoutError,
    ConnectionError,
    EOFError,
)


def _is_transient(exc: BaseException) -> bool:
    return isinstance(exc, _TRANSIENT_EXC)


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(5),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def ftp_retrieve(path: str) -> bytes:
    """Anonymous-FTP fetch of a single file into memory."""
    ftp = ftplib.FTP(FTP_HOST, timeout=180)
    try:
        ftp.login(FTP_USER, FTP_PASS)
        buf = io.BytesIO()
        ftp.retrbinary(f"RETR {path}", buf.write)
        return buf.getvalue()
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()
