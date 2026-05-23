from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# Mongo Connection
mongo = AsyncIOMotorClient(MONGO_URL)

db = mongo["AutoRenameBot"]

users = db.users


# ADD USER
async def add_user(user_id):

    user = await users.find_one(
        {"_id": user_id}
    )

    if user:
        return

    data = {
        "_id": user_id,
        "prefix": "@MovieHub",
        "suffix": "x265",
        "metadata": True,
        "thumbnail": None,
        "sequence": True,
        "count": 1
    }

    await users.insert_one(data)


# GET USER
async def get_user(user_id):

    user = await users.find_one(
        {"_id": user_id}
    )

    return user


# SET PREFIX
async def set_prefix(user_id, value):

    await users.update_one(
        {"_id": user_id},
        {"$set": {"prefix": value}}
    )


# SET SUFFIX
async def set_suffix(user_id, value):

    await users.update_one(
        {"_id": user_id},
        {"$set": {"suffix": value}}
    )


# SET THUMBNAIL
async def set_thumbnail(user_id, value):

    await users.update_one(
        {"_id": user_id},
        {"$set": {"thumbnail": value}}
    )


# SET METADATA
async def set_metadata(user_id, value):

    await users.update_one(
        {"_id": user_id},
        {"$set": {"metadata": value}}
    )


# ENABLE / DISABLE SEQUENCE
async def set_sequence(user_id, value):

    await users.update_one(
        {"_id": user_id},
        {"$set": {"sequence": value}}
    )


# UPDATE COUNT
async def update_count(user_id, value):

    await users.update_one(
        {"_id": user_id},
        {"$set": {"count": value}}
    )
