from flask import Blueprint, request, jsonify, session
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    f = request.files.get('file')
    if not f:
        return jsonify({'success': False, 'message': '未检测到文件'}), 400
    upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, f.filename)
    f.save(path)
    return jsonify({'success': True, 'path': path})
