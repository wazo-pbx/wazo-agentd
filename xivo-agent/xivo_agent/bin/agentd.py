# -*- coding: UTF-8 -*-

# Copyright (C) 2012-2013  Avencall
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

import argparse
import logging
import signal
from contextlib import contextmanager
from xivo import daemonize
from xivo_agent import ami
from xivo_agent.ctl.server import AgentServer
from xivo_agent.db_manager import DBManager
from xivo_agent.queuelog import QueueLogManager
from xivo_agent.service.service import AgentService
from xivo_agent.service.factory import StepFactory
from xivo_dao import agent_dao
from xivo_dao import agent_status_dao
from xivo_dao import line_dao
from xivo_dao import queue_dao
from xivo_dao import queue_log_dao
from xivo_dao import queue_member_dao

_LOG_FILENAME = '/var/log/xivo-agentd.log'
_PID_FILENAME = '/var/run/xivo-agentd.pid'

logger = logging.getLogger(__name__)


def main():
    parsed_args = _parse_args()

    _init_logging(parsed_args)

    if not parsed_args.foreground:
        daemonize.daemonize()

    logger.info('Starting xivo-agentd')
    daemonize.lock_pidfile_or_die(_PID_FILENAME)
    try:
        _run()
    finally:
        logger.info('Stopping xivo-agentd')
        daemonize.unlock_pidfile(_PID_FILENAME)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--foreground', action='store_true',
                        help='run in foreground')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase verbosity')
    return parser.parse_args()


def _init_logging(parsed_args):
    level = logging.DEBUG if parsed_args.verbose else logging.INFO
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    if parsed_args.foreground:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s (%(levelname)s): %(message)s'))
    else:
        handler = logging.FileHandler(_LOG_FILENAME)
        handler.setFormatter(logging.Formatter('%(asctime)s [%(process)d] (%(levelname)s): %(message)s'))
    root_logger.addHandler(handler)


def _run():
    _init_signal()
    db_manager = DBManager()
    db_manager.connect()
    with _new_ami_client() as ami_client:
        with _new_agent_server(db_manager) as agent_server:
            queue_log_manager = QueueLogManager(queue_log_dao)

            step_factory = StepFactory(ami_client, queue_log_manager, agent_login_dao,
                                       agent_dao, line_dao, queue_dao, queue_member_dao)

            agent_service = AgentService(agent_server)
            agent_service.init(step_factory)
            agent_service.run()


def _init_signal():
    signal.signal(signal.SIGTERM, _handle_sigterm)


def _handle_sigterm(signum, frame):
    raise SystemExit()


@contextmanager
def _new_ami_client():
    ami_client = ami.new_client('localhost', 'xivo_agent', 'die0Ahn8tae')
    try:
        yield ami_client
    finally:
        ami_client.close()


@contextmanager
def _new_agent_server(db_manager):
    agent_server = AgentServer(db_manager)
    try:
        yield agent_server
    finally:
        agent_server.close()


if __name__ == '__main__':
    main()
