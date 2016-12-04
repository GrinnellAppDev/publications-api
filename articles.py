from __future__ import print_function, division

import boto3
import json
import uuid
import datetime
import decimal
from boto3.dynamodb.conditions import Key, Attr


class DecimalEncoder(json.JSONEncoder):
    """
    Helper class to convert from DynamoDb object to JSON.
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def create_response(status_code, headers={}, res=None, err=None):
    """
    Create a response event from status code and content or an error.
    """
    resp_headers = {
        "Content-Type": "application/json",
    }

    resp_headers.update(headers)

    return {
        "statusCode": str(status_code),
        "body": (
            err.message if err is not None
            else json.dumps(res) if res is not None
            else ""
        ),
        "headers": resp_headers
    }


def get(event, context):
    db = boto3.resource("dynamodb")
    articles_table = db.Table("Articles")
    publications_table = db.Table("Publications")

    item = json.loads(event["body"])
    path_params = event["pathParameters"]
    publication_id = path_params["publicationId"]
    article_id = path_params["articleId"]

    # todo: validate the item with to a schema

    publication_get = publications_table.get_item(
        Key={"id": article_id, "publication": publication_id},
        ProjectionExpression="id"
    )

    if "Item" not in publication_get:
        err = Exception("No publication with id: {}".format(publication_id))
        return create_response(404, err=err)

    articles_get = articles_table.get_item(
        Key={"id": article_id, "article": article_id}
    )

    if "Item" not in articles_get:
        err = Exception("No article with id: {}".format(article_id))
        return create_response(404, err=err)
    return articles_get


def post(event, context):
    """
    Handle a post request.

    Validate the content, create a UUID, and then write to the database.
    """
    assert event["httpMethod"] == "POST"

    db = boto3.resource("dynamodb")
    articles_table = db.Table("Articles")
    publications_table = db.Table("Publications")

    item = json.loads(event["body"])
    path_params = event["pathParameters"]
    publication_id = path_params["publicationId"]

    # todo: validate the item with to a schema

    publication_get = publications_table.get_item(
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

    articles_table.put_item(Item=item)

    return create_response(204, {"x-id": item_id})
