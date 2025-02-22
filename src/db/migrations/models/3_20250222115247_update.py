from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `exel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `exel_id` INT NOT NULL,
    `quantity` INT NOT NULL,
    `name_docx_one` VARCHAR(50),
    `name_docx_two` VARCHAR(50),
    `name_docx_tre` VARCHAR(50)
) CHARACTER SET utf8mb4;
        ALTER TABLE `items` MODIFY COLUMN `name_item` VARCHAR(50)NOT NULL;
        ALTER TABLE `items` MODIFY COLUMN `unit` VARCHAR(10)NOT NULL;
        ALTER TABLE `items` MODIFY COLUMN `lot` VARCHAR(25);
        ALTER TABLE `users` MODIFY COLUMN `user_name` VARCHAR(20)NOT NULL;
        ALTER TABLE `users` MODIFY COLUMN `password` VARCHAR(20)NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `items` MODIFY COLUMN `name_item` VARCHAR(50)NOT NULL;
        ALTER TABLE `items` MODIFY COLUMN `unit` VARCHAR(10)NOT NULL;
        ALTER TABLE `items` MODIFY COLUMN `lot` VARCHAR(25);
        ALTER TABLE `users` MODIFY COLUMN `user_name` VARCHAR(20)NOT NULL;
        ALTER TABLE `users` MODIFY COLUMN `password` VARCHAR(20)NOT NULL;
        DROP TABLE IF EXISTS `exel`;"""
