#! /usr/bin/python3

import argparse
import os
import sys

from utils import set_mac, set_random_mac, reset_mac


parser = argparse.ArgumentParser(
    usage="sudo {} [-h] (-s [INTERFACE] [MAC-ADDR] | -r [INTERFACE] | -R [INTERFACE])".format(sys.argv[0]),
    description="Script to change your MAC address")

if os.getuid() != 0:
    print("Run as root")
    parser.print_usage()
    sys.exit(0)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--set", nargs=2, metavar=("[INTERFACE]", "[MAC-ADDR]"), help="Sets the given mac address")
group.add_argument("-r", "--randomise", metavar="[INTERFACE]", help="Sets a random MAC address")
group.add_argument("-R", "--reset", metavar="[INTERFACE]", help="Reset the MAC address")
args = parser.parse_args()

if args.set:
    set_mac(args.set[0], args.set[1])

elif args.randomise:
    set_random_mac(args.randomise)

elif args.reset:
    reset_mac(args.reset)
