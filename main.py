from xml.dom.minidom import parseString

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

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
