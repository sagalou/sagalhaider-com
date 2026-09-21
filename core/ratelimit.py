"""
Lightweight rate limiting backed by Redis (NoSQL, key-value store).

This is the project's concrete CP6 "NoSQL data access" component: the
relational data (Realisation, ServiceRequest, RequestStep, ChatbotRule...)
lives in SQL via the Django ORM, while short-lived request counters used
purely for abuse protection live in Redis, accessed directly through
Django's cache API (django-redis), which maps onto Redis INCR/EXPIRE.

No ORM involved here on purpose: this *is* the NoSQL access path.
"""

import time

from django.core.cache import caches


def is_rate_limited(key: str, limit: int, window_seconds: int) -> bool:
    """
    Return True if `key` has been hit more than `limit` times within the
    last `window_seconds`, and record this hit.

    Uses a simple fixed-window counter in Redis: INCR + EXPIRE-on-first-hit.
    """
    cache = caches["ratelimit"]
    now_bucket = int(time.time() // window_seconds)
    redis_key = f"ratelimit:{key}:{now_bucket}"

    try:
        count = cache.incr(redis_key)
    except ValueError:
        # Key doesn't exist yet
        cache.set(redis_key, 1, timeout=window_seconds)
        count = 1

    return count > limit


def client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def parse_rate(rate: str) -> tuple[int, int]:
    """Parse a "N/h" or "N/m" style rate string into (limit, window_seconds)."""
    count, _, period = rate.partition("/")
    windows = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return int(count), windows.get(period, 3600)
