"""Process-local request budgets and allowlisted provider telemetry; no raw errors."""

from collections import Counter, deque
from threading import Lock
from time import monotonic

from openai import OpenAIError


def error_category(error):
    code = getattr(error, "code", None)
    status = getattr(error, "status_code", None)
    if code in {"credit_balance_exhausted", "insufficient_quota"}:
        return "quota_exhausted"
    if status in {401, 403}:
        return "authentication_or_access"
    if status == 429:
        return "provider_rate_limited"
    if isinstance(error, TimeoutError) or type(error).__name__ == "APITimeoutError":
        return "timeout"
    if isinstance(error, ValueError):
        return "invalid_output"
    if status is not None:
        return "provider_error"
    return "connection_error"


class ProviderMonitor:
    def __init__(self, settings, clock=monotonic):
        self.settings, self.clock = settings, clock
        self.lock = Lock()
        self.calls = deque()
        self.counts = {}

    def reserve(self, owner):
        with self.lock:
            now = self.clock()
            while self.calls and self.calls[0][0] <= now - 60:
                self.calls.popleft()
            own_count = sum(user == owner for _, user in self.calls)
            allowed = (
                len(self.calls) < self.settings.model_calls_per_minute
                and own_count < self.settings.model_user_calls_per_minute
            )
            if allowed:
                self.calls.append((now, owner))
            return allowed

    def record(self, owner, status):
        with self.lock:
            self.counts.setdefault(owner, Counter())[status] += 1

    def snapshot(self, owner):
        with self.lock:
            return {
                "counts_since_process_start": dict(self.counts.get(owner, {})),
                "own_calls_last_minute": sum(
                    user == owner and timestamp > self.clock() - 60 for timestamp, user in self.calls
                ),
                "scope": "Authenticated owner only; process-local counters reset on restart.",
            }


def run_selection(settings, request, candidates, selector, monitor, owner):
    started = monotonic()
    if not monitor.reserve(owner):
        status, selection = "local_rate_limited", None
    else:
        try:
            selection = selector(settings, request, candidates)
            status = "selected"
        except (OpenAIError, ValueError, OSError) as exc:
            status, selection = error_category(exc), None
    monitor.record(owner, status)
    return selection, status, round((monotonic() - started) * 1000)
