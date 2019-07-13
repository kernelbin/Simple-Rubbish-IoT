import urllib.request
import urllib.parse


def send_http_request(url, data) -> str:
    with urllib.request.urlopen(url, data=urllib.parse.urlencode(data).encode()) as url:
        return url.read().decode()
