import os
import sys
from flask import Flask, session, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# 将项目根目录加入路径，确保导入 src 包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

load_dotenv()
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret')
# 使用默认值保证环境变量缺失时不会为 None
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '3306')
db_name = os.getenv('DB_NAME', 'association_db')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 86400
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# ORM & Migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 导入模型确保注册
from src.models.user import User
from src.models.activity import Activity

# 蓝图注册
from src.routes.auth import auth_bp
from src.routes.user import user_bp
from src.routes.activity import activity_bp
from src.routes.registration import registration_bp
from src.routes.dashboard import dashboard_bp
from src.routes.upload import upload_bp

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(activity_bp, url_prefix='/api/activities')
app.register_blueprint(registration_bp, url_prefix='/api/registrations')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(upload_bp, url_prefix='/api/upload')

# 首页
@app.route('/')
def index():
    activities = Activity.query.order_by(Activity.start_time.desc()).limit(10).all()
    return render_template('index.html', activities=activities)

# 错误处理
@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'message': '服务器内部错误'}), 500

# 安全头
@app.after_request
def add_security_headers(response):
    response.headers.update({
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block'
    })
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
