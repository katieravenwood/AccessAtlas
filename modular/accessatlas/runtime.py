"""Runtime context shared by AccessAtlas entry points."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd


SectionGuidanceRenderer = Callable[[str], None]


@dataclass(frozen=True)
class RuntimeContext:
    """Resolved identity, scope, and optional runtime-specific UI behavior."""

    current_user: pd.Series
    visible_tabs: list[str]
    users: pd.DataFrame
    systems: pd.DataFrame
    access: pd.DataFrame
    system_admins: pd.DataFrame
    runtime_name: str
    is_demo: bool = False
    section_guidance_renderer: SectionGuidanceRenderer | None = None
