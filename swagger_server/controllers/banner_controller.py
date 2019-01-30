import connexion
import six
from sqlalchemy import and_

from swagger_server.models.banner import Banner  # noqa: E501
from swagger_server.config import db, settings
from swagger_server import util


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
    app_codes = data.pop('app_code').split(',')
    for app in app_codes:
        data['app_code'] = app
        banner = Banner.from_dict(data)  # noqa: E501
        if not banner.msg:
            banner.msg = settings.MSG_TEMPLATE.render(banner=banner)
        banner_in_db = Banner.query.get((banner.app_code, banner.date_start))
        if banner_in_db:
            db.session.delete(banner_in_db)
        db.session.add(banner)
    db.session.commit()

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
    return 'do some magic!'


def get_banner_list(date_start=None, is_active=None, date_finish=None, app_codes=None):  # noqa: E501
    """Получить список активных баннеров

     # noqa: E501

    :param date_start: Дата начала работ
    :type date_start: str
    :param is_active: Актуальный баннер
    :type is_active: bool
    :param date_finish: Дата окончания работ
    :type date_finish: str
    :param app_codes: Системы на которые вешается баннер
    :type app_codes: List[str]

    :rtype: List[Banner]
    """
    date_start = util.deserialize_datetime(date_start)
    date_finish = util.deserialize_datetime(date_finish)
    return 'do some magic!'
