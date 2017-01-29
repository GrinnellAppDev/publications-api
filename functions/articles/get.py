##
# articles/get.py
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


def handler(event, context, db):
    assert event["httpMethod"] == "GET"

    path_params = event["pathParameters"]
    publication_id = path_params["publicationId"]
    article_id = path_params["articleId"]

    publication_get = db.publications.get_item(
        Key={"id": publication_id},
        ProjectionExpression="id"
    )

    if "Item" not in publication_get:
        raise HttpError(404, "No publication with id: {}"
                        .format(publication_id))

    articles_get = db.articles.get_item(
        Key={"publication": publication_id, "id": article_id}
    )

    if "Item" not in articles_get:
        raise HttpError(404, "No article with id: {}".format(article_id))

    return create_json_response(200, body=articles_get["Item"])
