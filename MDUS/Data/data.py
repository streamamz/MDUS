import pandas as pd
import os
import json

library_dir = os.path.dirname(__file__)

orbit = pd.read_pickle(os.path.join(library_dir, 'orbits.pkl'))
datapath_original = json.load(open(os.path.join(library_dir, 'datapath.json'), 'r'))