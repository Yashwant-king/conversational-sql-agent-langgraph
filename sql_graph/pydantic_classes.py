from pydantic import BaseModel, Field
from typing import Literal


class Verify_user_query(BaseModel):
    # approve: bool = Field(
    #     ...,
    #     description="Indicates whether the user query is related to SQL (True) or not (False).",
    # )
    question_type: Literal["related_to_given_schema", "not_related_to_given_schema"] = Field(
        ...,
        description="Find out the given user question is related to the given database schema or not. If it is related to the given schema, return 'related_to_given_schema'. If it is not related to the given schema but is related to SQL, if user question is related to sql but not related to given schema, return 'not_related_to_given_schema'.",
    )
