from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    name: str
    description: str
