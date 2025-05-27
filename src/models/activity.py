from datetime import datetime
from src.main import db
from .user import association_table  # 引入多对多关联表

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 可选：多对多关系
    participants = db.relationship('User', secondary=association_table, back_populates='activities')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time.isoformat()
        }
