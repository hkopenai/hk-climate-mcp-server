"""Shared fixtures for live integration tests.

These tests hit the real Hong Kong Observatory open-data APIs. Running them
back-to-back without any throttle can trip the upstream rate-limiter and
produce spurious 502/429 errors. The `throttle` fixture below sleeps for a
short, configurable interval before each test so a full ``pytest live_tests``
run stays well below typical per-second request budgets.
"""

import os
import time
import pytest

# Default pause between live tests. Override with the LIVE_TEST_THROTTLE_S
# environment variable when running against APIs that need a longer cool-down.
# 1.5s is a safe default for the HKO endpoints used by this server.
DEFAULT_THROTTLE_SECONDS = float(os.environ.get("LIVE_TEST_THROTTLE_S", "1.5"))


@pytest.fixture(autouse=True)
def throttle():
    """Sleep DEFAULT_THROTTLE_SECONDS before every live test."""
    time.sleep(DEFAULT_THROTTLE_SECONDS)
