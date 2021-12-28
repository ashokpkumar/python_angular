#from .entities.entity import Session, engine, Base
# sources
#https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
#https://medium.com/@alanhamlett/part-1-sqlalchemy-models-to-json-de398bc2ef47#:~:text=To%20add%20a%20serialization%20method,columns%20and%20returns%20a%20dictionary.&text=def%20to_dict(self%2C%20show%3D,of%20this%20model.%22%22%22
#sources

from entities.database import employee,project,authUser,timesubmissions,TimeMaster, forget_pass
from entities.database import employee,project,authUser,timesubmissions
from entities.database import announcements
from entities.database import Session, engine, Base
from entities.database import serialize_all

from entities.helper import stringToList,listToString

from entities.modules.time_submissions import time_module
from entities.modules.login import login_module
from entities.modules.employee import employee_module
from entities.modules.projects import project_module
from entities.modules.announcements import announcement_module
#from entities.sample_data import create_sample_employee,create_sample_project,create_sample_timesubmissions,sample_department,sample_designation
from entities.sample_data import create_sample_project,create_sample_employee,create_sample_authUser
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_expects_json import expects_json
from flask_mail import Mail, Message
from datetime import date, timedelta


from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import time
import datetime
import json
import pytest
from sqlalchemy.ext.serializer import loads, dumps
import entities.mail
from flask import request, render_template
import os
from env.config import Config
from flask_swagger_ui import get_swaggerui_blueprint

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

app = Flask(__name__, template_folder=template_dir)
app.config.from_object(Config)
mail = Mail(app)
jwt = JWTManager(app)
CORS(app)
app.register_blueprint(time_module, url_prefix="/")
app.register_blueprint(login_module, url_prefix="/")
app.register_blueprint(employee_module, url_prefix="/")
app.register_blueprint(project_module, url_prefix="/")
app.register_blueprint(announcement_module, url_prefix="/")

SWAGGER_URL = '/api-documentation' 
API_URL = '/static/swagger.yaml'   
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "RMG Application"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

Base.metadata.create_all(engine)

create_sample_employee()
create_sample_project()
create_sample_authUser()
# create_sample_timesubmissions()
# sample_department()
# sample_designation()



@app.route('/rawDataDownload', methods=['POST'])
def rawDataDownload():
    session = Session()
    sub_objects = session.query(timesubmissions).all()
    serialized_obj = serialize_all(sub_objects)
    raw_data=serialized_obj
    return(jsonify(raw_data))

if __name__ == '__main__':
    app.run(debug = True)