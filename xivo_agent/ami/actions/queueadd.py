# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

from xivo_agent.ami.actions.common.action import BaseAction


def QueueAddAction(queue, interface, member_name=None, state_interface=None, penalty=None, skills=None):
    return BaseAction('QueueAdd', [
        ('Queue', queue),
        ('Interface', interface),
        ('MemberName', member_name),
        ('StateInterface', state_interface),
        ('Penalty', penalty),
        ('Skills', skills),
    ])