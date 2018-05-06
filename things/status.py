import os
import psutil


def convert_bytes(data):
    return float(data/1024/1024/1024)


def load_avg():
    a = os.getloadavg()
    avg = '**Load averages:** {0:.2f}, {1:.2f}, {2:.2f}'.format(a[0], a[1], a[2])
    return avg


def memory():
    m = psutil.virtual_memory()
    total = '{0:.2f}'.format(convert_bytes(m.total))
    used = '{0:.2f}'.format(
        convert_bytes(m.total) * (m.percent/100))

    return '**RAM:** {0}/{1}GB'.format(used, total)


def cpu():
    psutil.cpu_percent(interval=1, percpu=False)
    percentage = '**CPU:** {0}%'.format(
        psutil.cpu_percent(interval=None, percpu=False))

    return percentage
