from flask import abort, jsonify, request
from marshmallow import ValidationError

from time_logger import db, app

from time_logger.models import Shift, ShiftSchema, Worker, WorkerSchema


@app.get("/workers/<int:worker_id>/shifts")
def get_shifts(worker_id):
    worker = Worker.query.get(worker_id)

    shifts_schema = ShiftSchema(many=True)
    data = shifts_schema.dump(worker.shifts)

    return jsonify(data)


@app.get("/workers/<int:worker_id>/shifts/<int:shift_id>")
def get_shift(worker_id, shift_id):
    shift = Shift.query \
        .join(Worker) \
        .filter(Worker.id == worker_id) \
        .filter(Shift.id == shift_id) \
        .one_or_none()

    if shift is not None:
        shift_schema = ShiftSchema()
        return shift_schema.dump(shift)
    else:
        abort(404, 'Shift not found for Id: {shift_id}'.format(shift_id=shift_id))


@app.post("/workers/<int:worker_id>/shifts")
def add_shift(worker_id):
    if request.is_json:
        json = request.get_json()

        shift_schema = ShiftSchema()
        try:
            data = shift_schema.load(json)
        except ValidationError as err:
            return err.messages, 422

        worker = Worker.query.get(worker_id)
        existing_shift = Shift.query.with_parent(worker)\
                              .filter(Shift.start_date == data['start_date'])\
                              .filter(Shift.end_date == data['end_date'])\
                              .one_or_none()

        if existing_shift is None:
            new_shift = Shift(start_date=data['start_date'], end_date=data['end_date'], worker_id=worker_id)
            db.session.add(new_shift)
            db.session.commit()
            return data, 201
        else:
            abort(
                409,
                "Shift {start_date} {end_date} exists already".format(
                    start_date=json['start_date'], end_date=json['end_date']
                ),
            )

    return {"error": "Request must be JSON"}, 415


@app.put("/workers/<int:worker_id>/shifts/<int:shift_id>")
def update_shift(worker_id, shift_id):
    pass


@app.patch("/workers/<int:worker_id>/shifts/<int:shift_id>")
def partially_update_shift(worker_id, shift_id):
    pass


@app.delete("/workers/<int:worker_id>/shifts/<int:shift_id>")
def delete_shift(worker_id, shift_id):
    pass
