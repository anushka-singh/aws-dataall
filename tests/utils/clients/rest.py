import pytest
from fastapi.testclient import TestClient
import os

os.environ['envname'] = 'pytest'
from src.cdkproxymain import app
import dataall

ENVNAME = os.environ.get('envname', 'pytest')


@pytest.fixture(scope='module')
def cdkclient():
    yield TestClient(app)


@pytest.fixture(scope='module')
def db() -> dataall.base.db.Engine:
    engine = dataall.base.db.get_engine(envname=ENVNAME)
    dataall.base.db.create_schema_and_tables(engine, envname=ENVNAME)
    yield engine
    engine.session().close()
    engine.engine.dispose()
