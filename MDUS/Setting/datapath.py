# setting for datapath.json
from MDUS.Data.data import datapath_original as dpo
import json
import os
import inspect

caller_dir = os.path.dirname(os.path.abspath(inspect.stack()[1].filename))
library_dir = os.path.dirname(__file__)

def chech_datapath_json():
    if not os.path.exists(os.path.join(caller_dir, 'datapath.json')):
        print("datapath.json file is missing")
        print("create a new datapath.json file")
        with open(os.path.join(caller_dir, 'datapath.json'), 'w') as f:
            json.dump(dpo, f, indent=4)
    else:
        with open(os.path.join(caller_dir, 'datapath.json'), 'r') as f:
            datapath_exist = json.load(f)
        diff = set(dpo.keys()) - set(datapath_exist.keys())
        if len(diff) > 0:
            print("datapath.json file is missing some keys")
            print("update datapath.json file")
            for key in diff:
                datapath_exist[key] = dpo[key]
            with open(os.path.join(caller_dir, 'datapath.json'), 'w') as f:
                json.dump(datapath_exist, f, indent=4)
            print("datapath.json file is updated")
            print("Please reload MDUS")
