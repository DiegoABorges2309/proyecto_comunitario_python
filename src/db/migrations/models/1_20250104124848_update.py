from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `items` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name_item` VARCHAR(20) NOT NULL,
    `quantity` DOUBLE NOT NULL,
    `unit` VARCHAR(10) NOT NULL,
    `lot` VARCHAR(25),
    `exp` DATE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `items`;"""
