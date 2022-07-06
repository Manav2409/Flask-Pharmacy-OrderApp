from db import db
from sqlalchemy import Integer
from datetime import datetime

class SubscriptionModel(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    subscription_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pres_id = db.Column(db.Integer)
    refill = db.Column(db.String(80))
    m_location = db.Column(db.String(120))
    sub_status = db.Column(db.String(80))

    def __init__(self, member_id,subscription_date, pres_id, refill, m_location, sub_status):
        self.member_id = member_id
        self.subscription_date = subscription_date
        self.pres_id = pres_id
        self.refill = refill
        self.m_location = m_location
        self.sub_status = sub_status

    def json(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'subscription_date': self.subscription_date,
            'pres_id': self.pres_id,
            'refill': self.refill,
            'm_location': self.m_location,
            'sub_status': self.sub_status
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    @classmethod
    def find_by_member_id(cls, member_id):
        return cls.query.filter_by(member_id=member_id).first() 

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()