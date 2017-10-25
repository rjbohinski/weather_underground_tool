# -*- coding: utf-8 -*-

"""Console script for Weather Underground to get the current weather."""

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import argparse

import logging
import logzero
from logzero import logger

from weather_underground_tool.weather_underground_tool import WU
# from weather_underground_tool import WU


DEFAULT_VERBOSITY = 0
DEFAULT_FILE_NAME = 'secret.txt'
DEFAULT_LOCATION = 'PA/Philadelphia'
DEFAULT_TEMPLATE = 'Current weather in [display_location_full]:\n' \
                   '    Weather:     [weather]\n' \
                   '    Temperature: [temp_f] F'


def setup_logging(verbose, quiet):
    """Setup logging level.

    :param int verbose: How verbose the logging should be.
    :param bool quiet: Log only error messages.
    :return: The logging level set.
    :rtype: int
    """
    logging_level = logging.WARNING

    if quiet:
        logging_level = logging.ERROR
    else:
        if verbose >= 3:
            logging_level = 1
        elif verbose == 2:
            logging_level = logging.DEBUG
        elif verbose == 1:
            logging_level = logging.INFO

    logzero.loglevel(logging_level)
    return logging_level


def load_key(file_name=DEFAULT_FILE_NAME):
    """Load the API key from the file.

    :param str file_name: The key file name.
    :return: The key.
    :rtype: str
    :raises IOError: If the file could not be read or is empty.
    """
    key = None
    with open(file_name, 'r') as key_file:
        key = key_file.read().strip()

    if key is None:
        raise IOError()
    return key


def main():
    """Console script for Weather Underground API."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--template',
        type=str,
        action='store',
        default=DEFAULT_TEMPLATE,
        help='The output format to use. '
             'Fields are identified by square brackets. '
             'For example, to print the temperature use the following: '
             '"Temperature: [temp_f] °F".'
             'The default template is "{}"'.format(DEFAULT_TEMPLATE))
    parser.add_argument(
        '-l',
        '--location',
        type=str,
        action='store',
        default=DEFAULT_LOCATION,
        help='Location used for weather query.'
             'The default location is "{}"'.format(DEFAULT_LOCATION))
    parser.add_argument(
        '-k',
        '--key-file',
        type=str,
        default=DEFAULT_FILE_NAME,
        help='Weather Underground API Key file.'
             ' Default file used is "{}".'.format(DEFAULT_FILE_NAME))
    parser.add_argument(
        '-K',
        '--key',
        type=str,
        default=None,
        help='Weather Underground API Key.'
             ' It is strongly recommended to not use this argument as the '
             'key will be stored in your command history.')
    group_log = parser.add_mutually_exclusive_group()
    group_log.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=DEFAULT_VERBOSITY,
        help='Increase logging level.'
             ' By default only logs warnings and errors.')
    group_log.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='Log errors only.')

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)
    key = None
    if args.key is not None and args.key is not '':
        key = args.key.strip()
    else:
        try:
            key = load_key(args.key_file)
        except IOError:
            logger.error("Weather Underground API key not found!")
            logger.error("Either save it in a file and point to the location"
                         " with --key-file or supply it with --key.")

    if key is not None:
        wu_api = WU(key)

        print(wu_api.format_data(['conditions'], args.location, args.template))


if __name__ == '__main__':
    main()
