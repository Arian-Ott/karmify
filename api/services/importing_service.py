from api.services.user_service import User as UserService
from api.db import get_db
import csv
import os
from PIL import Image


def read_users_from_csv(path="api/data/users.csv") -> list[dict]:
    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        return list(reader)


def process_user_image(username: str, user_id: str):
    source = f"api/data/import/{username}.jpg"
    dest = f"api/data/assets/{user_id}.webp"
    if os.path.exists(source):
        img = Image.open(source).convert("RGB")
        img.save(dest, "WEBP", quality=85)


async def handler():
    users = read_users_from_csv()

    for user_data in users:
        user_service = UserService()
        user_service.set_username(user_data["username"])
        user_service.set_email(user_data["email"])
        user_service.set_password(user_data["password"])

        if not UserService.get_by_username(user_data["username"]):
            user_obj = user_service.create_user()
            process_user_image(user_obj.username, user_obj.user_id)
