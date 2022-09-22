# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.consumer import BusConsumer as Consumer
from xivo_bus.publisher import BusPublisher as Publisher
from xivo_bus.resources.ami.event import AMIEvent
from xivo.status import Status


class BusConsumer(Consumer):
    @classmethod
    def from_config(cls, bus_config):
        name = 'wazo-agentd'
        return cls(name=name, **bus_config)

    def provide_status(self, status):
        status['bus_consumer']['status'] = (
            Status.ok if self.consumer_connected() else Status.fail
        )


class BusPublisher(Publisher):
    @classmethod
    def from_config(cls, service_uuid, bus_config):
        name = 'wazo-agentd'
        return cls(name=name, service_uuid=service_uuid, **bus_config)


class QueueMemberPausedEvent(AMIEvent):
    name = 'QueueMemberPause'
    routing_key = 'ami.{}'.format(name)
