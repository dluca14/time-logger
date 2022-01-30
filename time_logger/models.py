from datetime import datetime

from time_logger import db, ma


class Worker(db.Model):
    __tablename__ = 'worker'

    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), index=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# class WorkerSchema(ma.Schema):
#     class Meta:
#         model = Worker
#         fields = ("lname", "fname", "timestamp")
class WorkerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Worker

    id = ma.auto_field()
    lname = ma.auto_field()
    fname = ma.auto_field()
    timestamp = ma.auto_field()


class Shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    worker = db.relationship("Worker", backref=db.backref('shifts', lazy=True))


# class ShiftSchema(ma.Schema):
#     class Meta:
#         model = Shift
#         fields = ("start_date", "end_date")
class ShiftSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shift
        include_fk = True

    id = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    worker_id = ma.auto_field()
