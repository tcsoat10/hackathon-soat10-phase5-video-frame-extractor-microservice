from pydantic import BaseModel, ConfigDict

class RegisterVideoConfigDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    
    delete_after_processing: bool
