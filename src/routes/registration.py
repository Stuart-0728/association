from flask import Blueprint, request, jsonify, session, redirect, url_for
from main import db
from models.activity import Activity
from models.user import User

registration_bp = Blueprint('registration', __name__)

# 简易报名：用户报名活动
@registration_bp.route('/register', methods=['POST'])
def register_activity():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    data = request.json
    act = Activity.query.get_or_404(data['activity_id'])
    user = User.query.get(user_id)
    act.participants.append(user)  # 需在模型中定义多对多关系
    db.session.commit()
    return jsonify({'success': True})
