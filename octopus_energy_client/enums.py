from enum import Enum

class ResourceType(Enum):
    """
    Available Resource Types
    """
    GAS = 'gas'
    ELECTRICITY = 'electricity'


class ChargeType(Enum):
    """
    Charge types for electricity and gas tariffs.
    """
    STANDING_CHARGES = "standing-charges"
    STANDARD_UNIT_RATES = "standard-unit-rates"
    DAY_UNIT_RATES = "day-unit-rates"
    NIGHT_UNIT_RATES = "night-unit-rates"


class Aggregate(Enum):
    """
    Aggregation options for electricity and gas consumption data.
    """
    HALF_HOURLY = None
    HOURLY = "hour"
    DAILY = "day"
    WEEKLY = "week"
    MONTHLY = "month"
    QUARTERLY = "quarter"
