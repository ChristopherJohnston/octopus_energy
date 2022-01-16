def iso_format(dt):
    """
    Converts a python datetime to an ISO-8601 standard string.

    The Octopus Energy does not accept a string with UTC represented as +00:00, therefore this method replaces
    the "+00:00" for UTC with the "Z" syntax. e.g:
        datetime.datetime(2021, 1, 1, 23, 30, 0, tzinfo=pytz.utc) => "2021-01-01T23:30:00+00:00" => "2021-01-01T23:30:00Z"    

    :param datetime.datetime dt: The datetime to format.
    :returns: An ISO-8601 formatted date string
    :rtype: str
    """
    return dt.isoformat().replace('+00:00', 'Z')
