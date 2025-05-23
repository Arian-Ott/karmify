from api.models.roles import RoleTable, UserRoleTable
from api.models.users import UserTable
from api.db import get_db
from api.services.user_service import User
from api.config import settings
from api.db import Base, engine
from api.config import settings
import pandas as pd
import os
import shutil
import csv


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
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_roles():
    with get_db() as db:
        roles = [
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
    create_admin_user()
    assign_admin_role()
