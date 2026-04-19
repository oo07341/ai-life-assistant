# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_uuid = db.Column(db.String(36), unique=True, nullable=False, index=True)
    nickname = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    plans = db.relationship('Plan', back_populates='user', lazy='dynamic')
    search_logs = db.relationship('SearchLog', back_populates='user', lazy='dynamic')

    @staticmethod
    def get_or_create(user_uuid):
        """根据 UUID 获取或创建用户"""
        user = User.query.filter_by(user_uuid=user_uuid).first()
        if not user:
            user = User(user_uuid=user_uuid)
            db.session.add(user)
            db.session.commit()
        return user


class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(__import__('uuid').uuid4())[:8])
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal = db.Column(db.String(128), nullable=False)
    schedule_info = db.Column(db.JSON, nullable=False)  # 原始参数
    schedule_data = db.Column(db.JSON, nullable=False)  # schedule 数组
    ics_content = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    parent_plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = db.relationship('User', back_populates='plans')
    daily_tasks = db.relationship('DailyTask', back_populates='plan', lazy='dynamic', cascade='all, delete-orphan')
    parent = db.relationship('Plan', remote_side=[id], backref='children')

    def to_dict(self):
        return {
            'plan_id': self.plan_uuid,
            'goal': self.goal,
            'schedule_info': self.schedule_info,
            'schedule': self.schedule_data,
            'ics_content': self.ics_content,
            'completed_dates': [t.task_date.isoformat() for t in self.daily_tasks.filter_by(completed=True).all()],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'parent_plan_ids': [self.parent.plan_uuid] if self.parent else []
        }


class DailyTask(db.Model):
    __tablename__ = 'daily_tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    task_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.UniqueConstraint('plan_id', 'task_date', name='uq_plan_date'),)

    plan = db.relationship('Plan', back_populates='daily_tasks')


class SearchLog(db.Model):
    __tablename__ = 'search_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    query = db.Column(db.String(255), nullable=False)
    intent = db.Column(db.String(32), nullable=True)
    keywords = db.Column(db.JSON, nullable=True)
    result_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', back_populates='search_logs')