# -*- coding: utf-8 -*-

"""Weather Underground API wrapper."""

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import json
import re
from logzero import logger

try:
    # Python 3
    import urllib.request
    import urllib
    USE_URLLIB2 = False
except ImportError:
    # Python 2
    import urllib2
    USE_URLLIB2 = True


class WU(object):
    """Weather Underground API wrapper"""

    RE_BRACKET = re.compile(r'\[(.*?)\]')

    BASE_URL = 'http://api.wunderground.com/api/{}/{}/q/{}.json'

    def __init__(self, key):
        """Setup the Weather Underground API wrapper.

        :param str key: The Weather Underground API key.
        :raises TypeError: If the provided argument is not the correct type.
        """
        try:
            # Python 2
            if not isinstance(key, (unicode, str)):
                raise TypeError('key is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(key, str):
                raise TypeError('key is not of type str.')

        self.key = key

        logger.debug('WU(key: %s)', self.key)

    def call_api(self, features, location):
        """Call the Weather Underground API.

        :param list features: List of features to query.
        :param str location: Location to query.
        :return: JSON data.
        :rtype: dict
        :raises TypeError: If the provided argument is not the correct type.
        """
        if not isinstance(features, list):
            raise TypeError('features is not of type list.')
        try:
            # Python 2
            if not isinstance(location, (unicode, str)):
                raise TypeError('location is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(location, str):
                raise TypeError('location is not of type str.')

        logger.debug('WU.call_api('
                     'features: %s, '
                     'location: %s)', features, location)

        feature_str = ''
        for feature in features:
            if feature_str is not '':
                feature_str += '/'
            feature_str += feature
        url = WU.BASE_URL.format(self.key, feature_str, location)
        logger.debug('Calling API using url %s', url)

        # For compatibility with Python 2.
        if USE_URLLIB2:
            query = urllib2.urlopen(url)
        else:
            query = urllib.request.urlopen(url)

        result = json.loads(query.read())
        logger.log(1,
                   'Result:\n%s\n\n',
                   json.dumps(
                       result,
                       indent=2,
                       sort_keys=True))
        query.close()

        return result

    def format_data(self, features, location, template):
        """Query the API and replace the values in the template string.

        :param list features: The API features to query.
        :param str location: The location to query.
        :param str template: The template string that will be formatted.
        :return: Formatted string.
        :rtype: str
        :raises TypeError: If the provided argument is not the correct type.
        """

        if not isinstance(features, list):
            raise TypeError('features is not of type list.')
        try:
            # Python 2
            if not isinstance(location, (unicode, str)):
                raise TypeError('location is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(location, str):
                raise TypeError('location is not of type str.')
        try:
            # Python 2
            if not isinstance(template, (unicode, str)):
                raise TypeError('template is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(template, str):
                raise TypeError('template is not of type str.')

        logger.debug('WU.format_data('
                     'features: %s, '
                     'location: %s, '
                     'template: %s)', features, location, template)

        output = template
        fields = WU.RE_BRACKET.findall(template)

        json_data = self.call_api(features, location)
        json_ok = False

        try:
            errors = json_data['response']['error']
            logger.error('Weather Underground API error: [%s] "%s" ',
                         json_data['response']['error']['type'],
                         json_data['response']['error']['description'])
            json_ok = False
        except KeyError:
            logger.debug('No errors reported by the WU API.')
            json_ok = True

        if json_ok:
            for field in fields:
                logger.debug('Working on field: "%s"', field)
                data = None

                if field.find('display_location_') != -1:
                    subfield = field.replace('display_location_', '')
                    try:
                        data = json_data['current_observation'][
                            'display_location'][subfield]
                    except KeyError:
                        data = None
                else:
                    try:
                        data = json_data['current_observation'][field]
                    except KeyError:
                        data = None

                if data is None:
                    logger.warning('Invalid parameter in template'
                                   ' "%s"', field)
                else:
                    output = output.replace('[{}]'.format(field), str(data))

        return output
