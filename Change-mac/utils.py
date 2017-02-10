import random
import subprocess


def set_mac(interface, mac):
    cmd = "ifconfig {} down hw ether {}".format(interface, mac)
    subprocess.call(cmd.split())
    cmd = "ifconfig {} up".format(interface)
    subprocess.call(cmd.split())


def set_random_mac(interface):
    v = random.SystemRandom().choice((
        (0x00, 0x05, 0x69),
        (0x00, 0x50, 0x56),
        (0x00, 0x0C, 0x29),
        (0x00, 0x16, 0x3E),
        (0x00, 0x03, 0xFF),
        (0x00, 0x1C, 0x42),
        (0x00, 0x0F, 0x4B),
        (0x08, 0x00, 0x27))
    )

    mac = [
        v[0],
        v[1],
        v[2],
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    mac[0] |= 2
    mac = ':'.join('{0:02X}'.format(octet) for octet in mac)
    set_mac(interface, mac)


def reset_mac(interface):
    cmd = "ethtool -P {}".format(interface)
    mac = str(subprocess.check_output(cmd.split()), encoding="utf-8")
    mac = mac.split()[-1]
    set_mac(interface, mac)
