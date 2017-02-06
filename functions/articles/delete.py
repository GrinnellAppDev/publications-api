##
# articles/delete.py
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

from response import create_json_response, HttpError
from validate import validate_publication_id, InvalidArticleError


def handler(event, context, db):
    assert event["httpMethod"] == "DELETE"

    path_params = event["pathParameters"]
    publication_id = path_params["publicationId"]
    article_id = path_params["articleId"]

    validate_publication_id(publication_id, db)

    article_key = {"publication": publication_id, "id": article_id}
    articles_get = db.articles.get_item(Key=article_key)

    if "Item" not in articles_get:
        raise InvalidArticleError(article_id)

    db.articles.delete_item(Key=article_key)

    return create_json_response(200, body=articles_get["Item"])
