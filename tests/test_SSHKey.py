"""
This module contains tests for the SSHKey class
"""

from unittest import TestCase
from mock import MagicMock, patch
from doboto import SSHKey


class TestSSHKey(TestCase):
    """
    This class implements unittests for the SSHKey class
    """

    def setUp(self):
        """
        Define resources usable by all unit tests
        """

        self.test_url = "http://abc.example.com"
        self.test_uri = "{}/account/keys".format(self.test_url)
        self.test_token = "abc123"
        self.instantiate_args = (self.test_url, self.test_token)

        self.klass_name = "SSHKey"
        self.klass = getattr(SSHKey, self.klass_name)

    def test_class_exists(self):
        """
        SSHKey class is defined
        """

        self.assertTrue(hasattr(SSHKey, self.klass_name))

    def test_can_instantiate(self):
        """
        SSHKey class can be instantiated
        """

        exc_thrown = False

        try:
            self.klass(*self.instantiate_args)
        except Exception:
            exc_thrown = True

        self.assertFalse(exc_thrown)

    @patch('doboto.SSHKey.SSHKey.pages')
    def test_list_happy(self, mock_pages):
        """
        list works with happy path
        """

        ssh_key = self.klass(self.test_url, self.test_token)
        result = ssh_key.list()

        mock_pages.assert_called_with(self.test_uri, "ssh_keys")

    @patch('doboto.SSHKey.SSHKey.request')
    def test_create(self, mock_request):
        """
        create works with datas
        """

        ssh_key = self.klass(self.test_url, self.test_token)

        datas = {
            "name": "My SSH Public Key",
            "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAQQD example"
        }

        result = ssh_key.create(
            datas["name"], datas["public_key"]
        )

        mock_request.assert_called_with(
            self.test_uri, "ssh_key", 'POST', attribs=datas
        )


    @patch('doboto.SSHKey.SSHKey.request')
    def test_info(self, mock_request):
        """
        info works with ssh id or fingerprint
        """

        ssh_key_id = 512189
        ssh_key = self.klass(self.test_url, self.test_token)
        result = ssh_key.info(ssh_key_id)

        test_uri = "{}/{}".format(self.test_uri, ssh_key_id)
        mock_request.assert_called_with(test_uri, "ssh_key")

    @patch('doboto.SSHKey.SSHKey.request')
    def test_update(self, mock_request):
        """
        update works with ssh id or fingerprint
        """

        ssh_key_id = 512189
        ssh_key = self.klass(self.test_url, self.test_token)
        result = ssh_key.update(ssh_key_id, "My Other Public Key")

        test_uri = "{}/{}".format(self.test_uri, ssh_key_id)
        mock_request.assert_called_with(
            test_uri, "ssh_key", 'PUT', attribs={"name": "My Other Public Key"}
        )

    @patch('doboto.SSHKey.SSHKey.request')
    def test_destroy(self, mock_request):
        """
        destroy works with ssh id or fingerprint
        """

        ssh_key_id = 512189
        ssh_key = self.klass(self.test_url, self.test_token)
        result = ssh_key.destroy(ssh_key_id)

        test_uri = "{}/{}".format(self.test_uri, ssh_key_id)
        mock_request.assert_called_with(test_uri, request_method='DELETE')
