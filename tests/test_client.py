from octopus_energy_client import OctopusEnergy, ResourceType
import unittest
import mock
import responses
import requests
import datetime
import pytz

class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        
        self.api_key = "123456"
        self.electricity_serial = "abc1234"
        self.electricity_mpan = "1234567890"
        self.electricity_product_code = "21JBLAH"
        self.electricity_region = "Z"
        self.gas_serial = "cba4321"
        self.gas_mprn = "0987654321"
        self.gas_product_code = "12XFOO"
        self.gas_region = "A"


        self.client = OctopusEnergy(
            api_key=self.api_key,
            electricity_serial=self.electricity_serial,
            electricity_mpan=self.electricity_mpan,
            electricity_product_code=self.electricity_product_code,
            electricity_region=self.electricity_region,
            gas_serial=self.gas_serial,
            gas_mprn=self.gas_mprn,
            gas_product_code=self.gas_product_code,
            gas_region=self.gas_region
        )
    
    def test_meter_url(self):
        self.assertEqual(self.client.meter_url(ResourceType.ELECTRICITY), f"{self.client.base_url}/electricity-meter-points/{self.electricity_mpan}")
        self.assertEqual(self.client.meter_url(ResourceType.GAS), f"{self.client.base_url}/gas-meter-points/{self.gas_mprn}")

    def test_tariff_url(self):
        self.assertEqual(self.client.tariff_url(ResourceType.ELECTRICITY), f"{self.client.base_url}/products/{self.electricity_product_code}/electricity-tariffs/E-1R-{self.electricity_product_code}-{self.electricity_region}")
        self.assertEqual(self.client.tariff_url(ResourceType.GAS), f"{self.client.base_url}/products/{self.gas_product_code}/gas-tariffs/E-1R-{self.gas_product_code}-{self.gas_region}")

    def test_consumption_url(self):
        self.assertEqual(self.client.consumption_url(ResourceType.ELECTRICITY), f"{self.client.base_url}/electricity-meter-points/{self.electricity_mpan}/meters/{self.electricity_serial}/consumption")
        self.assertEqual(self.client.consumption_url(ResourceType.GAS), f"{self.client.base_url}/gas-meter-points/{self.gas_mprn}/meters/{self.gas_serial}/consumption")

    def test_date_to_periods(self):
        dt = datetime.date(2021,1,1)
        period_from, period_to = self.client.date_to_periods(dt)
        
        self.assertEqual(period_from, datetime.datetime(2021,1,1,0,0,0, tzinfo=pytz.utc))
        self.assertEqual(period_to, datetime.datetime(2021,1,1,23,30,0, tzinfo=pytz.utc))

    @responses.activate
    def test_get_data(self):
        url = "https://api.octopus.energy/v1/electricity-meter-points/01234567890"
        expected = {'gsp': '_C', 'mpan': '01234567890', 'profile_class': 1}

        responses.add(responses.GET, url, json=expected, status=200)

        response = self.client.get_data(url)
        self.assertDictEqual(response, expected)
        responses.assert_call_count(url, 1)

    @responses.activate
    def test_get_meter_point_electricity(self):
        url = self.client.meter_url(ResourceType.ELECTRICITY)
        expected = {'gsp': '_C', 'mpan': '01234567890', 'profile_class': 1}

        responses.add(responses.GET, url, json=expected, status=200)

        response = self.client.get_meter_point(ResourceType.ELECTRICITY)
        self.assertDictEqual(response, expected)
        responses.assert_call_count(url, 1)

    @responses.activate
    def test_get_meter_point_gas(self):
        url = self.client.meter_url(ResourceType.GAS)
        expected = {'gsp': '_C', 'mprn': '0987654321', 'profile_class': 1}

        responses.add(responses.GET, url, json=expected, status=200)

        response = self.client.get_meter_point(ResourceType.GAS)
        self.assertDictEqual(response, expected)
        responses.assert_call_count(url, 1)

    @responses.activate
    def test_get_grid_supply_points(self):
        url = f"{self.client.base_url}/industry/grid-supply-points"
        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "group_id": "_A"
                },
            ]
        }

        responses.add(responses.GET, url, json=expected, status=200)

        response = self.client.get_grid_supply_points()
        self.assertDictEqual(response, expected)
        responses.assert_call_count(url, 1)

    @responses.activate
    def test_get_grid_supply_points_with_postocde(self):
        url = f"{self.client.base_url}/industry/grid-supply-points?postcode=SW1A%201AA"
        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "group_id": "_A"
                },
            ]
        }

        responses.add(responses.GET, url, json=expected, status=200)

        response = self.client.get_grid_supply_points("SW1A 1AA")
        self.assertDictEqual(response, expected)
        responses.assert_call_count(url, 1)


if __name__ == '__main__':
    unittest.main()