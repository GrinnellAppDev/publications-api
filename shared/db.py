##
# db.py
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
Abstracts away boto3 database for easier of unit testing later.

We can easily make a dummy db for unit tests if all code uses this interface.
"""

from __future__ import print_function, division

import boto3

from boto3.dynamodb.conditions import Key, Attr


class Db(object):

    _resource = None
    _articles_table = None
    _publications_table = None

    def __init__(self):
        self._resource = boto3.resource("dynamodb")

    @property
    def articles(self):
        if self._articles_table is None:
            name = "publications_articles"
            self._articles_table = self._resource.Table(name)
        return self._articles_table

    @property
    def publications(self):
        if self._publications_table is None:
            name = "publications_publications"
            self._publications_table = self._resource.Table(name)
        return self._publications_table
