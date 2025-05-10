from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50, default="holdenmcgroin")
    email: EmailStr = Field(
        min_length=5, max_length=100, default="holden.mcgroin@holden.xxx"
    )
    password: str = Field(min_length=8, max_length=100, default="hallo1234!")


class UserCreate(UserBase):
    user_id: str
    date_created: str
