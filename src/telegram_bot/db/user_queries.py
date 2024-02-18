
from typing import Type, Any

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

#from src.telegram_bot.db import User
from src.telegram_bot.db.skindatabase import SkinDatabase


#class UserQueries:
#    @staticmethod
#    async def remove_user(user_id: int):
#        session_maker = Database.get_session_maker()
#        async with session_maker() as session:
#            stmt = delete(User).where(User.user_id == user_id)
#            await session.execute(stmt)
#            await session.commit()
#
#    @staticmethod
#    async def add_user(user_id: int, username: str, full_name: str):
#        session_maker = Database.get_session_maker()
#        async with session_maker() as session:
#            await session.execute(insert(User).values(user_id=user_id, username=username, full_name=full_name))
#            await session.commit()
#
#    @staticmethod
#    async def is_user_exists(user_id: int) -> bool:
#        session_maker = Database.get_session_maker()
#        async with session_maker() as session:
#            stmt = select(User.full_name).where(User.user_id == user_id)
#            sql_result = await session.execute(stmt)
#            result = sql_result.one_or_none()
#            return True if result else False
#
#    @staticmethod
#    async def get_user_info(
#            user_id: int, information: str | list | tuple
#    ) -> Type[Any] | None:
#        session_maker = Database.get_session_maker()
#        async with session_maker() as session:
#            if isinstance(information, (list, tuple)):
#                models = [User.__dict__[info] for info in information]
#                stmt = select(*models).where(User.user_id == user_id)
#            else:
#                stmt = select(User.__dict__[information]).where(User.user_id == user_id)
#
#            result = await session.execute(stmt)
#            return result.one_or_none()
#
#    @staticmethod
#    async def get_users():
#        session_maker = Database.get_session_maker()
#        async with session_maker() as session:
#            stmt = select(User)
#            result = await session.execute(stmt)
#            return result.scalars()
#
#
#