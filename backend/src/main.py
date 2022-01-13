from entities.database import timesubmissions
from entities.database import Session, engine, Base
from entities.database import serialize_all
from entities.modules.time_submissions import time_module
from entities.modules.login import login_module
from entities.modules.employee import employee_module
from entities.modules.projects import project_module
from entities.modules.announcements import announcement_module
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask import Flask, jsonify
from flask_cors import CORS
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

@app.route('/rawDataDownload', methods=['POST'])
def rawDataDownload():
    session = Session()
    sub_objects = session.query(timesubmissions).all()
    serialized_obj = serialize_all(sub_objects)
    raw_data=serialized_obj
    return(jsonify(raw_data))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)