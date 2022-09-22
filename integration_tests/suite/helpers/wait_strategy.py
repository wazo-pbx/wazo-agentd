# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests

from hamcrest import assert_that, has_entries

from wazo_test_helpers import until
from wazo_test_helpers.wait_strategy import WaitStrategy


class EverythingOkWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def is_ready():
            try:
                status = integration_test.agentd.status()
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'bus_consumer': has_entries(status='ok'),
                        # 'bus_publisher': has_entries(status='ok'),  # FIXME
                        'service_token': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)
