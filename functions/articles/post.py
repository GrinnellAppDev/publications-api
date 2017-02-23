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

from response import create_json_response, HttpError
from validate import validate_publication_id, deep_empty_string_clean


def handler(event, context, db):
    assert event["httpMethod"] == "POST"

    article = json.loads(event["body"])
    path_params = event["pathParameters"]
    publication_id = path_params["publicationId"]

    # todo: validate the article with a schema

    validate_publication_id(publication_id, db)

    deep_empty_string_clean(article)

    article_id = str(uuid.uuid1())
    article["id"] = article_id
    article["publication"] = publication_id
    article["datePublished"] = str(datetime.datetime.utcnow())

    db.articles.put_item(Item=article)

    assert event["path"][-1] != "/"

    headers = {
        "Location": "{}/{}".format(event["path"], article_id)
    }

    return create_json_response(201, headers, body=article)
