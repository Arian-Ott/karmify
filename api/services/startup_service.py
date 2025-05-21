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
USER_CSV = settings.IMPORT_DIR + "/users.csv"


def csv_reader(path):
    df = pd.read_csv(path)
    users = df.to_dict(orient="records")
    return users

def copy_jpg_to_assets():


    source_dir = ""    
    dest_dir = settings.IMPORT_DIR 

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith(".jpg"):
            shutil.copy(os.path.join(source_dir, filename), dest_dir)
            print(f"Copied {filename} to {dest_dir}")
        else:
            print(f"Skipped {filename}, not a .jpg file")

def check_user_exists(username, email):
    with get_db() as db:
        if db.query(UserTable).filter(UserTable.username == username).first():
            return True
        if db.query(UserTable).filter(UserTable.email == email).first():
            return True
    return False


def create_users():
    users = csv_reader(USER_CSV)

    for user in users:
        print(user["username"])
        if check_user_exists(user["username"], user["email"]):
            continue
        usr = User()
        usr.set_username(user["username"])
        usr.set_password(user["password"])
        usr.set_email(user["email"])
        usr.create_user()


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
    csv_reader(USER_CSV)
    table_creation()
    create_roles()
    create_admin_user()
    assign_admin_role()
    copy_jpg_to_assets()
    create_users()
