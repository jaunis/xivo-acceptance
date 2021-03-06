# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce.registry import world


EXTENSIONS_URL = 'extensions'


def all_extensions(parameters=None):
    parameters = parameters or {}
    return world.restapi_utils_1_1.rest_get(EXTENSIONS_URL, params=parameters)


def get_extension(extension_id):
    return world.restapi_utils_1_1.rest_get('%s/%s' % (EXTENSIONS_URL, extension_id))


def all_user_links_by_extension_id(extension_id):
    return world.restapi_utils_1_1.rest_get('%s/%s/user_links' % (EXTENSIONS_URL, extension_id))


def create_extension(parameters):
    return world.restapi_utils_1_1.rest_post(EXTENSIONS_URL, parameters)


def update(extension_id, parameters):
    return world.restapi_utils_1_1.rest_put('%s/%s' % (EXTENSIONS_URL, extension_id), parameters)


def delete_extension(extension_id):
    return world.restapi_utils_1_1.rest_delete('%s/%s' % (EXTENSIONS_URL, extension_id))
