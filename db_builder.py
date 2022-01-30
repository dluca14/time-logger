from datetime import datetime

from time_logger import db
from time_logger.models import Worker, WorkerSchema, Shift, ShiftSchema


db.create_all()

w_schema = WorkerSchema()
s_schema = ShiftSchema()

w1 = Worker(lname='Luca', fname='David')
s1 = Shift(start_date=datetime(2021, 1, 1, 8), end_date=datetime(2021, 1, 1, 16), worker=w1)
s2 = Shift(start_date=datetime(2021, 1, 2, 12), end_date=datetime(2021, 1, 1, 20))
w1.shifts.append(s2)
db.session.add(w1)

w2 = Worker(lname='Chiran', fname='Lavinia')
s3 = Shift(start_date=datetime(2021, 1, 1, 12), end_date=datetime(2021, 1, 1, 20), worker=w2)
db.session.add(w2)

db.session.commit()

# Shift.query.with_parent(w1).filter(Shift.start_date != datetime(2021, 1, 1, 8).all()
