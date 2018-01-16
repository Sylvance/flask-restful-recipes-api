import datetime

from code.database import (
    db,
    Model,
    SurrogatePK,
)

class Token(SurrogatePK, Model):
    """
    Token Model for storing JWT tokens
    """

    __tablename__ = 'tokens'
    token = db.Column(db.String(500), unique=True, nullable=False)
    banned_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, **kwargs):
        db.Model.__init__(self, token = token, **kwargs)
        self.banned_on = datetime.datetime.now()

    @classmethod
    def check_banned(cls, auth_token):
        res = cls.query.filter_by(token=auth_token).first()
        if res:
            return True
        return False

    def __repr__(self):  # pragma: nocover
        return '<Token({token})>'.format(token=self.token)
