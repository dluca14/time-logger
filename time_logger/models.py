from datetime import datetime

from marshmallow import fields
from marshmallow.validate import Range

from time_logger import db, ma


class Worker(db.Model):
    __tablename__ = 'worker'

    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), index=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkerSchema(ma.Schema):
    class Meta:
        model = Worker

    id = fields.Integer(required=True)
    lname = fields.Str(required=True)
    fname = fields.Str(required=True)
    timestamp = fields.DateTime(allow_none=True)


# shifts_per_day = {
#     '1': {
#         'start_hour': 8,
#         'end_hour': 16
#     },
#     '2': {
#         'start_hour': 16,
#         'end_hour': 0
#     },
#     '3': {
#         'start_hour': 0,
#         'end_hour': 8
#     }
# }

class Shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    shift_number = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    worker = db.relationship("Worker", backref=db.backref('shifts', lazy=True))


class ShiftSchema(ma.Schema):
    class Meta:
        model = Shift
        include_fk = True

    id = fields.Integer(required=True)
    shift_type = fields.Integer(validate=Range(min=1, max=4))
    created = fields.DateTime(allow_none=False)
    worker_id = fields.Integer(required=True)
