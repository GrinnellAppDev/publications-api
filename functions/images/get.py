##
# images/get.py
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

import base64
from response import create_raw_response, HttpError, create_json_response


def handler(event, context, bucket):
    # assert event["httpMethod"] == "GET"
    # return create_json_response(
    #     200,
    #     body=event  # image_data_str
    # )

    path_params = event["path"]  # event["pathParameters"]
    image_id = path_params["imageId"]
    filename = "/tmp/{}".format(image_id)

    bucket.download_file(image_id, filename)
    with open(filename, "rb") as image:
        image_data = image.read()
        image_b64 = base64.b64encode(image_data)
        print(type(image_data))
        print(image_data)

    # try:
    #     resource = bucket.get(image_id)
    # except bucket.ClientError as err:
    #     error_code = err.response["Error"]["Code"]
    #     if error_code == "NoSuchKey":
    #         raise HttpError(404, "No image with id {}".format(image_id))
    #     else:
    #         raise

    # stream = resource["Body"]
    # content_type = resource["ContentType"]
    # image_data = stream.read()
    # print(type(image_data))
    # print(image_data.decode)
    # # print(type(bytearray(image_data)))
    # # print("image data len = {}".format(len(image_data)))
    # print("bytes = {}".format(bytearray(image_data)))

    return image_b64
    # return create_raw_response(
    #     200,
    #     headers={
    #         "Content-Type": "image/jpeg"  # content_type
    #     },
    #     body=image_b64  # image_data_str
    # )
