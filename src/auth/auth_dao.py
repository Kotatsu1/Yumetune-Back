from .auth_models import RefreshSessionModel
from .auth_schemas import RefreshSessionCreate, RefreshSessionUpdate
from base_dao import BaseDAO



class RefreshSessionDAO(BaseDAO[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]):
    model = RefreshSessionModel
