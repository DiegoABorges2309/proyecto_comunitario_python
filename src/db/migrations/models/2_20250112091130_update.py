from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `items` MODIFY COLUMN `name_item` VARCHAR(50) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `items` MODIFY COLUMN `name_item` VARCHAR(20) NOT NULL;"""
