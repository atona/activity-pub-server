from xml.dom.minidom import parseString

from fastapi import Response
from fastapi.responses import JSONResponse

from .main import app

server = "activity-pub-server.onrender.com"
actor = "test"


@app.get(f"/@{actor}")
@app.get(f"/users/{actor}")
def person():
    content = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": f"https://{server}/users/{actor}",  # Fediverseで一意
        "type": "Person",
        "url": f"https://{server}/users/{actor}",  # プロフィールページのURL
        "summary": "my simple activitypub",  # 概要
        "preferredUsername": f"{actor}",  # ユーザID
        "name": "actor river dragon this help",  # 表示名
        "inbox": f"https://{server}/users/{actor}/inbox",  # このユーザへの宛先
        "outbox": f"https://{server}/users/{actor}/outbox",  # このユーザの発信元
        "publicKey": {
            "id": f"https://{server}/users/{actor}#main-key",
            "owner": f"https://{server}/users/{actor}",
            "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyPEg43747qkgIW2vbyZi\nkFmct7co1IiWXXBAoL3JzOPtHLJQGCE7+JogmmGQ3Rl3CdOjcm+0M2/xl9w0oyCU\nyx4STZ9at1Mem1Dq07e/KLMN0w/hXiR4zTeIMuVWx4/jYxjwKT1sp4ermEGmDPRD\nb2HlbN3CzHGJUlsIHSjOP9GtPy24JNItnEff0LoKMwHt6VUo8UEPmuFoxLmgmxD0\nqyryiViw0CGB4nTdy378KWTOFdLADM1LWOkmt/Ao4n0Ho0COABuhWhgPR9ymJa73\nwKbynjpj8wFU7KLuXHOlY0Bl/6mBMb2RjmpFnhJVQgqJAmMCozMw/Mp3Y4JYWsSy\nUwIDAQAB\n-----END PUBLIC KEY-----\n",
        },
    }
    headers = {"Content-Type": "application/activity+json"}
    return JSONResponse(content=content, headers=headers)


@app.get(f"/users/{actor}/note")
def note():
    content = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": f"https://{server}/users/{actor}/1",  # Fediverseで一意
        "type": "Note",
        "attributedTo": f"https://{server}/users/{actor}",  # 投稿者のPerson#id
        "content": "<p>投稿内容</p>",  # XHTMLで記述された投稿内容
        "published": "2018-06-18T12:00:00+09:00",  # ISO形式の投稿日
        "to": [  # 公開範囲
            "https://www.w3.org/ns/activitystreams#Public",  # 公開（連合？）
            f"https://{server}/users/{actor}/follower",  # フォロワー
        ],
    }
    headers = {"Content-Type": "application/activity+json"}
    return JSONResponse(content=content, headers=headers)


@app.get("/.well-known/host-meta")
def webfinger_host_meta():
    data = (
        '<?xml version="1.0"?>\
        <XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">\
            <Link rel="lrdd" type="application/xrd+xml" template="'
        + "https://"
        + server
        + '/.well-known/webfinger?resource={uri}"/>\
        </XRD>'
    )
    return Response(content=data, media_type="application/xml")


@app.get("/.well-known/webfinger")
def webfinger_resource():
    content = {
        "subject": f"acct:{actor}@{server}",
        "aliases": [f"https://{server}/@{actor}", f"https://{server}/users/{actor}"],
        "links": [
            {
                "rel": "http://webfinger.net/rel/profile-page",
                "type": "text/html",
                "href": f"https://{server}/@{actor}",
            },
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": f"https://{server}/users/{actor}",
            },
            {
                "rel": "http://ostatus.org/schema/1.0/subscribe",
                "template": f"https://{server}/authorize_interaction?uri={{uri}}",
            },
        ],
    }

    return JSONResponse(content=content)
