# Octopus Energy

A Python API for retrieving Octopus Energy data.

See [https://developer.octopus.energy/docs/api/](https://developer.octopus.energy/docs/api/) for more details of the Octopus API.

## Installation

```shell
pip install octopus-energy-client
```

## Features

* Retrieve information about electricity and gas meters.
* Retrieve tariff data, including half-hourly rates for the octopus agile electricity plan.
* Retrieve consumption data from electricity and gas meters, including up to half-hourly intervals.

## Examples

```python
import math
from octopus_energy_client import OctopusEnergy, ResourceType, ChargeType, Aggregate

# Account API Key, Serials, MPAN/MPRN and Product Codes can be found at https://octopus.energy/dashboard/developer/
octopus_client = OctopusEnergy(
    api_key={octopus_api_key},
    electricity_serial={octopus_electricity_serial},
    electricity_mpan={octopus_electricity_mpan},
    electricity_product_code={octopus_electricity_product_code},
    electricity_region={octopus_electricity_region},
    gas_serial={octopus_gas_serial},
    gas_mprn={octopus_gas_mprn},
    gas_product_code={octopus_gas_product_code},
    gas_region={octopus_gas_region},
)

##############
# Meter Data #
##############

electricity_meter_info = octopus_client.get_meter_point(ResourceType.ELECTRICITY)
# {'gsp': '_C', 'mpan': '0123456789012', 'profile_class': 1}

grid_supply_points = octopus_client.get_grid_supply_points("SW1A 1AA")
# {'count': 1, 'next': None, 'previous': None, 'results': [{'group_id': '_C'}]}

###############
# Tariff Data #
###############

gas_standard_rates = octopus_client.get_tariff_data(ResourceType.GAS, ChargeType.STANDARD_UNIT_RATES)
gas_standing_charges = octopus_client.get_tariff_data(ResourceType.GAS, ChargeType.STANDING_CHARGES)

electricity_standing_charges = octopus_client.get_tariff_data(ResourceType.ELECTRICITY, ChargeType.STANDING_CHARGES)
# {'count': 1, 'next': None, 'previous': None, 'results': [{'value_exc_vat': 20.0, 'value_inc_vat': 21.0, 'valid_from': '2017-01-01T00:00:00Z', 'valid_to': None}]}

electricity_day_rates = octopus_client.get_tariff_data(ResourceType.ELECTRICITY, ChargeType.DAY_UNIT_RATES)
# {'detail': 'This tariff has standard rates, not day and night.'}

electricity_night_rates = octopus_client.get_tariff_data(ResourceType.ELECTRICITY, ChargeType.NIGHT_UNIT_RATES)
# {'detail': 'This tariff has standard rates, not day and night.'}

# Paginated results for a month of half-hourly electricity tariff data
page_size = 100    
tariff_data = octopus_client.get_tariff_data(
    ResourceType.ELECTRICITY,
    ChargeType.STANDARD_UNIT_RATES,
    period_from=datetime.datetime(2020, 1, 1, tzinfo=pytz.utc),
    period_to=datetime.datetime(2020, 1, 31, tzinfo=pytz.utc),
    page_size=page_size,
)


result_count = tariff_data['count']
pages = math.ceil(result_count / page_size)

for page in range(2, pages+1):
    tariff_data = octopus_client.get_tariff_data(
        ResourceType.ELECTRICITY,
        ChargeType.STANDARD_UNIT_RATES,
        period_from=datetime.datetime(2020, 1, 1, tzinfo=pytz.utc),
        period_to=datetime.datetime(2020, 1, 31, tzinfo=pytz.utc),
        page_size=100,
        page=page
    ))

####################
# Consumption Data #
####################

electricity_consumption = octopus_client.get_consumption_for_date(ResourceType.ELECTRICITY, datetime.date(2022,1,1))
gas_consumption = octopus_client.get_consumption_for_date(ResourceType.GAS, datetime.date(2022,1,1))

consumption = octopus_client.get_consumption_for_period(
    ResourceType.ELECTRICITY,
    period_from=datetime.datetime(2022, 1, 1, tzinfo=pytz.utc),
    period_to=datetime.datetime(2022, 1, 14, tzinfo=pytz.utc),
    group_by=Aggregate.DAILY
)

consumption = octopus_client.get_consumption_for_period(
    ResourceType.GAS,
    period_from=datetime.datetime(2022, 1, 1, tzinfo=pytz.utc),
    period_to=datetime.datetime(2022, 1, 14, tzinfo=pytz.utc),
    group_by=Aggregate.DAILY
)

# Paginated results for 2 weeks of half-hourly gas consumption
consumption = octopus_client.get_consumption_for_period(
    ResourceType.GAS,
    period_from=datetime.datetime(2022, 1, 1, tzinfo=pytz.utc),
    period_to=datetime.datetime(2022, 1, 14, tzinfo=pytz.utc),
    page_size=100
)

while consumption.get('next'):
    url = consumption.get('next')
    consumption = octopus_client.get_data(consumption.get('next'))

```
