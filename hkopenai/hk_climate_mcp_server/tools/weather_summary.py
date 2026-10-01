"""
Aggregated Weather Summary Tool - Returns multiple HKO weather data
sections in a single MCP call by fanning out to several endpoints
in parallel.

The Hong Kong Observatory exposes ~10 distinct open-data endpoints
(current observations, local forecast, 9-day forecast, warnings,
warning details, hourly tides, visibility, lightning, radiation,
special tips). Each existing tool in this package wraps exactly one
endpoint. An agent that needs "everything right now" therefore has
to make 9+ sequential `tools/call` round-trips, which is slow and
brittle: one failing endpoint kills the rest of the call.

This module adds a single `get_weather_summary` tool that fetches
all sections concurrently via `asyncio.gather` and returns one
consolidated dict. Partial failures are reported per-section as
`{"error": ...}` so a slow `radiation` endpoint never blocks the
rest of the response.

The aggregator reuses the existing per-section private functions
rather than re-implementing the HTTP calls, so URL paths, language
codes, validation logic, and station dictionaries stay in one
place. Adding a new section is a one-line edit to the `_SECTIONS`
list below.
"""

import asyncio
from datetime import date
from typing import Any, Awaitable, Callable, Dict, List, Tuple

from fastmcp import FastMCP

from . import current_weather, forecast, tides, warnings


def _build_sections(lang: str) -> List[Tuple[str, Callable[[], Dict[str, Any]]]]:
    today = date.today()
    return [
        (
            "current",
            lambda: current_weather._get_current_weather(
                region="Hong Kong Observatory", lang=lang
            ),
        ),
        ("local_forecast", lambda: forecast._get_local_weather_forecast(lang=lang)),
        ("nine_day", lambda: forecast._get_9_day_weather_forecast(lang=lang)),
        ("warnings", lambda: warnings._get_weather_warning_summary(lang=lang)),
        ("warning_info", lambda: warnings._get_weather_warning_info(lang=lang)),
        (
            "tides",
            lambda: tides._get_hourly_tides(
                station="QUB",  # Quarry Bay — central HK reference station
                year=today.year,
                month=today.month,
                day=today.day,
                lang=lang,
            ),
        ),
    ]


async def _run_section(
    name: str, fn: Callable[[], Dict[str, Any]]
) -> Tuple[str, Dict[str, Any]]:
    """Run one sync section helper in the default executor, catching all errors."""
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(None, fn)
        return name, result
    except Exception as exc:  # noqa: BLE001 - we deliberately swallow per-section failures
        return name, {"error": f"{type(exc).__name__}: {exc}"}


async def _aggregate(lang: str) -> Dict[str, Any]:
    sections = _build_sections(lang)
    tasks: List[Awaitable[Tuple[str, Dict[str, Any]]]] = [
        _run_section(name, fn) for name, fn in sections
    ]
    results = await asyncio.gather(*tasks)
    payload: Dict[str, Any] = dict(results)
    payload["_meta"] = {
        "lang": lang,
        "sections": [name for name, _ in sections],
        "generated_at": date.today().isoformat(),
    }
    return payload


def register(mcp: FastMCP) -> None:
    """Register the aggregated weather summary tool with the FastMCP server."""

    @mcp.tool(
        description=(
            "Get aggregated Hong Kong weather in one call: current observations, "
            "local and 9-day forecast, active warnings, warning details, and "
            "today's hourly tides for Quarry Bay. Internally fans out to "
            "multiple HKO endpoints concurrently; per-section failures are "
            "reported as {\"error\": \"...\"} rather than failing the whole call."
        ),
    )
    async def get_weather_summary(lang: str = "en") -> Dict[str, Any]:
        """
        Aggregated Hong Kong weather summary.

        Args:
            lang: Language code (en/tc/sc, default: en).

        Returns:
            Dict with one key per section plus a `_meta` key listing the
            sections fetched and the response generation date. Each section
            value is either the underlying tool's payload or an `{"error": ...}`
            if that section's HKO endpoint failed.
        """
        return await _aggregate(lang)
