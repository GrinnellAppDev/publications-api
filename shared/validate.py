##
# validate.py
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

"""
Validate requests with json schema.
"""

from jsonschema import validate
import boto3

from response import HttpError


class InvalidPublicationError(HttpError):
    def __init__(self, publication_id):
        HttpError.__init__(
            self, 404, "No publication with id: {}".format(publication_id)
        )


class InvalidArticleError(HttpError):
    def __init__(self, article_id):
        HttpError.__init__(
            self, 404, "No article with id: {}".format(article_id)
        )


def validate_publication_id(pub_id, db):
    get = db.publications.get_item(
        Key={"id": pub_id},
        ProjectionExpression="id"
    )

    if "Item" not in get:
        raise InvalidPublicationError(pub_id)


def validate_request(event, context):
    """
    Handle a post request.

    Validate the content, create a UUID, and then write to the database.
    """
    pass
