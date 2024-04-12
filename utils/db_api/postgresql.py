from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        try:
            self.pool = await asyncpg.create_pool(
                dsn=f"postgresql://postgres:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
            print('Successfully connected to the PostgreSQL database!')
        except Exception as e:
            print('Something went wrong while connecting to PostgreSQL: ', e)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_group_info(self):
        sql = """
        CREATE TABLE IF NOT EXISTS group_info (
        group_id VARCHAR(100) NOT NULL UNIQUE,
        restrict_min INT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_words(self):
        sql = """
        CREATE TABLE IF NOT EXISTS bad_words (
        words VARCHAR(100) NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def add_new_group(self, group_id, restrict_min):
        sql = """
        INSERT INTO group_info (group_id, restrict_min)
        VALUES ($1, $2) returning *
        """
        return await self.execute(sql, group_id, restrict_min, fetchrow=True)

    async def get_restrict_min_by_group_id(self, group_id):
        sql = """
        SELECT restrict_min
        FROM group_info
        WHERE group_id = $1;
        """
        return await self.execute(sql, group_id, fetchval=True)

    async def update_restrict_min_by_group_id(self, restrict_min, group_id):
        sql = """
        UPDATE group_info
        SET restrict_min = $1
        WHERE group_id = $2
        """
        return await self.execute(sql, restrict_min, group_id, execute=True)

    # i want to get all groups ids
    async def count_groups(self):
        sql = "SELECT COUNT(*) FROM group_info"
        return await self.execute(sql, fetchval=True)

    async def drop_groups(self):
        await self.execute("DROP TABLE IF EXISTS group_info", execute=True)

    async def add_word(self, word: str):
        sql = """
        INSERT INTO bad_words (words)
        VALUES ($1)
        """
        try:
            await self.execute(sql, word, execute=True)
            return True  # Return True if the word was successfully added
        except asyncpg.exceptions.UniqueViolationError:
            return False  # Return False if the word already exists in the table

    async def get_all_words(self):
        sql = "SELECT words FROM bad_words;"
        words = await self.execute(sql, fetch=True)
        return [row['words'] for row in words]

    async def delete_word(self, word: str):
        sql = "DELETE FROM bad_words WHERE words = $1"
        await self.execute(sql, word, execute=True)

    async def delete_words(self):
        await self.execute("DROP TABLE bad_words", execute=True)

    async def get_admins(self):
        records = await self.execute("SELECT telegram_id FROM admins", fetch=True)
        telegram_ids = [record['telegram_id'] for record in records]
        return telegram_ids

    async def select_member(self, **kwargs):
        sql = "SELECT * FROM group_info WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_users_by_group_id(self, group_id):
        sql = """
        SELECT telegram_id
        FROM group_info
        WHERE group_id = $1
        """
        return await self.execute(sql, group_id, fetch=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE IF EXISTS users", execute=True)

    async def get_unique_group_ids(self):
        sql = "SELECT * FROM group_info"
        return await self.execute(sql, fetch=True)

    async def get_admins(self):
        records = await self.execute("SELECT telegram_id FROM admins", fetch=True)
        telegram_ids = [record['telegram_id'] for record in records]
        return telegram_ids

    async def add_admin(self, telegram_id):
        sql = """
        INSERT INTO admins (telegram_id) VALUES ($1)
        ON CONFLICT (telegram_id) DO NOTHING
        """
        await self.execute(sql, telegram_id, execute=True)

    async def remove_admin(self, telegram_id):
        sql = """
        DELETE FROM admins WHERE telegram_id = $1
        """
        await self.execute(sql, telegram_id, execute=True)

    async def is_admin(self, user_id: int) -> bool:
        """
        Check if the given user ID is among the admin IDs stored in the database.

        Args:
            user_id (int): The user ID to check.

        Returns:
            bool: True if the user ID is among the admin IDs, False otherwise.
        """
        sql = "SELECT COUNT(*) FROM admins WHERE telegram_id = $1"
        admin_count = await self.execute(sql, user_id, fetchval=True)
        return admin_count > 0
