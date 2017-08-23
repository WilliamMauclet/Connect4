from time import localtime


def format_time(timestamp):
    hours = timestamp // 3600
    minutes = (timestamp % 3600) // 60
    seconds = (timestamp % 60) // 1
    return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s\n"


def get_time():
    time_string = str(localtime()[1]) + "M" + \
                  str(localtime()[2]) + "D_" + \
                  str(localtime()[3]) + "h" + \
                  str(localtime()[4]) + "m"
    return time_string
