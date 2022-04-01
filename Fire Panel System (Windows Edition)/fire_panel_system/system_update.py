from bs4 import *

path = "C:/Users/Neeraj Chekutty/Desktop/SDP/Website/website/_includes/"
parser = "html.parser"

def update_html(output, file_name):
    with open(path + file_name,"w") as file:
        file.write(str(output))

def system_off():
    with open(path + "fire_panel_status.html") as fps, open(path + "fred_status.html") as fs, open(path + "app_link_status.html") as als,  open(path + "live_status.html") as ls, open(path + "live_status_link.html") as lsl, open(path + "warnings.html") as warnings, open(path + "sys_network.html") as sys_network:
        fps_raw = BeautifulSoup(fps, parser)
        fs_raw = BeautifulSoup(fs, parser)
        als_raw = BeautifulSoup(als, parser)
        ls_raw = BeautifulSoup(ls, parser)
        lsl_raw = BeautifulSoup(lsl, parser)
        warnings_raw = BeautifulSoup(warnings, parser)
        sys_network_raw = BeautifulSoup(sys_network, parser)

    fps_raw.find(id="fire_panel_status").string = "Fire Panel: OFF"
    fps_raw.find(id="fps")["class"] = "card bg-danger"

    fs_raw.find(id="fred_status").string = "F.R.E.D: ACTIVE"
    fs_raw.find(id="fs")["class"] = "card bg-success"

    als_raw.find(id="app_link_status").string = "App Link: ACTIVE"
    als_raw.find(id="als")["class"] = "card bg-success"

    ls_raw.find(id="live_status")["hidden"] = "hidden"
    lsl_raw.find(id="live_status_link")["hidden"] = "hidden"

    warnings_raw.find(id="warnings").string = "Warnings: 1"
    warnings_raw.find(id="warnings_card")["class"] = "card bg-danger"

    sys_network_raw.find(id="sys_network").string = "System Network: ERROR"
    sys_network_raw.find(id="sys_network_card")["class"] = "card bg-danger"

    for x in [(fps_raw, "fire_panel_status.html"),(fs_raw, "fred_status.html"), (als_raw, "app_link_status.html"), (ls_raw, "live_status.html"), (lsl_raw, "live_status_link.html"), (warnings_raw, "warnings.html"), (sys_network_raw, "sys_network.html")]:
        update_html(str(x[0]), x[1])

def system_on():
    with open(path + "fire_panel_status.html") as fps, open(path + "warnings.html") as warnings, open(path + "sys_network.html") as sys_network:
        fps_raw = BeautifulSoup(fps, parser)
        warnings_raw = BeautifulSoup(warnings, parser)
        sys_network_raw = BeautifulSoup(sys_network, parser)

    fps_raw.find(id="fire_panel_status").string = "Fire Panel: ACTIVE"
    fps_raw.find(id="fps")["class"] = "card bg-success"

    warnings_raw.find(id="warnings").string = "Warnings: NONE"
    warnings_raw.find(id="warnings_card")["class"] = "card bg-success"

    sys_network_raw.find(id="sys_network").string = "System Network: OK"
    sys_network_raw.find(id="sys_network_card")["class"] = "card bg-success"

    for x in [(fps_raw, "fire_panel_status.html"), (warnings_raw, "warnings.html"), (sys_network_raw, "sys_network.html")]:
        update_html(str(x[0]), x[1])

def raise_alarm(location):
    with open(path + "fred_status.html") as fs, open(path + "app_link_status.html") as als,  open(path + "live_status.html") as ls, open(path + "live_status_link.html") as lsl:
        fs_raw = BeautifulSoup(fs, parser)
        als_raw = BeautifulSoup(als, parser)
        ls_raw = BeautifulSoup(ls, parser)
        lsl_raw = BeautifulSoup(lsl, parser)

    fs_raw.find(id="fred_status").string = "F.R.E.D: IN USE"
    fs_raw.find(id="fs")["class"] = "card bg-warning"

    als_raw.find(id="app_link_status").string = "App Link: IN USE"
    als_raw.find(id="als")["class"] = "card bg-warning"

    del ls_raw.find(id="live_status")["hidden"]
    ls_raw.find(id="fire_location").string = "Fire Identified: " + location
    ls_raw.find(id="fred_activity").string = "F.R.E.D " + location + " : EXPLORING..."

    del lsl_raw.find(id="live_status_link")["hidden"]

    for x in [(fs_raw, "fred_status.html"), (als_raw, "app_link_status.html"), (lsl_raw, "live_status_link.html"), (ls_raw, "live_status.html")]:
        update_html(str(x[0]), x[1])

def raise_fault():
    with open(path + "fire_panel_status.html") as fps, open(path + "warnings.html") as warnings, open(path + "sys_network.html") as sys_network:
        fps_raw = BeautifulSoup(fps, parser)
        warnings_raw = BeautifulSoup(warnings, parser)
        sys_network_raw = BeautifulSoup(sys_network, parser)

    fps_raw.find(id="fire_panel_status").string = "Fire Panel: INACTIVE"
    fps_raw.find(id="fps")["class"] = "card bg-danger"

    warnings_raw.find(id="warnings").string = "Warnings: 1"
    warnings_raw.find(id="warnings_card")["class"] = "card bg-danger"

    sys_network_raw.find(id="sys_network").string = "System Network: ERROR"
    sys_network_raw.find(id="sys_network_card")["class"] = "card bg-danger"

    for x in [(fps_raw, "fire_panel_status.html"), (warnings_raw, "warnings.html"), (sys_network_raw, "sys_network.html")]:
        update_html(str(x[0]), x[1])

def reset_alarm():
    with open(path + "fred_status.html") as fs, open(path + "app_link_status.html") as als,  open(path + "live_status.html") as ls, open(path + "live_status_link.html") as lsl:
        fs_raw = BeautifulSoup(fs, parser)
        als_raw = BeautifulSoup(als, parser)
        ls_raw = BeautifulSoup(ls, parser)
        lsl_raw = BeautifulSoup(lsl, parser)

    fs_raw.find(id="fred_status").string = "F.R.E.D: ACTIVE"
    fs_raw.find(id="fs")["class"] = "card bg-success"

    als_raw.find(id="app_link_status").string = "App Link: ACTIVE"
    als_raw.find(id="als")["class"] = "card bg-success"

    ls_raw.find(id="live_status")["hidden"] = "hidden"

    lsl_raw.find(id="live_status_link")["hidden"] = "hidden"

    for x in [(fs_raw, "fred_status.html"), (als_raw, "app_link_status.html"), (ls_raw, "live_status.html"), (lsl_raw, "live_status_link.html")]:
        update_html(str(x[0]), x[1])