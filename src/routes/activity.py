from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from main import db
from models.activity import Activity

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/', methods=['GET'])
def list_activities():
    acts = Activity.query.order_by(Activity.start_time.desc()).all()
    return jsonify([a.to_dict() for a in acts])

@activity_bp.route('/create', methods=['GET', 'POST'])
def create_activity():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        data = request.form
        a = Activity(title=data['title'], description=data['description'])
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('activity_form.html')
