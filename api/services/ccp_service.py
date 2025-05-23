from api.models.ccp import CCPLog, CCPCategories
from api.models.users import UserTable
from api.services.user_service import User
from api.db import get_db
from sqlalchemy import func
from uuid import UUID


class CCPCategoriesService:
    def __init__(self):
        pass

    @staticmethod
    def get_all_categories():
        """
        Get all available CCP categories.
        """
        with get_db() as db:
            return db.query(CCPCategories).all()

    @staticmethod
    def get_category_by_id(category_id):
        """
        Get a specific CCP category by its ID.
        """
        with get_db() as db:
            category = (
                db.query(CCPCategories).filter(CCPCategories.id == category_id).first()
            )
            if not category:
                raise ValueError("CCP category not found")
            return category

    @staticmethod
    def get_category_by_name(category_name):
        """
        Get a specific CCP category by its name.
        """
        with get_db() as db:
            category = (
                db.query(CCPCategories)
                .filter(CCPCategories.category_name == category_name)
                .first()
            )
            if not category:
                raise ValueError("CCP category not found")
            return category


class CCPLogService:
    def __init__(self, user_id, category, comment):
        self._category_service = CCPCategoriesService()
        self.user_id = UUID(user_id)
        self.category = self._category_service.get_category_by_name(category)
        self.comment = comment
        with get_db() as db:
            if not db.query(UserTable).filter(UserTable.id == self.user_id).first():
                raise ValueError("User not found")
            if (
                not db.query(CCPCategories)
                .filter(CCPCategories.id == self.category.id)
                .first()
            ):
                raise ValueError("CCP category not found")
            self.log = CCPLog(
                user_id=self.user_id,
                category_id=self.category.id,
                points_awarded=self.category.points,
                notes=self.comment,
            )
            db.add(self.log)
            db.commit()
            db.refresh(self.log)


class CCPService:
    def __init__(self):
        pass

    @staticmethod
    def get_sum_points(user_id):
        """
        Get the total points for a specific user.
        """
        with get_db() as db:
            if not db.query(UserTable).filter(UserTable.id == UUID(user_id)).first():
                raise ValueError("User not found")
            return (
                db.query(CCPLog)
                .filter(CCPLog.user_id == user_id)
                .with_entities(func.sum(CCPLog.points_awarded))
                .scalar()
            )

    @staticmethod
    def get_ccp_logs(user_id):
        """
        Get all CCP logs for a specific user.
        """
        with get_db() as db:
            if not db.query(UserTable).filter(UserTable.id == UUID(user_id)).first():
                raise ValueError("User not found")
            return db.query(CCPLog).filter(CCPLog.user_id == user_id).all()

    @staticmethod
    def get_ccp_log_by_id(log_id):
        """
        Get a specific CCP log by its ID.
        """
        with get_db() as db:
            log = db.query(CCPLog).filter(CCPLog.id == log_id).first()
            if not log:
                raise ValueError("CCP log not found")
            return log

    @staticmethod
    def create_ccp_log(user_id, log_data):
        """
        Create a new CCP log for a specific user.
        """
        with get_db() as db:
            if not db.query(UserTable).filter(UserTable.id == UUID(user_id)).first():
                raise ValueError("User not found")
            log = CCPLog(user_id=user_id, **log_data)
            db.add(log)
            db.commit()
            db.refresh(log)
            return log
