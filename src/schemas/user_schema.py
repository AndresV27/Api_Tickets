from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    role_id: int | None = None

    class Config:
        from_atributes = True    

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

class UserRolerUpdate(BaseModel):
    role_id: int
