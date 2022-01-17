import requests
import os
import logging
import datetime
import pytz
from .enums import ResourceType, Aggregate
from .util import iso_format


logger = logging.getLogger(__name__)


class OctopusEnergy:
    """
    Python API for retrieving Octopus Energy data.

    See https://developer.octopus.energy/docs/api/ for more details of the Octopus API.    
    """
    base_url = "https://api.octopus.energy/v1"

    def __init__(
        self,
        api_key=None,
        electricity_serial=None,
        electricity_mpan=None,
        electricity_product_code=None,
        electricity_region=None,
        gas_serial=None,
        gas_mprn=None,
        gas_product_code=None,
        gas_region=None
    ):
        """
        Initialiser for the OctopusEnergy class.

        For account keys and serial numbers, see https://octopus.energy/dashboard/developer/.

        All params are optional, with defaults taken from environment variables if not specified.

        :param str api_key: The customer API key for accessing octopus energy data. Default: environ['OCTOPUS_API_KEY']
        :param str electricity_serial: The Serial number of the electricty meter point. Default: environ['OCTOPUS_ELECTRICITY_SERIAL']
        :param str electricity_mpan: The MPAN of the electricty meter point. Default: environ['OCTOPUS_ELECTRICITY_MPAN']
        :param str electricity_product_code: The product code for the electricity account. Default: environ['OCTOPUS_ELECTRICITY_PRODUCT_CODE']
        :param str electricity_region: The region for the electricity product. Default: environ['OCTOPUS_ELECTRICITY_REGION']
        :param str gas_serial: The Serial number of the gas meter point. Default: environ['OCTOPUS_GAS_SERIAL']
        :param str gas_mprn: The MPRN of the gas meter point. Default: environ['OCTOPUS_GAS_MPRN']
        :param str gas_product_code: The product code for the gas account. Default: environ['OCTOPUS_GAS_PRODUCT_CODE']
        :param str gas_region: The region for the gas product. Default: environ['OCTOPUS_GAS_REGION']
        """        
        self.api_key = api_key or os.environ["OCTOPUS_API_KEY"]
        self.octopus_electricity_serial = electricity_serial or os.environ['OCTOPUS_ELECTRICITY_SERIAL']
        self.octopus_electricity_mpan = electricity_mpan or os.environ['OCTOPUS_ELECTRICITY_MPAN']
        self.ocopus_electricity_product_code = electricity_product_code or os.environ.get("OCTOPUS_ELECTRICITY_PRODUCT_CODE", "AGILE-18-02-21")
        self.octopus_elecricity_region = electricity_region or os.environ.get("OCTOPUS_ELECTRICITY_REGION", "C")

        self.octopus_gas_serial = gas_serial or os.environ['OCTOPUS_GAS_SERIAL']
        self.octopus_gas_mprn = gas_mprn or os.environ['OCTOPUS_GAS_MPRN']
        self.octopus_gas_product_code = gas_product_code or os.environ.get("OCTOPUS_GAS_PRODUCT_CODE", "AGILE-18-02-21")
        self.octopus_gas_region = gas_region or os.environ.get("OCTOPUS_GAS_REGION", "C")

        self.electricity_consumption_units = "kWh"
        self.gas_consumption_units = "m³"
    
    def meter_url(self, resource_type):
        """
        URL for retrieving information about a meter.

        :param ResourceType resource_type: The Type of resource to retrieve, e.g. ResourceType.ELECTRICITY.
        :returns: A URL for retrieving information about a meter.
        :rtype: str
        """
        if resource_type == ResourceType.ELECTRICITY:
            meter_url = f"electricity-meter-points/{self.octopus_electricity_mpan}"
        elif resource_type == ResourceType.GAS:
            meter_url = f"gas-meter-points/{self.octopus_gas_mprn}"
        return f"{self.base_url}/{meter_url}"

    def tariff_url(self, resource_type):
        """
        URL for retrieving tariff information.

        :param ResourceType resource_type: The Type of resource to retrieve, e.g. ResourceType.ELECTRICITY.
        :returns: A URL for retrieving tariff information.
        :rtype: str
        """

        if resource_type == ResourceType.ELECTRICITY:
            tariff_url = f"{self.ocopus_electricity_product_code}/electricity-tariffs/E-1R-{self.ocopus_electricity_product_code}-{self.octopus_elecricity_region}"
        elif resource_type == ResourceType.GAS:
            tariff_url = f"{self.octopus_gas_product_code}/gas-tariffs/E-1R-{self.octopus_gas_product_code}-{self.octopus_gas_region}"

        return f"{self.base_url}/products/{tariff_url}"

    def consumption_url(self, resource_type):
        """
        URL for retrieving consumption data for a meter.

        :param ResourceType resource_type: The Type of resource to retrieve, e.g. ResourceType.ELECTRICITY.
        :returns: A URL for retrieving consumption data for a meter.
        :rtype: str
        """
        if resource_type == ResourceType.ELECTRICITY:
            serial = self.octopus_electricity_serial
        elif resource_type == ResourceType.GAS:
            serial = self.octopus_gas_serial

        return f"{self.meter_url(resource_type)}/meters/{serial}/consumption"

    def date_to_periods(self, dt):
        """
        Calculates the period_from and period_to for the given date.

        E.g. datetime.date(2022, 1, 1) =>
            datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
            datetime.datetime(2022, 1, 1, 23, 30, 0, tzinfo=pytz.utc)

        :param datetime.date dt: The date for which consumption data should be retrieved. e.g. datetime.date(2022, 1, 1)
        :returns: a tuple of dates containing the start and end periods in UTC.
        :rtype: (datetime.datetime, datetime.datetime)
        """
        date_from = datetime.datetime.combine(dt, datetime.datetime.min.time(), tzinfo=pytz.utc)
        date_to = date_from + datetime.timedelta(hours=23, minutes=30)

        # Convert to UTC
        return date_from.astimezone(pytz.utc), date_to.astimezone(pytz.utc)

    def get_data(self, url):
        """
        Makes an API-key authenticated request to the octopus API using the given URL.

        :param str url: The URL to request.
        :returns: A parsed json object of results.
        :rtype: dict
        """
        r = requests.get(url, auth=(self.api_key +':',''))
        return r.json()

    ##############
    # Meter Data #
    ##############

    def get_meter_point(self, resource_type):
        """
        Retrieves information about the meter point.

        e.g.:

        {
            "gsp": "_H",
            "mpan": "2000024512368",
            "profile_class": 1
        }

        :param ResourceType resource_type: The Type of resource to retrieve, e.g. ResourceType.ELECTRICITY.
        :returns: A dictionary containing details of the electricity meter point.
        :rtype: dict
        """
        return self.get_data(self.meter_url(resource_type))

    def get_grid_supply_points(self, postcode=None):
        """
        Retrieves a list of grid supply points.

        e.g.

        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "group_id": "_A"
                },
            ]
        }

        :param str postcode: (optional) A postcode to filter on.
        :returns: A dictionary containing a list of grid supply point objects.
        :rtype: dict
        """
        postcode_str = f"?postcode={postcode}" if postcode is not None else ""
        return self.get_data(f"{self.base_url}/industry/grid-supply-points{postcode_str}")

    ###############
    # Tariff Data #
    ###############

    def get_tariff_data(self, resource_type, charge_type, period_from=None, period_to=None, page_size=100, page=None):
        """
        Makes an API-key authenticated request for tariff data to the octopus API.

        :param ResourceType resource_type: The Type of resource to retrieve, e.g. ResourceType.ELECTRICITY.
        :param ChargeType charge_type: The charge type to retrieve. e.g. ChargeType.STADNING_CHARGES
        :param datetime.datetime period_from: The earliest time period for which unit rates should be retrieved. e.g. datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        :param datetime.datetime period_to: The latest time period for which unit rates should be retrieved. e.g. datetime.datetime(2022, 1, 1, 23, 30, 0, tzinfo=pytz.utc)
        :param int page_size: (optional, default 100) Page size of returned results. Default 100, Max 1,500 to give up to a month of half-hourly prices.
        :param int page: (optional, default None) The page number to load.
        :returns: Tariff information.
        :rtype: dict
        """
        period_from_str = f"&period_from={iso_format(period_from)}" if period_from is not None else ""
        period_to_str = f"&period_to={iso_format(period_to)}" if period_to is not None else ""
        page_str = f"&page={page}" if page is not None else ""
        return self.get_data(f"{self.tariff_url(resource_type)}/{charge_type.value}?page_size={page_size}{page_str}{period_from_str}{period_to_str}")


    ####################
    # Consumption Data #
    ####################

    def get_consumption_for_period(self, resource_type, period_from, period_to, reverse_order=False, page_size=100, page=None, group_by=Aggregate.HALF_HOURLY):
        """
        Retrieves consumption data for the given resource between the given periods.

        :param ResourceType resource_type: The Type of resource to retrieve, e.g. ResourceType.ELECTRICITY.
        :param datetime.datetime period_from: The earliest time period for which consumption data should be retrieved. e.g. datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        :param datetime.datetime period_to: The latest time period for which consumption data should be retrieved. e.g. datetime.datetime(2022, 1, 1, 23, 30, 0, tzinfo=pytz.utc)
        :param bool reverse_order: (optional, default False) Should the results be returned in reverse date order.
        :param int page_size: (optional, default 100) Page size of returned results. Default 100, Max 25,000 to give a full year of harlf-hourly consumption details.
        :param int page: (optional, default None) The page number to load.
        :param Aggregate group_by: (optional, default Aggregate.HALF_HOURLY) Aggregates consumption over a speficied time period.
        :returns: A dictionary object representing consumption data for the resource.
        :rtype: dict
        """
        order = "-period" if reverse_order else "period"
        page_str = f"&page={page}" if page is not None else ""
        group_by_str = f"&group_by={group_by.value}" if group_by != Aggregate.HALF_HOURLY else ""
        return self.get_data(f"{self.consumption_url(resource_type)}?period_from={iso_format(period_from)}&period_to={iso_format(period_to)}&order_by={order}&page_size={page_size}{page_str}{group_by_str}")

    def get_consumption_for_date(self, resource_type, date_from, reverse_order=False, page_size=100, page=None, group_by=Aggregate.HALF_HOURLY):
        """
        Retrieves consumption data for the meter on the given date.

        :param ResourceType resource_type: The Type of resource to retrieve, e.g. ResourceType.ELECTRICITY.
        :param datetime.date date_from: The date for which consumption data should be retrieved. e.g. datetime.datetime(2022, 1, 1)
        :param bool reverse_order: (optional, default False) Should the results be returned in reverse date order.
        :param int page_size: (optional, default 100) Page size of returned results. Default 100, Max 25,000 to give a full year of harlf-hourly consumption details.
        :param int page: (optional, default 1) The page nnumber to load.
        :param Aggregate group_by: (optional, default Aggregate.HALF_HOURLY) Aggregates consumption over a speficied time period.
        :returns: A dictionary object representing consumption data for the resource.
        :rtype: dict
        """
        period_from, period_to = self.date_to_periods(date_from)
        return self.get_consumption_for_period(resource_type, period_from, period_to, reverse_order, page_size, page, group_by)
