from api.models.roles import RoleTable, UserRoleTable
from api.models.users import UserTable
from api.db import get_db
from api.services.user_service import User
from api.config import settings
from api.db import Base, engine
from api.config import settings
from api.models.ccp import CCPCategories
import pandas as pd



def check_user_exists(username, email):
    with get_db() as db:
        if db.query(UserTable).filter(UserTable.username == username).first():
            return True
        if db.query(UserTable).filter(UserTable.email == email).first():
            return True
    return False


def table_creation():
    """Startup event handler."""
    if settings.DEBUG:
        Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def add_ccp_categories():
    """Add default CCP categories."""
    with get_db() as db:
        categories = [
            {
                "category_name": "Bypassing with VPN",
                "description": "Bypassing the restrictions of the CCP with a VPN.",
                "china_points": -40,
                "is_violation": True,
            },
            {
                "category_name": "Disrespecting the CCP",
                "description": "Disrespecting the CCP.",
                "china_points": -99999,
                "is_violation": True,
            },
            {
                "category_name": "Helping elderly people",
                "description": "Helping old people",
                "china_points": 40,
                "is_violation": False,
            },
            {
                "category_name": "Helping adults",
                "description": "Helping adults is half of elderly people",
                "china_points": 20,
                "is_violation": False,
            },
            {
                "category_name": "Helping children",
                "description": "Helping children is half of adults",
                "china_points": 10,
                "is_violation": False,
            },
        ]
        for category in categories:
            if (
                db.query(CCPCategories)
                .filter(CCPCategories.category_name == category["category_name"])
                .first()
            ):
                continue
            new_category = CCPCategories(
                category_name=category["category_name"],
                description=category["description"],
                is_violation=category["is_violation"],
                points=category["china_points"],
            )
            db.add(new_category)
        db.commit()


def create_roles():
    with get_db() as db:
        roles = [
            RoleTable(name="xijinping", description="xijinping"),
            RoleTable(name="admin", description="Administrator"),
            RoleTable(name="user", description="Regular user"),
            RoleTable(name="guest", description="Guest user"),
        ]

        for role in roles:
            if db.query(RoleTable).filter(RoleTable.name == role.name).first():
                continue
            db.add(role)
        db.commit()


def create_admin_user():
    with get_db() as db:
        if db.query(UserTable).filter(UserTable.username == "admin").first():
            return

    user = User()
    user.set_username("admin")
    user.set_email("admin@example.com")
    user.set_password("admin")
    user.create_user()


def assign_admin_role():
    with get_db() as db:
        user = db.query(UserTable).filter(UserTable.username == "admin").first()
        if not user:
            return

        if (
            db.query(UserRoleTable)
            .filter(
                UserRoleTable.user_id == user.id,
                UserRoleTable.role_name == "admin",
            )
            .first()
        ):
            return

        role = RoleTable(name="admin")
        user_role = UserRoleTable(user_id=user.id, role_name=role.name)
        db.add(user_role)
        db.commit()


def startup():
    """Startup event handler."""

    table_creation()
    create_roles()
    add_ccp_categories()
    create_admin_user()
    assign_admin_role()
