import logging
import datetime
import pytz
from octopus_energy_client import OctopusEnergy, ResourceType, ChargeType, Aggregate

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

def meter_data():
    octopus_client = OctopusEnergy()

    ##############
    # Meter Data #
    ##############

    logger.info(octopus_client.get_meter_point(ResourceType.ELECTRICITY))
    logger.info(octopus_client.get_grid_supply_points("SW1A 1AA"))


def tariff_data():
    octopus_client = OctopusEnergy()

    ###############
    # Tariff Data #
    ###############

    logger.info(octopus_client.get_tariff_data(ResourceType.ELECTRICITY, ChargeType.STANDING_CHARGES))
    logger.info(octopus_client.get_tariff_data(ResourceType.ELECTRICITY, ChargeType.DAY_UNIT_RATES))
    logger.info(octopus_client.get_tariff_data(ResourceType.ELECTRICITY, ChargeType.NIGHT_UNIT_RATES))

    logger.info(octopus_client.get_tariff_data(ResourceType.GAS, ChargeType.STANDARD_UNIT_RATES))
    logger.info(octopus_client.get_tariff_data(ResourceType.GAS, ChargeType.STANDING_CHARGES))

    # Paginated results for a month of half-hourly electricity tariff data
    page_size = 100    
    tariff_data = octopus_client.get_tariff_data(
        ResourceType.ELECTRICITY,
        ChargeType.STANDARD_UNIT_RATES,
        period_from=datetime.datetime(2020, 1, 1, tzinfo=pytz.utc),
        period_to=datetime.datetime(2020, 1, 31, tzinfo=pytz.utc),
        page_size=page_size,
    )
    logger.info(tariff_data)

    import math
    result_count = tariff_data['count']
    pages = math.ceil(result_count / page_size)

    for page in range(2, pages+1):
        logger.info(octopus_client.get_tariff_data(
            ResourceType.ELECTRICITY,
            ChargeType.STANDARD_UNIT_RATES,
            period_from=datetime.datetime(2020, 1, 1, tzinfo=pytz.utc),
            period_to=datetime.datetime(2020, 1, 31, tzinfo=pytz.utc),
            page_size=100,
            page=page
        ))


def consumption_data():
    octopus_client = OctopusEnergy()

    ####################
    # Consumption Data #
    ####################

    logger.info(octopus_client.get_consumption_for_date(ResourceType.ELECTRICITY, datetime.date(2022,1,1)))
    logger.info(octopus_client.get_consumption_for_date(ResourceType.GAS, datetime.date(2022,1,1)))

    consumption = octopus_client.get_consumption_for_period(
        ResourceType.ELECTRICITY,
        period_from=datetime.datetime(2022, 1, 1, tzinfo=pytz.utc),
        period_to=datetime.datetime(2022, 1, 14, tzinfo=pytz.utc),
        group_by=Aggregate.DAILY
    )

    logger.info(consumption)

    consumption = octopus_client.get_consumption_for_period(
        ResourceType.GAS,
        period_from=datetime.datetime(2022, 1, 1, tzinfo=pytz.utc),
        period_to=datetime.datetime(2022, 1, 14, tzinfo=pytz.utc),
        group_by=Aggregate.DAILY
    )

    logger.info(consumption)


    # Paginated results for 2 weeks of half-hourly gas consumption
    consumption = octopus_client.get_consumption_for_period(
        ResourceType.GAS,
        period_from=datetime.datetime(2022, 1, 1, tzinfo=pytz.utc),
        period_to=datetime.datetime(2022, 1, 14, tzinfo=pytz.utc),
        page_size=100
    )

    while consumption.get('next'):
        url = consumption.get('next')
        logger.info(url)
        consumption = octopus_client.get_data(consumption.get('next'))


def main():
    meter_data()
    tariff_data()
    consumption_data()

if __name__ == '__main__':
    main()