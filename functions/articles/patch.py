##
# articles/patch.py
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
from validate import (validate_publication_id, deep_empty_string_clean,
                      InvalidArticleError)
from readtime import get_read_time_minutes


def handler(event, context, db):
    assert event["httpMethod"] == "PATCH"

    new_fields = json.loads(event["body"])
    path_params = event["pathParameters"]
    publication_id = path_params["publicationId"]
    article_id = path_params["articleId"]

    # todo: validate the updates with a schema, make some fields immutable

    validate_publication_id(publication_id, db)

    deep_empty_string_clean(new_fields)

    article = db.articles.get({
        "publication": publication_id,
        "id": article_id,
    })

    if article is None:
        raise InvalidArticleError(article_id)

    read_time = get_read_time_minutes(new_fields["content"])
    new_fields["readTimeMinutes"] = read_time

    article.update(new_fields)
    db.articles.put(article)

    assert event["path"][-1] != "/"

    return create_json_response(200, body=article)
