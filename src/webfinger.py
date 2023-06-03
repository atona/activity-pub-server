import re
from typing import Union

from fastapi import Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud
from .main import app, get_db
from .settings import get_settings

settings = get_settings()


@app.get("/.well-known/host-meta")
def webfinger_host_meta():
    data = (
        '<?xml version="1.0"?>\
        <XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">\
            <Link rel="lrdd" type="application/xrd+xml" template="'
        + settings.get_base_url()
        + '/.well-known/webfinger?resource={uri}"/>\
        </XRD>'
    )
    return Response(content=data, media_type="application/xml")


@app.get("/.well-known/webfinger")
def webfinger_resource(
    request: Request, resource: Union[str, None] = None, db: Session = Depends(get_db)
):
    print(request.base_url)
    print(resource)
    m = re.match("^acct:([a-zA-Z0-9_\-]+)@([a-zA-Z0-9_\-\.]+)", resource)
    subject, name, domain = m.group(0, 1, 2) if m else [None, None, None]
    user = crud.get_user_by_name(db, name=name)
    print(domain)
    print(settings.app_domain)
    print(settings.app_port)
    print(settings.app_protocol)
    print(settings.get_base_url())
    if domain != settings.app_domain or user is None:
        raise HTTPException(status_code=404, detail=f"Not Found.")
    content = {
        "subject": subject,
        "aliases": [
            f"{settings.get_base_url()}/@{name}",
            f"{settings.get_base_url()}/users/{name}",
        ],
        "links": [
            {
                "rel": "http://webfinger.net/rel/profile-page",
                "type": "text/html",
                "href": f"{settings.get_base_url()}/@{name}",
            },
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": f"{settings.get_base_url()}/users/{name}",
            },
            {
                "rel": "http://ostatus.org/schema/1.0/subscribe",
                "template": f"{settings.get_base_url()}/authorize_interaction?uri={{uri}}",
            },
        ],
    }

    return JSONResponse(content=content)
