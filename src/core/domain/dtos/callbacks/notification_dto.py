from typing import Optional, Union
from pydantic import BaseModel

class NotificationDTO(BaseModel):
    job_ref: str
    status: str
    service: str
    timestamp: str
    detail: Optional[Union[str, None]] = None
    zip_url: Optional[Union[str, None]] = None
