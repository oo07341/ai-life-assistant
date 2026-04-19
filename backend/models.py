# models.py
# 数据库模型定义

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(50), primary_key=True)  # 用户ID
    email = db.Column(db.String(100), unique=True, nullable=True)
    username = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    plans = db.relationship('Plan', backref='user', lazy=True, cascade='all, delete-orphan')
    search_history = db.relationship('SearchHistory', backref='user', lazy=True, cascade='all, delete-orphan')

class Plan(db.Model):
    """学习计划表"""
    __tablename__ = 'plans'
    
    id = db.Column(db.String(50), primary_key=True)  # 计划ID
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    goal = db.Column(db.String(200))
    target_date = db.Column(db.Date)
    daily_hours = db.Column(db.Integer, default=4)
    subjects = db.Column(db.Text, default='[]')  # 存储科目列表的JSON字符串
    schedule_data = db.Column(db.Text, default='{}')  # 存储日程安排的JSON字符串
    ics_content = db.Column(db.Text)  # iCalendar文件内容
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_dates = db.Column(db.Text, default='[]')  # 已完成的日期列表的JSON字符串
    parent_plan_ids = db.Column(db.Text, default='[]')  # 父计划ID列表的JSON字符串
    
    # 属性访问器，自动处理JSON序列化
    @property
    def subjects_list(self):
        return json.loads(self.subjects) if self.subjects else []
    
    @subjects_list.setter
    def subjects_list(self, value):
        self.subjects = json.dumps(value, ensure_ascii=False)
    
    @property
    def schedule_dict(self):
        return json.loads(self.schedule_data) if self.schedule_data else {}
    
    @schedule_dict.setter
    def schedule_dict(self, value):
        self.schedule_data = json.dumps(value, ensure_ascii=False)
    
    @property
    def completed_dates_list(self):
        return json.loads(self.completed_dates) if self.completed_dates else []
    
    @completed_dates_list.setter
    def completed_dates_list(self, value):
        self.completed_dates = json.dumps(value, ensure_ascii=False)
    
    @property
    def parent_plan_ids_list(self):
        return json.loads(self.parent_plan_ids) if self.parent_plan_ids else []
    
    @parent_plan_ids_list.setter
    def parent_plan_ids_list(self, value):
        self.parent_plan_ids = json.dumps(value, ensure_ascii=False)

class SearchHistory(db.Model):
    """搜索历史表"""
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String(200), nullable=False)
    intent = db.Column(db.String(50))  # shopping, schedule, general
    product_keywords = db.Column(db.Text, default='[]')  # 商品关键词列表的JSON字符串
    location_hint = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def product_keywords_list(self):
        return json.loads(self.product_keywords) if self.product_keywords else []
    
    @product_keywords_list.setter
    def product_keywords_list(self, value):
        self.product_keywords = json.dumps(value, ensure_ascii=False)

class PriceComparison(db.Model):
    """商品比价表"""
    __tablename__ = 'price_comparisons'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(50))  # 平台名称：美团、饿了么等
    price = db.Column(db.Float)
    original_price = db.Column(db.Float)
    discount = db.Column(db.String(50))
    location = db.Column(db.String(50))
    url = db.Column(db.String(500))
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)
