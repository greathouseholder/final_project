from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from src.infra.adapters.rdb.interface import RDBRepository
from src.infra.adapters.rdb.sqlalchemy.repository import SQLAlchemyRDBRepository
from src.shared.config import config

Base = declarative_base()


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_db_engine(self) -> AsyncEngine:
        return create_async_engine(
            config.RELATIONAL_DATABASE_URL,
            future=True
        )

    @provide(scope=Scope.APP)
    def provide_session_factory(
            self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )

    @provide(scope=Scope.REQUEST)
    def provide_db_session(
        self,
        session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncSession:
        return session_factory()


class SQLAlchemyRDBRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_sqlalchemy_repository(
            self, session: AsyncSession) -> RDBRepository:
        return SQLAlchemyRDBRepository(session)
