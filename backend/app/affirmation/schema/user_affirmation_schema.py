from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import Field
import uuid
from datetime import datetime, time as dt_time

class AffirmationOptIn(BaseModel):
    affirmation_schedule: Optional[dt_time] = Field(default_factory=lambda: datetime.now().time())
class AffirmationSettingsBase(BaseModel):
    affirmation_opted: bool = Field(default=False)
    affirmation_schedule: Optional[dt_time] = Field(default_factory=lambda: datetime.now().time())

class AffirmationSettingsUpdate(AffirmationSettingsBase):
    pass
class AffirmationSettingsPublic(AffirmationSettingsBase) :
    pass 

