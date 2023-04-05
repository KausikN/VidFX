'''
Set of tools for video editing and fun video effects
'''

# Imports
from EffectsLibrary.EffectsLibrary import *
from Utils.EffectTransistionUtils import *

# Main Vars


# Main Functions
# Tree Cache Conversion Functions
def EffectTreeCache_Tree2Dict(EFFECT_TREE, transistion=False):
    '''
    Converts EffectTree Cache Data in tree format to dict format
    '''
    # Init
    EFFECT_TREE_DATA = {
        "root": EFFECT_TREE["root"].get_dict(children=False),
        "nodes": {k: EFFECT_TREE["nodes"][k].get_dict(children=False) for k in EFFECT_TREE["nodes"].keys()},
        "node_id_counter": EFFECT_TREE["node_id_counter"],
        "connections": {}
    }
    # Save Connections
    for k in EFFECT_TREE["nodes"].keys():
        EFFECT_TREE_DATA["connections"][k] = EFFECT_TREE["nodes"][k].parent.get_dict(transistion=transistion)
    OUTPUT = {
        "EFFECT_TREE": EFFECT_TREE_DATA
    }
    return OUTPUT

def EffectTreeCache_Dict2Tree(DICT_DATA, transistion=False):
    '''
    Converts EffectTree Cache Data in dict format to tree format
    '''
    # Init
    EFFECT_TREE_DATA = DICT_DATA["EFFECT_TREE"]
    # Create Nodes
    EFFECT_TREE = {
        "root": EFFECT_TREE_NODE(EFFECT_TREE_DATA["root"]["id"]),
        "nodes": {},
        "node_id_counter": EFFECT_TREE_DATA["node_id_counter"]
    }
    ## Create Initial Nodes
    for k in EFFECT_TREE_DATA["nodes"].keys(): EFFECT_TREE["nodes"][k] = EFFECT_TREE_NODE(k)
    ## Create Connections
    CONNECTIONS = {}
    for k in EFFECT_TREE_DATA["connections"].keys():
        conn_data = EFFECT_TREE_DATA["connections"][k]
        ## Get Effect Data
        EFFECT_FUNC_DATA = conn_data["effect"]
        EFFECT_FUNC_DATA["func"] = AVAILABLE_EFFECTS[EFFECT_FUNC_DATA["name"]]["func"]
        if transistion:
            for pk in EFFECT_FUNC_DATA["transistion"].keys(): EFFECT_FUNC_DATA["transistion"][pk]["transistion"]["func"] = TRANSISTION_FUNCS[EFFECT_FUNC_DATA["transistion"][pk]["transistion"]["name"]]["func"]
        ## Create Connection
        START_NODE = EFFECT_TREE["root"] if conn_data["start"] not in EFFECT_TREE["nodes"].keys() else EFFECT_TREE["nodes"][conn_data["start"]]
        END_NODE = EFFECT_TREE["nodes"][conn_data["end"]]
        CONNECTIONS[k] = EFFECT_TREE_CONNECTION(
            START_NODE, END_NODE, 
            EFFECT_FUNC_DATA,
            effect_tree_pointer=EFFECT_TREE # Pass Effect Tree Pointer
        )
    ## Connect Nodes
    for k in CONNECTIONS.keys():
        conn = CONNECTIONS[k]
        if conn.start.id == EFFECT_TREE["root"].id:
            EFFECT_TREE["root"].children[conn.end.id] = conn
        else:
            EFFECT_TREE["nodes"][conn.start.id].children[conn.end.id] = conn
        EFFECT_TREE["nodes"][conn.end.id].parent = conn
    
    OUTPUT = {
        "EFFECT_TREE": EFFECT_TREE
    }
    return OUTPUT