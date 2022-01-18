from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime,ARRAY,VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc
from sqlalchemy.orm.attributes import QueryableAttribute
from env.config import Config

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.USER_DB}:{Config.PWD_DB}@{Config.HOST_DB}:{Config.PORT_DB}/{Config.NAME_DB}'
engine = create_engine(SQLALCHEMY_DATABASE_URI,pool_size=10, max_overflow=20)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class authUser(Base):
    __tablename__ = 'authUser'
    id = Column(Integer, primary_key=True)
    emp_id = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    roles = Column(VARCHAR(2000))

class timesubmissions(Base):
    __tablename__="timesubmissions"
    id = Column(Integer, primary_key=True)
    date_info = Column(DateTime)
    user_id = Column(String(50))
    manager_id = Column(String(50))
    time_type = Column(String(50))
    submission_id = Column(String(50))
    status = Column(String(50)) # ['submitted-pending approval','approved','unapproved']
    hours = Column(Integer)
    project_code=Column(String(50))
    task_id=Column(String(50))
    description=Column(String(1000))
    remarks=Column(String(1000))

class designation(Base):
    __tablename__="designation"
    id=Column(Integer,primary_key=True)
    designation=Column(String(50))

class department(Base):
    __tablename__="department"
    id=Column(Integer,primary_key=True)
    department_name=Column(String(50))

class announcements(Base):
    __tablename__="announcements"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    announcement_info = Column(String(50))
    announcement_category = Column(String(50))
    date_logged = Column(DateTime)
    
class employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    emp_id = Column(String(50))
    manager_id = Column(String(50))
    email = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    sur_name = Column(String(50))
    initial = Column(String(50)) 
    salutation = Column(String(5)) #mr,ms, Miss, Mrs
    project_code = Column(VARCHAR(50))
    dept = Column(String(50))
    designation = Column(String(50))
    
    emp_start_date = Column(VARCHAR(50))
    emp_last_working_date = Column(VARCHAR(50))
    emp_project_assigned_date = Column(VARCHAR(50))
    emp_project_end_date = Column(VARCHAR(50))

    employment_status = Column(String(50)) #in project, new joined, in notice, bench, relieved
    manager_name = Column(String(50)) 
    manager_dept = Column(String(50))
    resource_status = Column(String(50))
    delivery_type = Column(String(50))
    additional_allocation =  Column(String(50))
    skills =  Column(String(50))
    roles =  Column(VARCHAR(2000))

    
    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide), _path=("%s.%s" % (_path, key.lower()))
                        #_path=('%s.%s' % (path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data

class project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(50))
    project_code = Column(String(50))
    project_name = Column(String(50))
    project_manager_id=Column(VARCHAR(50))
    project_start_date = Column(VARCHAR(50))
    project_status = Column(String(50))
    billing_type = Column(String(50))
    segment = Column(String(50))
    geography = Column(String(50))
    solution_category = Column(String(50))
    financial_year = Column(String(50))
    resource_info = Column(String(50))

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide), _path=("%s.%s" % (_path, key.lower()))
                        #_path=('%s.%s' % (path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data
  
def serialize_all(data_obj):
    serialized = []
    for data in data_obj:
        data_dict = data.__dict__
        data_dict_keys = list(data_dict.keys())
        serial_dict ={}
        for i in range(1,len(data_dict_keys)):
            serial_dict[data_dict_keys[i]]=data_dict[data_dict_keys[i]]
        serialized.append(serial_dict)
    return serialized


class TimeMaster(Base):
    __tablename__ = 'TimeMaster'
    id = Column(Integer, primary_key=True)
    emp_id = Column(String(50))
    month = Column(String(50))
    year = Column(String(50))
    timedata = Column(VARCHAR(3000))

class forget_pass(Base):
    __tablename__ = 'forget_pass'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    email_address = Column(String(50))
    reset_token = Column(String(50))
    create_date = Column(VARCHAR(2000))

