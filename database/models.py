from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()

def wib_now():
    return datetime.now(
        ZoneInfo("Asia/Jakarta")
    )

class ScanHistory(db.Model):

    __tablename__ = 'scan_history'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    cleaned_text = db.Column(
        db.Text
    )

    prediction = db.Column(
        db.String(20),
        nullable=False
    )

    confidence = db.Column(
        db.Float
    )

    risk_score = db.Column(
        db.Integer
    )

    category = db.Column(
        db.String(100)
    )

    created_at = db.Column(
        db.DateTime,
        default=wib_now
    )

    def __repr__(self):
        return (
            f"<ScanHistory {self.id}>"
        )