'''
Parser Utils for Streamlit UI
'''

# Imports
import numpy as np

# Main Vars
LIST_SEPARATORS = [',', ';', '\n']

# Main Functions
def ListParser(data, data_type=str):
    parsed_data = []
    for r in LIST_SEPARATORS:
        data = data.replace(r, ';')
    parsed_data = np.array(list(map(data_type, data.split(';'))))
    return parsed_data

# Driver Code