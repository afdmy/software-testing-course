"""Stable result paths shared by API processes and Celery workers.

Historically the project used paths relative to the process working directory.
That produced ``<project>/results`` when a worker was started from the project
root and ``<project>/backend/results`` when it was started from ``backend``.
New jobs always use the backend directory, while readers keep supporting both
locations so existing results remain visible.
"""

from pathlib import Path
from typing import Iterable, Iterator, Optional, Tuple


BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
PRIMARY_RESULTS_ROOT = BACKEND_DIR / "results"
LEGACY_RESULTS_ROOT = PROJECT_ROOT / "results"
RESULTS_ROOTS = (PRIMARY_RESULTS_ROOT, LEGACY_RESULTS_ROOT)

RESULT_GROUPS = (
    "evaluation_results",
    "adversarial_results",
    "defense_results",
    "scenario_results",
    "airsim_results",
)


def result_path(group: str, task_id: Optional[str] = None) -> Path:
    """Return the canonical location used for all newly created results."""
    path = PRIMARY_RESULTS_ROOT / group
    return path / task_id if task_id else path


def iter_group_dirs() -> Iterator[Tuple[str, Path]]:
    """Yield readable result groups in both canonical and legacy locations."""
    for root in RESULTS_ROOTS:
        for group in RESULT_GROUPS:
            yield group, root / group


def find_task_dir(
    task_id: str, groups: Optional[Iterable[str]] = None
) -> Tuple[Optional[str], Optional[Path]]:
    """Find a task in the canonical directory first, then in the legacy one."""
    selected_groups = tuple(groups) if groups is not None else RESULT_GROUPS
    for root in RESULTS_ROOTS:
        for group in selected_groups:
            candidate = root / group / task_id
            if candidate.is_dir():
                return group, candidate
    return None, None
