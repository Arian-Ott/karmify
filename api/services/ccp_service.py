from api.models.ccp import CCPLog, CCPCategories
from api.models.users import UserTable
from api.services.user_service import User
from api.db import get_db
from api.schemas.ccp_schema import CCPReport
from sqlalchemy import func
from uuid import UUID
from sqlalchemy.orm import joinedload


class CCPCategoriesService:
    def __init__(self):
        pass

    @staticmethod
    def get_all_categories():
     
        """
        Get all available CCP categories.
        """
        with get_db() as db:
            categories = db.query(CCPCategories).order_by(CCPCategories.category_name).all()
            print(f"Found {len(categories)} CCP categories.")
            return [
                {
                    "id": category.id,
                    "category_name": category.category_name,
                    "description": category.description,
                    "is_violation": category.is_violation,
                    "points": category.points,
                }
                for category in categories
            ]

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
                return {"points": 0}

            total_points = (
                db.query(func.sum(CCPLog.points_awarded))
                .filter(CCPLog.user_id == UUID(user_id))
                .scalar()
            )

            if total_points is None:
                return {"points": 0}

            return {"points": total_points}

    @staticmethod
    def get_ccp_logs(user_id):
        """
        Get all CCP logs for a specific user, returned as a list of dictionaries.
        """
        user_uuid = UUID(user_id)
        with get_db() as db:
            user = db.query(UserTable).filter(UserTable.id == user_uuid).first()
            if not user:
                raise ValueError("User not found")

            logs = (
                db.query(CCPLog)
                .options(joinedload(CCPLog.category))
                .filter(CCPLog.user_id == user_uuid)
                .all()
            )

            return [
                {
                    "id": log.id,
                    "category_name": log.category.category_name
                    if log.category
                    else None,
                    "points_awarded": log.points_awarded,
                    "notes": log.notes,
                    "timestamp": log.date_logged,
                }
                for log in logs
            ]

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
    def create_ccp_log(report: CCPReport):
        """
        Create a new CCP log for a specific user.
        """
        with get_db() as db:
            user = (
                db.query(UserTable)
                .filter(UserTable.username == report.reportee)
                .first()
            )
            if not user:
                raise ValueError("User not found")

            category = (
                db.query(CCPCategories)
                .filter(CCPCategories.id == report.category_id)
                .first()
            )
            if not category:
                raise ValueError("CCP category not found")

            log = CCPLog(
                user_id=user.id,
                category_id=category.id,
                points_awarded=category.points,
                notes=report.comment,
            )
            db.add(log)
            db.commit()
