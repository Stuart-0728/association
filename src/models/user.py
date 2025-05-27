from src.main import db

association_table = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # 可选：多对多关系
    activities = db.relationship('Activity', secondary=association_table, back_populates='participants')

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}
