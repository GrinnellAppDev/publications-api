"""
Validates Requests
"""

from jsonschema import validate
import boto3


class InvalidPublicationError(Exception):
  def __init__(self,publication_id):
    super(InvalidPublicationError,self).__init__("No publication with id: {}".format(publication_id))

def validate_publication_id():
  publication_get = publications_table.get_item(
    Key={"id": publication_id},
    ProjectionExpression="id"
  )
  if "Item" not in publication_get:
    raise InvalidPublicationError

def validate_request(event, context):
  """
  Handle a post request.

  Validate the content, create a UUID, and then write to the database.
  """
  pass
