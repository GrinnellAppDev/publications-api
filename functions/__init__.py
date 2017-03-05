##
# functions/__init__.py
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

import os
import sys

# directories to be exposed so the modules they contain can be imported
GLOBAL_DIRS = "shared", "lib", "lib/repoze"

# add each of GLOBAL_DIRS to sys.path
root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
sys.path.extend([os.path.join(root_dir, gdir) for gdir in GLOBAL_DIRS])

# now that imports are properly configured, we can import our code
from publications import publications_list  # nopep8
from articles import (articles_list, articles_get, articles_post,
                      articles_patch, articles_delete)  # nopep8
