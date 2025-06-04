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
            {
                "category_name": "Clapping too slowly at political speech",
                "description": "Applauding at a tempo insufficiently enthusiastic during official events.",
                "china_points": -50,
                "is_violation": True,
            },
            {
                "category_name": "Downloading Winnie the Pooh memes",
                "description": "Possessing digital contraband of a bear that must not be named.",
                "china_points": -999,
                "is_violation": True,
            },
            {
                "category_name": "Owning more than one VPN",
                "description": "Excessively bypassing the Great Firewall, like it's a hobby.",
                "china_points": -150,
                "is_violation": True,
            },
            {
                "category_name": "Wearing a Che Guevara T-shirt ironically",
                "description": "Subversive ambiguity detected in fashion choices.",
                "china_points": -100,
                "is_violation": True,
            },
            {
                "category_name": "Standing during national anthem… with slouch",
                "description": "Failing to exude maximum patriotism through posture.",
                "china_points": -25,
                "is_violation": True,
            },
            {
                "category_name": "Singing revolutionary songs in karaoke",
                "description": "Injecting the party spirit into nightlife.",
                "china_points": +35,
                "is_violation": False,
            },
            {
                "category_name": "Correctly identifying Xi Jinping Thought",
                "description": "Demonstrates ideological clarity under pressure.",
                "china_points": +88,
                "is_violation": False,
            },
            {
                "category_name": "Googling 'Tiananmen'",
                "description": "Asking questions that should not be asked.",
                "china_points": -1000,
                "is_violation": True,
            },
            {
                "category_name": "Bringing own chopsticks to restaurant",
                "description": "Culturally virtuous and hygienic behavior.",
                "china_points": +10,
                "is_violation": False,
            },
            {
                "category_name": "Using Telegram in plain sight",
                "description": "Suspiciously transparent encrypted communication.",
                "china_points": -80,
                "is_violation": True,
            },
            {
                "category_name": "Accidentally creating a hexagram while drawing",
                "description": "Potential unsanctioned mysticism or summoning.",
                "china_points": -30,
                "is_violation": True,
            },
            {
                "category_name": "Laughing during news broadcast",
                "description": "Disrespecting the solemn tone of state media.",
                "china_points": -20,
                "is_violation": True,
            },
            {
                "category_name": "Nodding aggressively during CCP speech",
                "description": "Showing excessive and slightly terrifying enthusiasm.",
                "china_points": +5,
                "is_violation": False,
            },
            {
                "category_name": "Paying utility bills on time",
                "description": "Consistently paying electricity, water, and gas bills before the deadline.",
                "china_points": +20,
                "is_violation": False,
            },
            {
                "category_name": "Defaulting on a bank loan",
                "description": "Failure to repay a personal or business loan in the agreed timeframe.",
                "china_points": -100,
                "is_violation": True,
            },
            {
                "category_name": "Donating to government-approved charities",
                "description": "Supporting public welfare through approved charitable organizations.",
                "china_points": +30,
                "is_violation": False,
            },
            {
                "category_name": "Violating public health orders",
                "description": "Refusing to comply with pandemic-related restrictions or quarantine rules.",
                "china_points": -80,
                "is_violation": True,
            },
            {
                "category_name": "Using real-name registration online",
                "description": "Complying with legal requirements for identity verification on websites and platforms.",
                "china_points": +10,
                "is_violation": False,
            },
            {
                "category_name": "Evading public transportation fare",
                "description": "Riding subways, buses, or trains without paying the required fare.",
                "china_points": -25,
                "is_violation": True,
            },
            {
                "category_name": "Being cited in court records",
                "description": "Appearing in publicly available legal rulings or as a party in a civil/criminal case.",
                "china_points": -150,
                "is_violation": True,
            },
            {
                "category_name": "Reporting illegal activity",
                "description": "Cooperating with authorities by reporting crimes or policy violations.",
                "china_points": +50,
                "is_violation": False,
            },
            {
                "category_name": "Buying train tickets for others with your ID",
                "description": "Allowing someone else to travel under your name, potentially bypassing restrictions.",
                "china_points": -60,
                "is_violation": True,
            },
            {
                "category_name": "Posting verified positive reviews",
                "description": "Providing genuine, positive feedback for businesses or services online.",
                "china_points": +5,
                "is_violation": False,
            },
            {
                "category_name": "Spitting in public",
                "description": "Contributing to public health issues through unhygienic behavior.",
                "china_points": -15,
                "is_violation": True,
            },
            {
                "category_name": "Driving under the influence",
                "description": "Operating a vehicle while intoxicated.",
                "china_points": -200,
                "is_violation": True,
            },
            {
                "category_name": "Using public restrooms without flushing",
                "description": "Failing to maintain hygiene standards in public facilities.",
                "china_points": -10,
                "is_violation": True,
            },
            {
                "category_name": "Participating in state-sponsored events",
                "description": "Engaging in government-organized activities or celebrations.",
                "china_points": +15,
                "is_violation": False,
            },
            {
                "category_name": "Sharing state secrets",
                "description": "Disclosing confidential information that could harm national security.",
                "china_points": -99999,
                "is_violation": True,
            },
            {
                "category_name": "Using social media responsibly",
                "description": "Posting content that aligns with government policies and promotes social harmony.",
                "china_points": +10,
                "is_violation": False,
            },
            {
                "category_name": "Participating in community service",
                "description": "Volunteering for local projects or helping neighbors.",
                "china_points": +20,
                "is_violation": False,
            },
            {
                "category_name": "Using Windows",
                "description": "Using Microsoft Bloatware instead of Debian GNU/Linux.",
                "china_points": -42,
                "is_violation": True,
            },
        ]
        categories = list(sorted(categories, key=lambda x: x["category_name"]))
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
