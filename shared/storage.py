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

import boto3
import botocore
from boto3.dynamodb import conditions


class Db(object):

    Key = conditions.Key
    Attr = conditions.Attr

    _resource = None
    _articles_table = None
    _publications_table = None
    _series_table = None

    def __init__(self):
        self._resource = boto3.resource("dynamodb")

    @property
    def publications(self):
        if self._publications_table is None:
            name = os.environ["PUBLICATIONS_TABLE_NAME"]
            self._publications_table = self._resource.Table(name)
        return self._publications_table

    @property
    def series(self):
        if self._series_table is None:
            name = os.environ["SERIES_TABLE_NAME"]
            self._series_table = self._resource.Table(name)
        return self._series_table

    @property
    def articles(self):
        if self._articles_table is None:
            name = os.environ["ARTICLES_TABLE_NAME"]
            self._articles_table = self._resource.Table(name)
        return self._articles_table


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
