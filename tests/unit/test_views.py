import datetime
from unittest.mock import patch, MagicMock, Mock


from tests.unit import client
from time_logger.models import Shift


def test_index(client):
    home_page = client.get("/")
    html = home_page.data.decode()

    assert "Welcome to Time-Logger" in html

    assert home_page.status_code == 200


def test_get_shifts(client):
    sh_obj = Shift(
        id=1,
        end_date=datetime.datetime(2021, 1, 1, 16),
        start_date=datetime.datetime(2021, 1, 1, 8),
        worker_id=1
    )
    wk_obj_mock = Mock(
        id=1,
        shifts=[sh_obj]
    )
    wk_model_mock = Mock()
    wk_model_mock.query.get.return_value = wk_obj_mock

    with patch.multiple('time_logger.views',
                        Worker=wk_model_mock):

        response = client.get("/workers/1/shifts")

        assert response.status_code == 200
        assert response.data.decode().replace('\n', '').replace(' ', '') == '[{"end_date":"2021-01-01T16:00:00","id":1,"start_date":"2021-01-01T08:00:00","worker_id":1}]'


def test_get_shift_return_200(client):
    sh_model_mock = Mock(return_value=Mock())

    sh_schema_obj_mock = Mock()
    sh_schema_mock = Mock(return_value=sh_schema_obj_mock)
    sh_schema_obj_mock.dump.return_value = 'shift'

    with patch.multiple('time_logger.views',
                        Shift=sh_model_mock,
                        ShiftSchema=sh_schema_mock):

        response = client.get("/workers/1/shifts/1")

        assert response.status_code == 200
        assert response.data.decode() == 'shift'


def test_get_shift_return_404(client):
    sh_model_mock = Mock()
    sh_model_mock.query.join.return_value.filter.return_value.filter.return_value.one_or_none.return_value = None

    with patch.multiple('time_logger.views',
                        Shift=sh_model_mock):

        response = client.get("/workers/1/shifts/1")

        assert response.status_code == 404
        sh_model_mock.query.join.return_value.filter.return_value.filter.return_value.one_or_none.assert_called_once()


def test_add_shift_201(client):
    rq_mock = Mock()
    rq_mock.is_json = True
    rq_mock.get_json.return_value = Mock()

    sh_schema_obj_mock = Mock()
    sh_schema_mock = Mock(return_value=sh_schema_obj_mock)
    sh_schema_obj_mock.load.return_value = {'start_date': 'start_date', 'end_date': 'end_date'}

    wk_obj_mock = Mock()
    wk_model_mock = Mock(return_value=wk_obj_mock)

    sh_model_mock = Mock()
    sh_model_mock.query.with_parent.return_value.filter.return_value.filter.return_value.one_or_none.return_value = None

    db_mock = Mock()

    with patch.multiple('time_logger.views',
                        request=rq_mock,
                        Shift=sh_model_mock,
                        ShiftSchema=sh_schema_mock,
                        Worker=wk_model_mock,
                        db=db_mock):

        client.post("/workers/1/shifts")

        rq_mock.get_json.assert_called_once()

        sh_schema_obj_mock.load.assert_called_once()

        wk_model_mock.query.get.assert_called_once()

        sh_model_mock.query.with_parent.return_value.filter.return_value.filter.return_value.one_or_none.assert_called_once()

        db_mock.session.add.assert_called_once()
        db_mock.session.commit.assert_called_once()


def test_add_shift_409(client):
    rq_mock = Mock()
    rq_mock.is_json = True
    rq_mock.get_json.return_value = {'start_date': 'start_date', 'end_date': 'end_date'}

    sh_schema_obj_mock = Mock()
    sh_schema_mock = Mock(return_value=sh_schema_obj_mock)
    sh_schema_obj_mock.load.return_value = {'start_date': 'start_date', 'end_date': 'end_date'}

    wk_obj_mock = Mock()
    wk_model_mock = Mock(return_value=wk_obj_mock)

    sh_model_mock = Mock()
    sh_model_mock.query.with_parent.return_value.filter.return_value.filter.return_value.one_or_none.return_value = 1

    db_mock = Mock()

    with patch.multiple('time_logger.views',
                        request=rq_mock,
                        Shift=sh_model_mock,
                        ShiftSchema=sh_schema_mock,
                        Worker=wk_model_mock,
                        db=db_mock):

        client.post("/workers/1/shifts")

        rq_mock.get_json.assert_called_once()

        sh_schema_obj_mock.load.assert_called_once()

        wk_model_mock.query.get.assert_called_once()

        sh_model_mock.query.with_parent.return_value.filter.return_value.filter.return_value.one_or_none.assert_called_once()

        db_mock.session.add.assert_not_called()
        db_mock.session.commit.assert_not_called()


def test_add_shift_415(client):
    rq_mock = Mock()
    rq_mock.is_json = False

    sh_schema_mock = Mock()
    wk_model_mock = Mock()
    sh_model_mock = Mock()
    db_mock = MagicMock()

    with patch.multiple('time_logger.views',
                        request=rq_mock,
                        Shift=sh_model_mock,
                        ShiftSchema=sh_schema_mock,
                        Worker=wk_model_mock,
                        db=db_mock):

        response = client.post("/workers/1/shifts")

        assert response.status_code == 415

        rq_mock.get_json.assert_not_called()

        wk_model_mock.query.get.assert_not_called()

        sh_model_mock.assert_not_called()

        db_mock.session.add.assert_not_called()
        db_mock.session.commit.assert_not_called()
