from fastapi import APIRouter, Depends, HTTPException, UploadFile, Request
from fastapi.params import File
from slowapi import Limiter

from clients.cloudinary_client import CloudinaryClient
from clients.fast_api_mail_client import FastApiMailClient
from repositories.user_repository import UserRepository
from schemas.users import UserOut
from services.auth_service import AuthService
from services.user_service import UserService

limiter = Limiter(
    key_func=lambda request: f"user-{getattr(request.state, 'user_id', 'anonymous')}",
    storage_uri="redis://redis:6379"
)

router = APIRouter(prefix="/users", tags=["users"])

user_repository = UserRepository()
email_client = FastApiMailClient()
image_client = CloudinaryClient()
auth_service = AuthService(user_repository=user_repository, email_sender=email_client)
user_service = UserService(user_repository=user_repository, image_client=image_client)


@router.get(
    "/me",
    response_model=UserOut,
)
@limiter.limit("5/minute")
async def get_current_user_info(
        request: Request,
        current_user: UserOut = Depends(auth_service.get_current_user),
):
    return current_user


@router.post("/me/avatar", response_model=UserOut)
async def change_avatar(
        file: UploadFile = File(...),
        current_user: UserOut = Depends(auth_service.get_current_user),
):
    updated_user = user_service.change_avatar(current_user.id, file)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
