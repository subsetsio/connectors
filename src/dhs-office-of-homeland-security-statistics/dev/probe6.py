import ssl, httpx
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
url="https://ohss.dhs.gov/topics/immigration/yearbook"
H={"User-Agent":UA}

def trial(name, ctx):
    try:
        with httpx.Client(verify=ctx, headers=H, follow_redirects=True, timeout=60) as c:
            r=c.get(url); print(name, r.status_code, len(r.content))
    except Exception as e:
        print(name, "ERR", type(e).__name__, str(e)[:60])

# default httpx ssl
trial("httpx-default", httpx.create_ssl_context())

# stdlib default (what requests-ish uses)
trial("stdlib-default", ssl.create_default_context())

# browser-ish cipher string
c1=ssl.create_default_context(); 
try:
    c1.set_ciphers("ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DEFAULT")
except Exception as e: print("cipher set err", e)
trial("stdlib-browserciphers", c1)

# urllib3's default context object reused in httpx
import urllib3.util.ssl_ as u3
trial("urllib3-default", u3.create_urllib3_context())
