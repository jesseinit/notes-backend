from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

import apps.users.users_schema as user_schemas
from apps.users import crud as UserDAL
from helpers.utils import HashManager, JWTBearer

router = APIRouter()


@router.post("/auth/register", status_code=201)
def register_user(payload: user_schemas.CreateUserInputSchema):
    user = UserDAL.get_existing_user(username=payload.username, email=payload.email)
    if user:
        return JSONResponse(
            content={"msg": "Username or Email has been taken", "data": None},
            status_code=409,
        )
    new_user = UserDAL.create_user(payload)
    return {
        "msg": "Signup Successful",
        "data": user_schemas.CreatedUserSchema.from_orm(new_user),
    }


@router.post("/auth/login", status_code=200)
def login_user(payload: user_schemas.UserLoginInputSchema):

    user = UserDAL.get_user_by_username(username=payload.username)
    if not user:
        return JSONResponse(
            content={"msg": "Invalid login credentials", "data": None},
            status_code=404,
        )

    is_valid_password = HashManager.verify_password(payload.password, user.password)
    if not is_valid_password:
        return JSONResponse(
            content={"msg": "Invalid login credentials", "data": None},
            status_code=400,
        )

    return {
        "msg": "Login Successful",
        "data": {
            "access_token": HashManager.encode_data(
                dict(id=str(user.id), username=user.username)
            )
        },
    }


@router.get("/me", status_code=200)
def user_profile(current_user: JWTBearer = Depends(JWTBearer())):
    return {
        "msg": "Profile Retrieved",
        "data": user_schemas.CreatedUserSchema.from_orm(current_user),
    }
