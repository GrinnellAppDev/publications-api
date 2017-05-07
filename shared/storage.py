##
# storage.py
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
Abstracts away boto3 resources for easier of unit testing later.

We can easily make a dummy db and bucket for unit tests if all code uses this
interface.
"""

from __future__ import print_function, division

import os
import json

from lru import lru_cache
import boto3
import botocore
from boto3.dynamodb import conditions


def _to_attribute(obj):
    if type(obj) in (str, unicode):
        return {"S": obj}
    if type(obj) in (int, float):
        return {"N": str(obj)}
    if type(obj) == list:
        return {"L": [_to_attribute(item) for item in obj]}
    if type(obj) == dict:
        attrs = {}
        for name, value in obj.iteritems():
            attrs[name] = _to_attribute(value)
        return {"M": attrs}

    # We haven't implemented all supported attribute types yet
    raise NotImplementedError("Cannot handle {}".format(type(obj)))


def _to_attribute_dict(dictionary):
    assert type(dictionary) == dict
    return _to_attribute(dictionary)["M"]


def _from_attribute(attribute):
    if "S" in attribute:
        return attribute["S"]
    if "N" in attribute:
        try:
            return int(attribute["N"])
        except ValueError:
            return float(attribute["N"])
    if "L" in attribute:
        return [_from_attribute(item) for item in attribute["L"]]
    if "M" in attribute:
        dictionary = {}
        for name, value in attribute["M"].iteritems():
            dictionary[name] = _from_attribute(value)
        return dictionary

    # We haven't implemented all supported attribute types yet
    raise NotImplementedError("Cannot handle {}".format(attribute))


def _from_attribute_dict(attrs):
    assert type(attrs) == dict
    return _from_attribute({"M": attrs})


def _paginated_response(response):
    try:
        items = [_from_attribute_dict(item) for item in response["Items"]]
    except KeyError:
        items = []

    try:
        next_page_key = response["LastEvaluatedKey"]
    except KeyError:
        next_page_key = None

    return items, next_page_key


class Table(object):

    _client = None
    _name = None

    def __init__(self, client, name):
        self._client = client
        self._name = name

    @property
    @lru_cache(1)
    def _query_paginator(self):
        return self._client.get_paginator("query")

    @property
    @lru_cache(1)
    def _scan_paginator(self):
        return self._client.get_paginator("scan")

    def get(self, key):
        response = self._client.get_item(
            TableName=self._name,
            Key=_to_attribute_dict(key),
        )

        try:
            return _from_attribute_dict(response["Item"])
        except KeyError:
            return None

    def query(self, page_key, page_size, key_query, index=None, reverse=False):
        builder = conditions.ConditionExpressionBuilder()
        expr, names, values = builder.build_expression(key_query, True)
        scan_forward = not reverse

        params = dict(
            TableName=self._name,
            KeyConditionExpression=expr,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=_to_attribute_dict(values),
            Limit=page_size,
            ScanIndexForward=scan_forward,
        )

        if index is not None:
            params.update(dict(
                IndexName=index,
                Select="ALL_PROJECTED_ATTRIBUTES",
            ))

        if page_key is not None:
            params.update(dict(
                ExclusiveStartKey=page_key,
            ))

        return _paginated_response(self._client.query(**params))

    def scan(self, page_key, page_size):
        params = dict(
            TableName=self._name,
            Limit=page_size,
        )

        if page_key is not None:
            params.update(dict(
                ExclusiveStartKey=page_key,
            ))

        return _paginated_response(self._client.scan(**params))

    def put(self, item):
        self._client.put_item(
            TableName=self._name,
            Item=_to_attribute_dict(item),
        )

    def delete(self, key):
        self._client.delete_item(
            TableName=self._name,
            Key=_to_attribute_dict(key),
        )


class Db(object):

    Key = conditions.Key
    Attr = conditions.Attr

    SHORT_ARTICLES_BY_DATE_INDEX = "ShortArticlesByDate"

    @classmethod
    @lru_cache(1)
    def get_instance(cls):
        return cls()

    @property
    @lru_cache(1)
    def _client(self):
        return boto3.client("dynamodb")

    @property
    @lru_cache(1)
    def publications(self):
        return Table(self._client, os.environ["PUBLICATIONS_TABLE_NAME"])

    @property
    @lru_cache(1)
    def series(self):
        return Table(self._client, os.environ["SERIES_TABLE_NAME"])

    @property
    @lru_cache(1)
    def articles(self):
        return Table(self._client, os.environ["ARTICLES_TABLE_NAME"])


class SimpleStorage(object):

    _resource = None
    _images_bucket = None

    def __init__(self):
        self._resource = boto3.resource("s3")

    @property
    def images(self):
        if self._images_bucket is None:
            name = os.environ["IMAGES_BUCKET_NAME"]
            self._images_bucket = self._resource.Bucket(name)
        return self._images_bucket


class Bucket(object):

    ClientError = botocore.exceptions.ClientError

    IMAGES_BUCKET_NAME = os.environ["IMAGES_BUCKET_NAME"]

    _client = None
    _bucket_name = None

    def __init__(self, bucket_name):
        self._client = boto3.client("s3")
        self._bucket_name = bucket_name

    def get(self, Key, **kwargs):
        return self._client.get_object(
            Bucket=self._bucket_name,
            Key=Key,
            **kwargs
        )

    def put(self, Key, **kwargs):
        return self._client.put_object(
            Bucket=self._bucket_name,
            Key=Key,
            **kwargs
        )

    def delete(self, Key, **kwargs):
        return self._client.delete_object(
            Bucket=self._bucket_name,
            Key=Key,
            **kwargs
        )
