from rest_framework.test import APITestCase


class ApiDocsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        APITestCase.setUpClass()

    def test_docs(self):
        self.client.get('/docs/')  # smoke test

    def test_api_docs(self):
        """ Smoke test to make sure we don't break /docs/api-docs/"""
        resp = self.client.get('/docs/api-docs/')
        self.assertIn('apis', resp.data)

    def test_api_docs_individually(self):
        """ Smoke test to make sure we don't break individual api-docs"""
        resp = self.client.get('/docs/api-docs/')
        for api in resp.data['apis']:
            api_path = '/docs/api-docs' + api['path']
            doc_resp = self.client.get(api_path)
            self.assertIn('apis', doc_resp.data, api['path'])
            for sub_api in doc_resp.data['apis']:
                for operation in sub_api['operations']:
                    self.assertTrue(operation['nickname'].islower(),
                                    '%s nickname is lowercase.' % api_path)
