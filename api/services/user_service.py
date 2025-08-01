from api.models.users import UserTable
from api.models.roles import UserRoleTable, RoleTable
from api.schemas.user_schema import UserBase, UserCreate
from api.schemas.role_schema import RoleBase
from sqlalchemy.orm import Session
from api.db import get_db
from uuid import UUID
from . import crypto_context
import os


class User:
    def __init__(self):
        self.username = None
        self.email = None
        self.password = None

    def set_schema(self, user: UserBase):
        self.username = user.username
        self.email = user.email
        self.password = crypto_context.hash(user.password.encode())

    def set_username(self, username: str):
        self.username = username

    def set_email(self, email: str):
        self.email = email

    def set_password(self, password: str):
        self.password = crypto_context.hash(password.encode())

    def get_password(self):
        with get_db() as db:
            user = (
                db.query(UserTable).filter(UserTable.username == self.username).first()
            )
            if user:
                return user.hashed_password
            else:
                raise ValueError("User not found")

    @staticmethod
    def get_by_username(username: str):
        with get_db() as db:
            return db.query(UserTable).filter(UserTable.username == username).first()

    @staticmethod
    def get_by_email(db, email: str):
        with get_db() as db:
            return db.query(UserTable).filter(UserTable.email == email).first()

    @staticmethod
    def get_by_id(db, user_id):
        with get_db() as db:
            return db.query(UserTable).filter(UserTable.id == UUID(user_id)).first()

    def create_user(self):
        with get_db() as db:
            if db.query(UserTable).filter(UserTable.username == self.username).first():
                raise ValueError("Username already exists")
            if db.query(UserTable).filter(UserTable.email == self.email).first():
                raise ValueError("Email already exists")

        with get_db() as db:
            user = UserTable(
                username=self.username, email=self.email, hashed_password=self.password
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return UserCreate(
                username=user.username,
                email=user.email,
                password=self.password,
                user_id=str(user.id),
                date_created=str(user.created_at),
            )

    @staticmethod
    def authenticate_user(username: str, password: str):
        with get_db() as db:
            user = db.query(UserTable).filter(UserTable.username == username).first()
            if not user:
                return False
            if not crypto_context.verify(password.encode(), user.hashed_password):
                return False
            return dict(
                UserCreate(
                    username=user.username,
                    email=user.email,
                    password=user.hashed_password,
                    user_id=str(user.id),
                    date_created=str(user.created_at),
                )
            )

    @staticmethod
    def get_all_users():
        with get_db() as db:
            users = db.query(UserTable).order_by(UserTable.username).all()
            return [
                UserCreate(
                    username=user.username,
                    email=user.email,
                    password=user.hashed_password,
                    user_id=str(user.id),
                    date_created=str(user.created_at),
                )
                for user in users
            ]

    @staticmethod
    def get_roles(username: str):
        with get_db() as db:
            user = db.query(UserTable).filter(UserTable.username == username).first()
            if not user:
                raise ValueError("User not found")
            roles = (
                db.query(UserRoleTable).filter(UserRoleTable.user_id == user.id).all()
            )
            roles = (
                db.query(RoleTable)
                .filter(RoleTable.name.in_([role.role_name for role in roles]))
                .all()
            )
            if not roles:
                return []
            print(list(roles))
            return [role.name for role in roles]

    @staticmethod
    def delete_user(user_id):
        user_id = UUID(user_id)
        with get_db() as db:
            user = db.query(UserTable).filter(UserTable.id == user_id).first()
            if not user:
                raise ValueError("User not found")
            db.delete(user)
            db.commit()
        if os.path.exists(f"api/static/uploads/{user_id}.webp"):
            os.remove(f"api/static/uploads/{user_id}.webp")
