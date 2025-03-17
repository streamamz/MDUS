from pathlib import Path
import json

setting_path = Path(__file__).resolve().parent.parent.joinpath("setting.json")
setting = open(setting_path,"r")
setting = json.load(setting)