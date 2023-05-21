from xml.dom.minidom import parseString

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def person():
    content = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Person",
        "id": "https://example.com/test",  # Fediverseで一意
        "name": "test",  # 表示名
        "preferredUsername": "test",  # ユーザID
        "summary": "my simple activitypub",  # 概要
        "inbox": "https://example.com/inbox",  # このユーザへの宛先
        "outbox": "https://example.com/outbox",  # このユーザの発信元
        "url": "https://example.com/test",  # プロフィールページのURL
        "icon": {
            "type": "Image",
            "mediaType": "image/png",  # mime type
            "url": "https://example.com/icon.ong",  # アイコン画像のURL
        },
    }
    headers = {"Content-Type": "application/activity+json"}
    return JSONResponse(content=content, headers=headers)


@app.get("/.well-known/host-meta")
async def webfinger_host_meta():
    data = """<?xml version="1.0"?>
        <XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">
            <Link rel="lrdd" type="application/xrd+xml" template="https://example.com/.well-known/webfinger?resource={uri}"/>\
        </XRD>
        """
    # dom = parseString(xml_str)
    return Response(content=data, media_type="application/xml")


@app.get("/.well-known/webfinger")
async def webfinger_resource():
    content = {
        "subject": "acct:test@example.com",
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": "https://example.com/test",
            },
        ],
    }

    return JSONResponse(content=content)
