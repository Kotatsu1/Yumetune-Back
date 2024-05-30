from .user_models import UserModel
from .user_schemas import UserCreateDB, UserUpdateDB
from base_dao import BaseDAO


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel


