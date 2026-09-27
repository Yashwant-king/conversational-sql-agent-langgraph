from pydantic import BaseModel, Field



class Verify_user_query(BaseModel):
    approve: bool = Field(
        ...,
        description="Indicates whether the user query is related to SQL (True) or not (False).",
    )