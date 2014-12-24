from flask.ext.testing import TestCase
import stockManagement


class test_stockManagment(TestCase):

    def create_app(self):
        stockapp = stockManagement.app
        return stockapp

    def setUp(self):
        pass

    def test_assert_indexTemplate_used_with_param(self):
        response = self.client.get("/test")
        self.assert_context("name", "test")
        self.assert_template_used('index.html')

    def test_assert_errorTemplate_used(self):
        response = self.client.get("/error")
        self.assert_template_used('error.html')

