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

from xivo_lettuce.remote_py_cmd import remote_exec

def create_profile(profile):
    remote_exec(_create_profile, profileinfo=profile)

def _create_profile(channel, profileinfo):
    from xivo_dao.helpers.db_manager import AsteriskSession
    from xivo_dao.alchemy.cti_profile import CtiProfile
    from xivo_dao.alchemy.ctipresences import CtiPresences
    from xivo_dao.alchemy.ctiphonehints import CtiPhoneHints
    from xivo_dao.alchemy.ctiphonehintsgroup import CtiPhoneHintsGroup

    profile = CtiProfile(**profileinfo)
#     if(profile.presence_id is None):
#         profile.presence_id = 1
    session = AsteriskSession()
    session.begin()
    session.execute('DELETE FROM cti_profile WHERE id = :profile_id', {'profile_id': int(profile.id)})
    session.add(profile)
    session.commit()
