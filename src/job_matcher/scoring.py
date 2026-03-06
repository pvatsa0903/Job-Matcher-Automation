from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class SignalScore:
    signal: str
    weight: float
    matched_phrases: tuple[str, ...]


@dataclass(frozen=True)
class ScoreBreakdown:
    total_score: float
    matched_signals: tuple[SignalScore, ...]


SIGNAL_WEIGHTS: dict[str, float] = {
    "scale_30m_plus": 3.2,
    "growth": 2.8,
    "monetization": 2.8,
    "retention": 2.6,
    "lifecycle_crm": 2.6,
    "experimentation": 2.5,
    "b2b_b2c_saas": 2.4,
    "incentives": 2.2,
    "gamification": 2.2,
}

SIGNAL_PATTERNS: dict[str, tuple[re.Pattern[str], ...]] = {
    "growth": (
        re.compile(r"\bgrowth\b", re.IGNORECASE),
        re.compile(r"\bgrowth[- ]?marketing\b", re.IGNORECASE),
        re.compile(r"\buser acquisition\b", re.IGNORECASE),
    ),
    "monetization": (
        re.compile(r"\bmoneti[sz]ation\b", re.IGNORECASE),
        re.compile(r"\brevenue optimization\b", re.IGNORECASE),
        re.compile(r"\bpricing strategy\b", re.IGNORECASE),
    ),
    "retention": (
        re.compile(r"\bretention\b", re.IGNORECASE),
        re.compile(r"\bchurn\b", re.IGNORECASE),
        re.compile(r"\bengagement lift\b", re.IGNORECASE),
    ),
    "lifecycle_crm": (
        re.compile(r"\blifecycle\b", re.IGNORECASE),
        re.compile(r"\bcrm\b", re.IGNORECASE),
        re.compile(r"\bemail journey\b", re.IGNORECASE),
        re.compile(r"\blifecycle marketing\b", re.IGNORECASE),
    ),
    "experimentation": (
        re.compile(r"\bexperimentation\b", re.IGNORECASE),
        re.compile(r"\ba/?b testing\b", re.IGNORECASE),
        re.compile(r"\bmultivariate testing\b", re.IGNORECASE),
        re.compile(r"\bexperiment design\b", re.IGNORECASE),
    ),
    "b2b_b2c_saas": (
        re.compile(r"\bb2b\b", re.IGNORECASE),
        re.compile(r"\bb2c\b", re.IGNORECASE),
        re.compile(r"\bsaas\b", re.IGNORECASE),
        re.compile(r"\bsubscription business\b", re.IGNORECASE),
    ),
    "scale_30m_plus": (
        re.compile(r"\b3\d\s?m\+?\b", re.IGNORECASE),
        re.compile(r"\b[3-9]\d\s?million\b", re.IGNORECASE),
        re.compile(r"\b\d{2,3}\s?mau\b", re.IGNORECASE),
        re.compile(r"\b\d{2,3}\s?million (users|customers|monthly users)\b", re.IGNORECASE),
    ),
    "incentives": (
        re.compile(r"\bincentive(s)?\b", re.IGNORECASE),
        re.compile(r"\brewards?\b", re.IGNORECASE),
        re.compile(r"\bloyalty program\b", re.IGNORECASE),
    ),
    "gamification": (
        re.compile(r"\bgamification\b", re.IGNORECASE),
        re.compile(r"\bgame[- ]?mechanic(s)?\b", re.IGNORECASE),
        re.compile(r"\bpoints? and badges?\b", re.IGNORECASE),
    ),
}


def _collect_text(parts: Iterable[Any]) -> str:
    return " ".join(str(p) for p in parts if p).strip()


def score_text(text: str) -> ScoreBreakdown:
    matched: list[SignalScore] = []
    total = 0.0

    for signal, patterns in SIGNAL_PATTERNS.items():
        hits: list[str] = []
        for pattern in patterns:
            if pattern.search(text):
                hits.append(pattern.pattern)
        if not hits:
            continue
        weight = SIGNAL_WEIGHTS[signal]
        total += weight
        matched.append(SignalScore(signal=signal, weight=weight, matched_phrases=tuple(hits)))

    return ScoreBreakdown(total_score=round(total, 3), matched_signals=tuple(matched))


def score_job(job: dict[str, Any]) -> ScoreBreakdown:
    text = _collect_text(
        (
            job.get("title"),
            job.get("description"),
            job.get("summary"),
            job.get("team"),
            " ".join(job.get("tags", [])) if isinstance(job.get("tags"), list) else None,
        )
    )
    return score_text(text)
