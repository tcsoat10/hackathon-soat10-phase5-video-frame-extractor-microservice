from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class StorageConfig:
    provider: Optional[str] = None
    endpoint_url: Optional[str] = None
    region_name: Optional[str] = None
    monitoring_url: Optional[str] = None

    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    project_id: Optional[str] = None
    bucket_name: Optional[str] = None

    max_attempts: int = 3
    retry_attempts: int = 4
    retry_multiplier: float = 1.0
    retry_min: int = 1
    retry_max: int = 60

    extra: Optional[Dict[str, Any]] = None


__all__ = ["StorageConfig"]
