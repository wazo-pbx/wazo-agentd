# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from xivo import debug
from xivo_dao.helpers import db_utils

logger = logging.getLogger(__name__)


class LoginHandler:

    def __init__(self, login_manager, agent_dao):
        self._login_manager = login_manager
        self._agent_dao = agent_dao

    @debug.trace_duration
    def handle_login_by_id(self, agent_id, extension, context, tenant_uuids=None):
        logger.info('Executing login command (ID %s) on %s@%s', agent_id, extension, context)
        with db_utils.session_scope():
            agent = self._agent_dao.get_agent(agent_id, tenant_uuids=tenant_uuids)
        self._handle_login(agent, extension, context)

    @debug.trace_duration
    def handle_login_by_number(self, agent_number, extension, context, tenant_uuids=None):
        logger.info('Executing login command (number %s) on %s@%s', agent_number, extension, context)
        with db_utils.session_scope():
            agent = self._agent_dao.get_agent_by_number(agent_number, tenant_uuids=tenant_uuids)
        self._handle_login(agent, extension, context)

    def _handle_login(self, agent, extension, context):
        self._login_manager.login_agent(agent, extension, context)
