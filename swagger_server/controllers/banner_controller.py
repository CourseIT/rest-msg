import datetime

import connexion
from flask import current_app
from sqlalchemy import and_
from sqlalchemy.sql.operators import in_op

from swagger_server import util
from swagger_server.config import db, settings
from swagger_server.models import Banner, AddBannerBody, Email


def add_banner(banner):  # noqa: E501
    """Зарегистрировать новые профилактические работы

     # noqa: E501

    :param banner: Добавляемый баннер
    :type banner: dict | bytes

    :rtype: None
    """
    if not connexion.request.is_json:
        return 'json is needed', 415

    data = connexion.request.get_json()

    banner_body = AddBannerBody.from_dict(data)
    for app in banner_body.app_codes:
        banner = Banner(app_code=app, date_start=banner_body.date_start, date_finish=banner_body.date_finish,
                        msg=banner_body.msg)
        if not banner.msg:
            banner.msg = settings.MSG_TEMPLATE.render(banner=banner)
        banner_in_db = Banner.query.get((banner.app_code, banner.date_start))
        if banner_in_db:
            db.session.delete(banner_in_db)
            db.session.commit()
        db.session.add(banner)
    db.session.commit()

    email_query = Email.query.filter_by(app_code=banner.app_code)

    if email_query.count():
        current_app.enqueue('common.email', system='maintenance', sender="Noreply",
                            receiver=[x.email for x in Email.query.filter_by(app_code=banner.app_code)],
                            subject='Обновление системы',
                            content_html=current_app.config['EMAIL'].render(banner=banner)
                            )

    return "Данные успешно добавлены"


def delete_banners(date_start, app_codes=None):  # noqa: E501
    """Удалить список баннеров, удовлетворяющих списку

     # noqa: E501

    :param date_start: Дата начала работ
    :type date_start: str
    :param app_codes: Системы на которые вешается баннер
    :type app_codes: List[str]

    :rtype: None
    """
    date_start = util.deserialize_datetime(date_start)
    for app_code in app_codes:
        banner_in_db = Banner.query.get_or_404((app_code, date_start))
        if banner_in_db:
            db.session.delete(banner_in_db)
    db.session.commit()
    return 'Данные успешно удалены'


def get_banner_info(app_code):  # noqa: E501
    """Получить информацию о текущем активном баннере

     # noqa: E501

    :param app_code: Идентификатор системы
    :type app_code: str

    :rtype: str
    """
    return Banner.query.filter(
        and_(Banner.app_code == app_code, Banner.date_finish > datetime.datetime.now())) \
        .order_by(Banner.date_start) \
        .first_or_404().msg


def get_banner_list(date_start=None, date_finish=None, app_codes=None):  # noqa: E501
    """Получить список активных баннеров

     # noqa: E501

    :param date_start: Дата начала работ
    :type date_start: str
    :param date_finish: Дата окончания работ
    :type date_finish: str
    :param app_codes: Системы на которые вешается баннер
    :type app_codes: List[str]

    :rtype: List[Banner]
    """
    date_start = util.deserialize_datetime(date_start) if date_start else datetime.datetime.min
    date_finish = util.deserialize_datetime(date_finish) if date_finish else datetime.datetime.max

    filtered = and_(Banner.date_start >= date_start, Banner.date_finish <= date_finish)
    if app_codes:
        filtered = and_(in_op(Banner.app_code, app_codes), filtered)

    return Banner.query.filter(filtered) \
        .order_by(Banner.date_start) \
        .all()
