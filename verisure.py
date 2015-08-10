""" Command line interface for Verisure MyPages """

from __future__ import print_function
import argparse

from mypages import MyPages
from mypages import (
    SMARTPLUG_ON, SMARTPLUG_OFF,
    ALARM_STATUS_ARMED_HOME, ALARM_STATUS_ARMED_AWAY, ALARM_STATUS_DISARMED,
    DEVICE_ALARM, DEVICE_SMARTPLUG, DEVICE_ETHERNET, DEVICE_CLIMATE
    )

COMMAND_GET = 'get'
COMMAND_SET = 'set'


def print_status(status):
    for device in status:
        print(device.device_type)
        for item in device.__dict__.iteritems():
            print('\t{}: {}'.format(item[0], item[1]))

# pylint: disable=C0103
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Read or change status of verisure devices')
    parser.add_argument(
        'username',
        help='MySite username')
    parser.add_argument(
        'password',
        help='MySite password')

    commandsparser = parser.add_subparsers(
        help='commands',
        dest='command')

    # Get command
    get_parser = commandsparser.add_parser(
        COMMAND_GET,
        help='Read status of one or many device types')
    get_parser.add_argument(
        'devices',
        nargs='+',
        choices=[
            DEVICE_ALARM,
            DEVICE_CLIMATE,
            DEVICE_SMARTPLUG,
            DEVICE_ETHERNET
            ],
        help='Read status for device type',
        default=[])

    # Set command
    set_parser = commandsparser.add_parser(
        COMMAND_SET,
        help='Set status of a device')
    set_device = set_parser.add_subparsers(
        help='device',
        dest='device')

    # Set smartplug
    set_smartplug = set_device.add_parser(
        DEVICE_SMARTPLUG,
        help='set smartplug value')
    set_smartplug.add_argument(
        'serial_number',
        help='serial number')
    set_smartplug.add_argument(
        'new_value',
        choices=[
            SMARTPLUG_ON,
            SMARTPLUG_OFF],
        help='new value')

    # Set alarm
    set_alarm = set_device.add_parser(
        DEVICE_ALARM,
        help='set alarm status')
    set_alarm.add_argument(
        'code',
        help='alarm code')
    set_alarm.add_argument(
        'new_status',
        choices=[
            ALARM_STATUS_ARMED_HOME,
            ALARM_STATUS_ARMED_AWAY,
            ALARM_STATUS_DISARMED],
        help='new status')

    args = parser.parse_args()

    with MyPages(args.username, args.password) as verisure:
        if args.command == COMMAND_GET:
            for device in args.devices:
                if device == DEVICE_ALARM:
                    print_status(verisure.get_alarm_status())
                if device == DEVICE_CLIMATE:
                    print_status(verisure.get_climate_status())
                if device == DEVICE_SMARTPLUG:
                    print_status(verisure.get_smartplug_status())
                if device == DEVICE_ETHERNET:
                    print_status(verisure.get_ethernet_status())
        if args.command == COMMAND_SET:
            if args.device == DEVICE_SMARTPLUG:
                verisure.set_smartplug_status(
                    args.serial_number,
                    args.new_value)
            if args.device == DEVICE_ALARM:
                verisure.set_alarm_status(
                    args.code,
                    args.new_status)
