from datetime import datetime

from . import db


class URLMap(db.Model):
    __tablename__ = 'URLMap'
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, value=False):
        if value:
            return dict(
                url=self.original,
                short_link=self.short
            )
        return dict(url=self.original)

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])