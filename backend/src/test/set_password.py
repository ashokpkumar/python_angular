"""import pytest
from flask import Flask
from entities.sample_data import create_sample_employee,create_sample_project,create_sample_timesubmissions,create_sample_authUser,time_master
from collections.abc import Iterable
"
@pytest.fixture
def set_password(create_sample_authUser):
    data = authUser_list
    return isinstance(data, Iterable)
""

def test_login(check_login):
    data = dict(emp_id="Manager",password="manager123")
    assert data in data


 @pytest.mark.usefixtures('client_class')
class TestView:

    def login(self, emp_id, password):
        credentials = {'emp_id': "manager@ind.com", 'password': "manager123"}
        return self.client.post(url_for('login'), data=credentials)

    def test_login(self):
        assert self.login('manager@ind.com', 'manager123').status_code == 200
"""
@pytest.fixture(scope="session")
def connection():
    engine = create_engine(
        "mysql+mysqldb://{}:{}@{}:{}/{}".format(
            os.environ.get('TEST_DB_USER'),
            os.environ.get('TEST_DB_PASSWORD'),
            os.environ.get('TEST_DB_HOST'),
            os.environ.get('TEST_DB_PORT'),
            os.environ.get('TEST_DB_NAME'),
        )
    )
    return engine.connect()


def seed_database():
    users = [
        {
            "id": 1,
            "name": "John Doe",
        },
        # ...
    ]

    for user in users:
        db_user = User(**user)
        db_session.add(db_user)
    db_session.commit()


@pytest.fixture(scope="session")
def setup_database(connection):
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()
    
    seed_database()

    yield

    models.Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()