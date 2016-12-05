##
# articles/post.py
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

import json
import uuid
import datetime

from response import create_response


def handler(event, context, db):
    assert event["httpMethod"] == "POST"

    item = json.loads(event["body"])
    path_params = event["pathParameters"]
    publication_id = path_params["publicationId"]

    # todo: validate the item with to a schema

    publication_get = db.publications.get_item(
        Key={"id": publication_id},
        ProjectionExpression="id"
    )

    if "Item" not in publication_get:
        err = Exception("No publication with id: {}".format(publication_id))
        return create_response(404, err=err)

    item_id = str(uuid.uuid1())
    item["id"] = item_id
    item["publication"] = publication_id
    item["datePublished"] = str(datetime.date.today())

    db.articles.put_item(Item=item)

    assert event["path"][-1] != "/"

    headers = {
        "Location": "{}/{}".format(event["path"], item_id)
    }

    return create_response(201, headers, res=item)
