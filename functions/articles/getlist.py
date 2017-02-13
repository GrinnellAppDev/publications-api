##
# articles/getlist.py
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

from response import create_json_response


def handler(event, context, db):
    assert event["httpMethod"] == "GET"

    articles_get = db.articles.scan()  # warning naieve hack, doesn't work for
                                       # multiple publications

    if "Items" in articles_get:
        articles_list = articles_get["Items"]
    else:
        articles_list = []

    return create_json_response(200, body=articles_list)