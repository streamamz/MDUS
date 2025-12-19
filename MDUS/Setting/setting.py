import json
import inspect
import os

caller_dir = os.path.dirname(os.path.abspath(inspect.stack()[1].filename))
caller_dir = os.path.join(caller_dir, "datapath.json")
def load_datapath_json():
    setting = open(caller_dir,"r")
    setting = json.load(setting)
    return setting

# とりあえず用
def reload_setting():
    global setting
    setting = load_datapath_json()
    print("Reloaded datapath setting from datapath.json")