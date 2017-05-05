##
# readtime.py
#
# Created by Zander Otavka on 5/4/17.
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


from __future__ import division


def get_read_time_minutes(text):
    AVG_WPM = 450
    word_count = len(filter(lambda string: bool(string), text.split(" ")))
    return word_count / AVG_WPM
