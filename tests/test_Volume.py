"""
This module contains tests for the main DO class
"""

from unittest import TestCase
from mock import MagicMock, patch
from doboto import Volume


class TestVolume(TestCase):

    """
    This class implements unittests for the main DO class
    """

    def setUp(self):
        """
        Define resources usable by all unit tests
        """

        self.test_url = "http://abc.example.com"
        self.test_uri = "{}/volumes".format(self.test_url)
        self.test_token = "abc123"
        self.instantiate_args = (self.test_url, self.test_token)

        self.klass_name = "Volume"
        self.klass = getattr(Volume, self.klass_name)

    def test_class_exists(self):
        """
        Volume class is defined
        """

        self.assertTrue(hasattr(Volume, self.klass_name))

    def test_can_instantiate(self):
        """
        Volume class can be instantiated
        """

        exc_thrown = False

        try:
            self.klass(*self.instantiate_args)
        except Exception:
            exc_thrown = True

        self.assertFalse(exc_thrown)

    @patch('doboto.Volume.Volume.pages')
    def test_list(self, mock_pages):
        """
        list works
        """

        volume = self.klass(self.test_url, self.test_token)

        # Alone

        volume.list()
        mock_pages.assert_called_with(self.test_uri, "volumes")

        # By region

        region = "nyc1"
        volume.list(region)
        mock_pages.assert_called_with(self.test_uri, "volumes", params={"region": region})

    @patch('doboto.Volume.Volume.request')
    def test_create(self, mock_request):
        """
        create works with volume id
        """

        volume = self.klass(self.test_url, self.test_token)
        datas = {"name": "test.com", "region": "nyc3",
                 "size": "512mb", "image": "ubuntu-14-04-x64"}
        volume.create(datas)

        mock_request.assert_called_with(
            self.test_uri, "volume", 'POST', attribs=datas)

        # Check empty

        volume.create()

        mock_request.assert_called_with(
            self.test_uri,  "volume", 'POST', attribs={})

    @patch('doboto.Volume.Volume.request')
    def test_info(self, mock_request):
        """
        info works with volume id or name
        """

        id = 12345
        volume = self.klass(self.test_url, self.test_token)

        # By id

        volume.info(id)
        test_uri = "{}/{}".format(self.test_uri, id)
        mock_request.assert_called_with(test_uri, "volume")

        # By name and region

        volume.info(name="stuff", region="nyc1")
        test_uri = self.test_uri
        mock_request.assert_called_with(test_uri, "volume", params={"name": "stuff", "region": "nyc1"})

        # Requirements met

        self.assertRaisesRegexp(
            ValueError, "Must supply an id or name and region", volume.info
        )
        self.assertRaisesRegexp(
            ValueError, "Must supply an id or name and region", volume.info, name="stuff"
        )
        self.assertRaisesRegexp(
            ValueError, "Must supply an id or name and region", volume.info, region="nyc1"
        )

    @patch('doboto.Volume.Volume.request')
    def test_destroy(self, mock_request):
        """
        destroy works with volume id or name
        """

        id = 12345
        volume = self.klass(self.test_url, self.test_token)

        # By id

        volume.destroy(id)
        test_uri = "{}/{}".format(self.test_uri, id)
        mock_request.assert_called_with(test_uri, request_method="DELETE")

        # By name

        volume.destroy(name="stuff", region="nyc1")
        test_uri = self.test_uri
        mock_request.assert_called_with(
            test_uri, request_method="DELETE", params={"name": "stuff", "region": "nyc1"}
        )

        # Requirements met

        self.assertRaisesRegexp(
            ValueError, "Must supply an id or name and region", volume.destroy
        )
        self.assertRaisesRegexp(
            ValueError, "Must supply an id or name and region", volume.destroy, name="stuff"
        )
        self.assertRaisesRegexp(
            ValueError, "Must supply an id or name and region", volume.destroy, region="nyc1"
        )

    @patch('doboto.Volume.Volume.pages')
    def test_snapshot_list(self, mock_pages):
        """
        snapshot_list works with volume id
        """

        id = 12345
        volume = self.klass(self.test_url, self.test_token)
        volume.snapshot_list(id)
        test_uri = "{}/{}/snapshots".format(self.test_uri, id)

        mock_pages.assert_called_with(test_uri, "snapshots")

    @patch('doboto.Volume.Volume.request')
    def test_snapshot_create(self, mock_request):
        """
        test snapshot_create works with volume id
        """
        volume = self.klass(self.test_url, self.test_token)
        id = 12345
        test_uri = "{}/{}/snapshots".format(self.test_uri, id)

        snap_name = "snap-1"
        datas = {"name": snap_name}
        volume.snapshot_create(id, snap_name)
        mock_request.assert_called_with(test_uri, "snapshot", 'POST', attribs=datas)

    @patch('doboto.Volume.Volume.request')
    def test_attach(self, mock_request):
        """
        test that attach works with id and/or name
        """
        volume = self.klass(self.test_url, self.test_token)

        droplet_id = 123
        region = "nyc1"

        # By id

        id = 12345
        test_uri = "{}/{}/actions".format(self.test_uri, id)
        datas = {
            "type": "attach",
            "droplet_id": droplet_id
        }
        volume.attach(id=id, droplet_id=droplet_id)
        mock_request.assert_called_with(test_uri, "action", 'POST', attribs=datas)

        datas = {
            "type": "attach",
            "droplet_id": droplet_id,
            "region": region
        }
        volume.attach(id=id, droplet_id=droplet_id, region=region)
        mock_request.assert_called_with(test_uri, "action", 'POST', attribs=datas)

        # By name

        name = "stuff"
        test_uri = "{}/actions".format(self.test_uri)
        datas = {
            "type": "attach",
            "droplet_id": droplet_id,
            "volume_name": name
        }
        volume.attach(name=name, droplet_id=droplet_id)
        mock_request.assert_called_with(test_uri, "action", 'POST', attribs=datas)

        # Requirements met

        self.assertRaisesRegexp(
            ValueError, "Must supply an id or name", volume.attach, droplet_id=droplet_id
        )

    @patch('doboto.Volume.Volume.request')
    def test_detach(self, mock_request):
        """
        test that detach works with id and/or name
        """
        volume = self.klass(self.test_url, self.test_token)

        droplet_id = 123
        region = "nyc1"

        # By id

        id = 12345
        test_uri = "{}/{}/actions".format(self.test_uri, id)
        datas = {
            "type": "detach",
            "droplet_id": droplet_id
        }
        volume.detach(id=id, droplet_id=droplet_id)
        mock_request.assert_called_with(test_uri, "action", 'POST', attribs=datas)

        datas = {
            "type": "detach",
            "droplet_id": droplet_id,
            "region": region
        }
        volume.detach(id=id, droplet_id=droplet_id, region=region)
        mock_request.assert_called_with(test_uri, "action", 'POST', attribs=datas)

        # By name

        name = "stuff"
        test_uri = "{}/actions".format(self.test_uri)
        datas = {
            "type": "detach",
            "droplet_id": droplet_id,
            "volume_name": name
        }
        volume.detach(name=name, droplet_id=droplet_id)
        mock_request.assert_called_with(test_uri, "action", 'POST', attribs=datas)

        # Requirements met

        self.assertRaisesRegexp(
            ValueError, "Must supply an id or name", volume.detach, droplet_id=droplet_id
        )

    @patch('doboto.Volume.Volume.request')
    def test_resize(self, mock_request):
        """
        test that resize works
        """
        volume = self.klass(self.test_url, self.test_token)

        id = 12345
        region = "nyc1"
        size = 2
        test_uri = "{}/{}/actions".format(self.test_uri, id)
        datas = {
            "type": "resize",
            "size_gigabytes": 2
        }
        volume.resize(id, size)
        mock_request.assert_called_with(test_uri, "action", 'POST', attribs=datas)

        datas = {
            "type": "resize",
            "region": region,
            "size_gigabytes": 2
        }
        volume.resize(id, size, region)
        mock_request.assert_called_with(test_uri, "action", 'POST', attribs=datas)

    @patch('doboto.Volume.Volume.pages')
    def test_action_list(self, mock_pages):
        """
        actions works with volume id
        """

        id = 12345
        volume = self.klass(self.test_url, self.test_token)
        volume.action_list(id)
        test_uri = "{}/{}/actions".format(self.test_uri, id)

        mock_pages.assert_called_with(test_uri, "actions")

    @patch('doboto.Volume.Volume.request')
    def test_action_info(self, mock_request):
        """
        action_info works with volume id and action id
        """

        id = 12345
        action_id = 54321
        volume = self.klass(self.test_url, self.test_token)
        volume.action_info(id, action_id)
        test_uri = "{}/{}/actions/{}".format(
            self.test_uri, id, action_id)

        mock_request.assert_called_with(test_uri, "action")
