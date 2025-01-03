from .config import TORTOISE_ORM
from tortoise import Tortoise

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections()