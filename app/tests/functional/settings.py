import json
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class MongoTestSettings(BaseSettings):
    host: str = Field(alias='MONGO_HOST', default='127.0.0.1')
    port: int = Field(alias='MONGO_PORT', default=27017)

    @property
    def url(self):
        return f'mongodb://{self.host}:{self.port}'
    

class ServiceTestSettings(BaseSettings):
    host: str = Field(alias='SERVICE_HOST', default='127.0.0.1')
    port: int = Field(alias='SERVICE_PORT', default=8000)

    @property
    def url(self):
        return f'http://{self.host}:{self.port}'


class TestSettings(BaseSettings):
    mongo: MongoTestSettings = MongoTestSettings()
    service: ServiceTestSettings = ServiceTestSettings()
    base_dir: Path = Path(os.path.dirname(__file__)).parent.parent.resolve()


test_settings = TestSettings()