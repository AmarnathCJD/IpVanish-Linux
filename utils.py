import os
import psutil
from asyncio import sleep
import termcolor
import time


def is_openvpn_installed():
    return os.system("openvpn --version") == 0


async def get_network_speed(interface='wlp4s0', interval=1):
    net_io_start = psutil.net_io_counters(pernic=True).get(interface)

    if net_io_start is None:
        raise ValueError(f"Network interface {interface} not found")

    await sleep(interval)

    net_io_end = psutil.net_io_counters(pernic=True).get(interface)

    if net_io_end is None:
        raise ValueError(f"Network interface {interface} not found")

    bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
    bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv

    bps_sent = bytes_sent / interval
    bps_recv = bytes_recv / interval

    return human_readable_size(bps_recv), human_readable_size(bps_sent)


def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.2f} {unit}"


def fmt_to_log(msg, level='info'):
    return "{}: {} - {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), level, msg)


def log_info(message):
    print(termcolor.colored(fmt_to_log(message, 'info'), 'green'))


def log_error(message):
    print(termcolor.colored(fmt_to_log(message, 'error'), 'red'))


def log_warn(message):
    print(termcolor.colored(fmt_to_log(message, 'warn'), 'yellow'))
