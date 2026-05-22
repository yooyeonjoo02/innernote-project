from pydantic import BaseModel, EmailStr, Field


class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=100)
    nickname: str = Field(min_length=1, max_length=50)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    nickname: str

    class Config:
        from_attributes = True


class UserSignupResponse(BaseModel):
    message: str
    user: UserResponse


class UserLoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str