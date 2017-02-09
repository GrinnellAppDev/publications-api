##
# response.py
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

import json


class HttpError(Exception):

    status_code = None

    def __init__(self, status_code, message):
        Exception.__init__(self, message)
        self.status_code = status_code

    def to_response(self):
        return create_raw_response(
            status_code=self.status_code,
            headers={
                "Content-Type": "text/plain",
                "Access-Control-Allow-Origin": "*",
            },
            body=self.message
        )


def create_json_response(status_code, headers={}, body={}):
    resp_headers = {
        "Content-Type": "application/json",

        # todo: maybe get more exclusive
        "Access-Control-Allow-Origin": "*",
    }

    resp_headers.update(headers)

    return create_raw_response(status_code, resp_headers, json.dumps(body))


def create_raw_response(status_code, headers={}, body=""):
    return {
        "statusCode": str(status_code),
        "headers": headers,
        "body": body
    }
