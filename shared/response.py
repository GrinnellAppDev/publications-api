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
