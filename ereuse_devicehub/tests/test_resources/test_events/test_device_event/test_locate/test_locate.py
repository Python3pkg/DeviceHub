from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestLocate(TestDeviceEvent):
    LOCATE = 'locate'
    POST_LOCATE = TestDeviceEvent.DEVICE_EVENT + '/locate'

    def test_create_locate_with_place(self):
        locate = self.get_fixture(self.LOCATE, 'locate')
        locate['place'] = self.place['_id']
        locate['devices'] = self.devices_id
        self.post_and_check(self.POST_LOCATE, locate)
        # Let's check the place has been correctly materialized in the devices
        for device_id in self.devices_id:
            self.device_and_place_contain_each_other(device_id, self.place['_id'])

    def test_create_locate_with_coordinates(self):
        # Let's create a location with coordinates without a place that contains them. It will give us error.
        locate = self.get_fixture(self.LOCATE, 'locate_with_coordinates')
        locate['devices'] = self.devices_id
        try:
            self.post_and_check(self.POST_LOCATE, locate)
        except AssertionError as e:
            if e.args[0] == '400 != 201':
                # Now we create the place
                place = self.post_fixture(self.PLACES, self.PLACES, 'place_with_coordinates')
                # We repeat the location. As the coordinates are in the area of the place, we can create it
                locate = self.post_and_check(self.POST_LOCATE, locate)
                # Let's check if locate has been assigned to the place
                locate, _ = self.get(self.DEVICE_EVENT, '', locate['_id'])
                self.assertIn('place', locate)
                self.assertEqual(locate['place'], place['_id'])
            else:
                self.assertTrue(False)
        else:
            self.assertTrue(False)