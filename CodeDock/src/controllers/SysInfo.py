import platform

def osInfo():
    return platform.system(),platform.architecture()[0]

def screenInfo():
    monitor=screeninfo.get_monitors()
    return monitor[0].width,monitor[0].height
 