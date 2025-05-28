from flask import Flask, render_template, session, jsonify, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'replace_with_a_secret_key'

# 示例用户数据
users = {
    'admin': {'username': 'admin', 'role': 'admin'},
    'user': {'username': 'user', 'role': 'user'}
}

# 所有页面路由都渲染同一个模板，让前端 Vue Router 接管
@app.route('/')
@app.route('/activities')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
@app.route('/admin/activities/new')
@app.route('/activities/<path:dummy>')
def catch_all(dummy=None):
    currentUser = session.get('user')
    return render_template('index.html', currentUser=currentUser)

# 用户信息接口
@app.route('/api/auth/profile')
def api_profile():
    user = session.get('user')
    if user:
        return jsonify({'success': True, 'user': user})
    else:
        return jsonify({'success': False, 'message': '未登录'}), 401

# 登录接口
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    user = users.get(username)
    if user:
        session['user'] = user
        return jsonify({'success': True, 'user': user})
    else:
        return jsonify({'success': False, 'message': '用户名不存在'}), 400

# 登出接口
@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.pop('user', None)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
