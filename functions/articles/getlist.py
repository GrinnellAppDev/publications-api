##
# articles/getlist.py
#
# Copyright (C) 2016  Grinnell AppDev.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from __future__ import print_function, division

import base64
import uuid
import struct

from response import create_json_response
from validate import validate_publication_id


def handler(event, context, db):
    assert event["httpMethod"] == "GET"

    path_params = event["pathParameters"]
    publication_id = path_params["publicationId"]

    query_params = event["queryStringParameters"]

    PAGE_TOKEN_STRUCT_FORMAT = ">16sQ"
    if query_params is not None and "pageToken" in query_params:
        page_key_id, page_key_date = struct.unpack(
            PAGE_TOKEN_STRUCT_FORMAT,
            base64.urlsafe_b64decode(str(query_params["pageToken"]))
        )

        page_key = {
            "publication": {"S": publication_id},
            "id": {"S": str(uuid.UUID(bytes=page_key_id))},
            "datePublished": {"N": str(page_key_date)},
        }
    else:
        page_key = None

    if query_params is not None and "pageSize" in query_params:
        page_size = int(query_params["pageSize"])
    else:
        page_size = 30

    validate_publication_id(publication_id, db)

    articles, next_page_key = db.articles.query(
        page_key, page_size,
        db.Key("publication").eq(publication_id),
        index=db.SHORT_ARTICLES_BY_DATE_INDEX,
        reverse=True
    )

    response = {
        "items": articles,
    }

    if next_page_key is not None:
        response["nextPageToken"] = base64.urlsafe_b64encode(struct.pack(
            PAGE_TOKEN_STRUCT_FORMAT,
            uuid.UUID(next_page_key["id"]["S"]).bytes,
            int(next_page_key["datePublished"]["N"])
        ))

    return create_json_response(200, body=response)
