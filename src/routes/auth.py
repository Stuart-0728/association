from flask import Blueprint, request, session, redirect, url_for, flash
from main import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        if User.query.filter_by(username=data['username']).first():
            flash('用户名已存在')
            return redirect(url_for('auth.register'))
        user = User(
            username=data['username'],
            password=generate_password_hash(data['password']),
            email=data['email']
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            session.permanent = True
            session['user_id'] = user.id
            return redirect(url_for('dashboard.index'))
        flash('用户名或密码错误')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
