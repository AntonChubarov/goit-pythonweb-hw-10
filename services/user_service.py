from abc import ABC, abstractmethod
from typing import Optional, Dict

from fastapi import UploadFile

from schemas.users import UserUpdate, UserOut


class IUserUpdateRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def update(self, user_id: int, user_update: UserUpdate):
        pass

    @abstractmethod
    def update_avatar(self, user_id: int, avatar_url: str):
        pass


class IImageStorage(ABC):
    @abstractmethod
    def upload_image(self, file_path: str, options: Dict = None) -> Dict:
        pass

    @abstractmethod
    def delete_image(self, public_id: str) -> Dict:
        pass


class UserService:
    def __init__(self, user_repository: IUserUpdateRepository, image_client: IImageStorage):
        self.user_repository = user_repository
        self.image_client = image_client

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserOut]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        updated_user = self.user_repository.update(user_id, user_update)
        return UserOut.from_orm(updated_user)

    def change_avatar(self, user_id: int, file: UploadFile) -> Optional[UserOut]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        upload_result = self.image_client.upload_image(file.file, options={"folder": "user_avatars"})
        avatar_url = upload_result.get("secure_url")

        updated_user = self.user_repository.update_avatar(user_id, avatar_url)
        return UserOut.from_orm(updated_user)
