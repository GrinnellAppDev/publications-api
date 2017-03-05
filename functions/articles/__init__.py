##
# articles/__init__.py
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

from storage import Db
from response import HttpError

import getlist
import get
import post
import patch
import delete


def articles_list(event, context):
    try:
        return getlist.handler(event, context, Db.get_instance())
    except HttpError as err:
        return err.to_response()


def articles_get(event, context):
    try:
        return get.handler(event, context, Db.get_instance())
    except HttpError as err:
        return err.to_response()


def articles_post(event, context):
    try:
        return post.handler(event, context, Db.get_instance())
    except HttpError as err:
        return err.to_response()


def articles_patch(event, context):
    try:
        return patch.handler(event, context, Db.get_instance())
    except HttpError as err:
        return err.to_response()


def articles_delete(event, context):
    try:
        return delete.handler(event, context, Db.get_instance())
    except HttpError as err:
        return err.to_response()
