"""Shared fixtures for live integration tests.

These tests hit the real Hong Kong Observatory open-data APIs. Running them
back-to-back without any throttle can trip the upstream rate-limiter and
produce spurious 502/429 errors. The `throttle` fixture below sleeps for a
short, configurable interval before each test so a full ``pytest live_tests``
run stays well below typical per-second request budgets.

In addition to throttling, the `pytest_collection_modifyitems` hook below
auto-applies the `@pytest.mark.live` marker to every test collected from
this directory. That lets the CI workflow run `pytest -m "not live"` to
skip these slow, network-dependent tests without having to add the marker
to every test file by hand.
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


def pytest_collection_modifyitems(config, items):
    """Auto-apply @pytest.mark.live to every test in live_tests/.

    Lets the CI workflow deselect these tests with `-m "not live"`
    without requiring every test file to import and apply the marker
    manually. Mirrors the same hook in hk-finance-mcp-server's
    live_tests/conftest.py.
    """
    live_marker = pytest.mark.live
    for item in items:
        # Restrict to tests in the live_tests package. Item.fspath is the
        # absolute path of the test file; matching the path component is
        # robust against working-directory differences in CI runners.
        if "live_tests" in str(item.fspath):
            item.add_marker(live_marker)