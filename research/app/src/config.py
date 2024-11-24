from pydantic import Field
from pydantic_settings import BaseSettings

class MongoSettings(BaseSettings):
    """
    Конфигурация для настроек Mongo DB
    """
    host: str = Field(alias='MONGO_HOST', default='127.0.0.1')
    port: int = Field(alias='MONGO_PORT', default=27017)
    db: str = Field(alias='MONGO_DB', default='ugc')

    @property
    def url(self) -> str:
        return f'mongodb://{self.host}:{self.port}'


class PostgresSettings(BaseSettings):
    """
    Конфигурация для настроек Postgres
    """
    db: str = Field(alias='POSTGRES_DB', default='ugc')
    user: str = Field(alias='POSTGRES_USER', default='admin')
    password: str = Field(alias='POSTGRES_PASSWORD', default='123qwe')
    host: str = Field(alias='POSTGRES_HOST', default='127.0.0.1')
    port: int = Field(alias='POSTGRES_PORT', default=5432)

    @property
    def url(self) -> str:
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.url}"


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()
    postgres: PostgresSettings = PostgresSettings()

settings = Settings()