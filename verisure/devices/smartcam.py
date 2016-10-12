"""
Smartcam device
"""

import os
from .overview import Overview

OVERVIEW_URL = '/overview/camera'
CAPTURE_URL = '/picturelog/camera/{}/capture.cmd'
IMAGES_URL = '/picturelog/seriespage/0'
DOWNLOAD_URL = '/camera/{}/image/{}.jpg'


class Smartcam(object):
    """ Smartcam device

    Args:
        session (verisure.session): Current session
    """

    def __init__(self, session):
        self._session = session

    def get(self):
        """ Get device overview """
        status = self._session.get(OVERVIEW_URL)
        return [Overview('smartcam', val) for val in status]

    def download_image(self, device_id, image_id, dest_path):
        """Download a image from mypages smartcam."""
        pic_url = DOWNLOAD_URL.format(
            device_id.upper().replace(' ', '%20'),
            image_id)
        image_filename = pic_url.rsplit('/', 1)[1]
        self._session.download(pic_url, (os.path.join(
            dest_path, image_filename)))
        return

    def get_imagelist(self):
        """ Get a list of current images from the device """
        status = self._session.get(IMAGES_URL)
        image_series = status['imageSeries']
        image_data_list = [li['images'] for li in image_series]
        n = len(image_data_list)
        image_ids = {}
        for i in range(0, n):
            lookup_image_id = [li['id'] for li in image_data_list[i]]
            image_id = str(''.join(lookup_image_id))
            lookup_device_id = [li['deviceLabel'] for li in image_data_list[i]]
            device_id = str(''.join(lookup_device_id))
            image_ids[image_id] = device_id
        return image_ids

    def capture(self, device_id):
        """Capture a new image to mypages

            Args:
                device_id (str): smartcam device id
        """
        data = {}
        return not self._session.post((CAPTURE_URL.format(
            device_id.upper().replace(' ', '%20'))), data)
