# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.banner import Banner  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBannerController(BaseTestCase):
    """BannerController integration test stubs"""

    def test_add_banner(self):
        """Test case for add_banner

        Зарегистрировать новые профилактические работы
        """
        banner = Banner()
        response = self.client.open(
            '//notification',
            method='POST',
            data=json.dumps(banner),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_banners(self):
        """Test case for delete_banners

        Удалить список баннеров, удовлетворяющих списку
        """
        query_string = [('date_start', 'date_start_example'),
                        ('app_codes', 'app_codes_example')]
        response = self.client.open(
            '//notification',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_banner_info(self):
        """Test case for get_banner_info

        Получить информацию о текущем активном баннере
        """
        response = self.client.open(
            '//notification/{app_code}'.format(app_code='app_code_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_banner_list(self):
        """Test case for get_banner_list

        Получить список активных баннеров
        """
        query_string = [('date_start', '2013-10-20T19:20:30+01:00'),
                        ('is_active', true),
                        ('date_finish', '2013-10-20T19:20:30+01:00'),
                        ('app_codes', 'app_codes_example')]
        response = self.client.open(
            '//notification',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
