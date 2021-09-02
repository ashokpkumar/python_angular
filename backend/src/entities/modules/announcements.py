from flask import Blueprint, jsonify, request
import datetime
from entities.database import Session,serialize_all
from entities.database import announcements

announcement_module = Blueprint(name="announcements", import_name=__name__)

@announcement_module.route('/announcements')
def announcement():
    session = Session()
    announcement_objects = session.query(announcements).all()
    serialized_obj = serialize_all(announcement_objects)
    session.close()
    return (jsonify(serialized_obj))

@announcement_module.route('/add_announcements', methods=['POST'])
def add_announcements():
    data = request.get_json()
    announcement_data = announcements (user_id =data.get('user_id').lower(),
                                       announcement_info = data.get('announcement_info').lower(),
                                       announcement_category=data.get('announcement_category').lower(),
                                       date_logged = datetime.datetime.now(),
                                        )
    session = Session()
    session.add(announcement_data)
    session.commit()    
    return ({'success':'Announcements are added sucessfully '})

@announcement_module.route('/get_announcements', methods=['POST'])
def get_announcements():
    session = Session()
    data = request.get_json()
    user_id = data.get("user_id")
    existing_announcements = session.query(announcements).filter(announcements.user_id==user_id).order_by(announcements.id.desc())[-30:]
    if existing_announcements:
        serialized_obj = serialize_all(existing_announcements)
        #print(serialized_obj)
        return jsonify(serialized_obj),200  
    return jsonify({'info':'No announcements are available for you'}),200

@announcement_module.route('/del_fn',methods=['POST'])
def delete_fn():
    session = Session()
    data = request.get_json()
    x = data.get("x")
    delete_announcements=session.query(announcements).filter(announcements.id>=x).delete()
    #delete_announcements = announcements.delete().where(announcements.c.id > x)
    return jsonify({'info':'announcements are deleted '}),200
