from xml.dom.minidom import parseString

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/test")
def test():
    content = {"message": "Hello World"}
    return JSONResponse(content=content)


@app.get("/")
def person():
    content = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Person",
        "id": "https://activity-pub-server.onrender.com/test",  # Fediverseで一意
        "name": "test",  # 表示名
        "preferredUsername": "test",  # ユーザID
        "summary": "my simple activitypub",  # 概要
        "inbox": "https://activity-pub-server.onrender.com/inbox",  # このユーザへの宛先
        "outbox": "https://activity-pub-server.onrender.com/outbox",  # このユーザの発信元
        "url": "https://activity-pub-server.onrender.com/test",  # プロフィールページのURL
        "icon": {
            "type": "Image",
            "mediaType": "image/png",  # mime type
            "url": "https://activity-pub-server.onrender.com/icon.ong",  # アイコン画像のURL
        },
    }
    headers = {"Content-Type": "application/activity+json"}
    return JSONResponse(content=content, headers=headers)


@app.get("/.well-known/host-meta")
def webfinger_host_meta():
    data = """<?xml version="1.0"?>
        <XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">
            <Link rel="lrdd" type="application/xrd+xml" template="https://activity-pub-server.onrender.com/.well-known/webfinger?resource={uri}"/>\
        </XRD>
        """
    # dom = parseString(xml_str)
    return Response(content=data, media_type="application/xml")


@app.get("/.well-known/webfinger")
def webfinger_resource():
    content = {
        "subject": "acct:test@activity-pub-server.onrender.com",
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": "https://activity-pub-server.onrender.com/test",
            },
        ],
    }

    return JSONResponse(content=content)
