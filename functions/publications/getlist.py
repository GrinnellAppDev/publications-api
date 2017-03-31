##
# publications/getlist.py
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

from response import create_json_response


def handler(event, context, db):
    assert event["httpMethod"] == "GET"

    query_params = event["queryStringParameters"]

    if query_params is not None and "pageToken" in query_params:
        page_key = {
            "id": {"S": str(uuid.UUID(
                bytes=base64.urlsafe_b64decode(str(query_params["pageToken"]))
            ))}
        }
    else:
        page_key = None

    if query_params is not None and "pageSize" in query_params:
        page_size = int(query_params["pageSize"])
    else:
        page_size = 30

    publications, next_page_key = db.publications.scan(page_key, page_size)

    response = {
        "items": publications,
    }

    if next_page_key is not None:
        response["nextPageToken"] = base64.urlsafe_b64encode(
            uuid.UUID(next_page_key["id"]["S"]).bytes
        )

    return create_json_response(200, body=response)
