'''
Effect Variables
'''

# Imports
import numpy as np
from copy import deepcopy

# Main Classes
class EFFECT_TREE_CONNECTION:
    '''
    Effect Connection
    '''
    def __init__(self, start, end, effect, **params):
        self.start = start
        self.end = end
        self.effect = effect # Has ["name", "func", "params", ...]
        self.__dict__.update(params)

    def get_dict(self, transistion=False):
        '''
        Get Dict Data
        '''
        # Init
        d = {}
        # Get
        d["start"] = self.start.id
        d["end"] = self.end.id
        if not transistion:
            d["effect"] = {
                k: deepcopy(self.effect[k]) for k in self.effect.keys() if k != "func"
            }
        else:
            d["effect"] = {
                k: deepcopy(self.effect[k]) for k in self.effect.keys() if k not in ["func", "params"]
            }
            for pk in self.effect["transistion"].keys():
                d["effect"]["transistion"][pk]["transistion"] = {
                    k: d["effect"]["transistion"][pk]["transistion"][k]
                    for k in d["effect"]["transistion"][pk]["transistion"].keys() if k != "func"
                }

        return d

class EFFECT_TREE_NODE:
    '''
    Effect Tree Node
    '''
    def __init__(self, 
        id, 
        parent=None, children=None, 
        I=None, 
        history_length=0,
        **params
        ):
        # Main Params
        self.id = id
        # Connection Params
        self.parent = parent
        self.children = children if children is not None else {}
        # Image Params
        self.I = I
        # Other Params
        ## Count of previous frames to store
        self.history_length = history_length
        # Update Params
        self.__dict__.update(params)
        # Init
        ## History
        self.history = [None for i in range(history_length)]
        if history_length > 0 and I is not None: self.history[-1] = I

    def generate(self, propogate=False):
        '''
        Generate Image by applying effect to parent image
        '''
        # Generate
        if self.parent.effect is not None:
            ## If propogate or parent image not generated, generate parent first
            if propogate or self.parent.start.I is None: self.parent.start.generate(propogate=propogate)
            ## Generate
            other_params = {
                "node": self
            }
            ### Check if combination effect
            self.I = self.parent.effect["func"](self.parent.start.I, **self.parent.effect["params"], **other_params)
        else:
            self.I = self.parent.start.I
        # Update History
        self.updateHistory()

        return self.I

    def updateHistory(self):
        '''
        Update History
        '''
        # Update
        if self.history_length == 0:
            if len(self.history) > 0: self.history = []
            return
        if self.history_length == len(self.history):
            self.history.pop(0)
            self.history.append(self.I)
        elif self.history_length > len(self.history):
            self.history.append(self.I)
        else:
            self.history = self.history[-self.history_length:]

    def delete(self, propogate=False):
        '''
        Delete Node
        '''
        # Init
        deleted_node_ids = []
        # print(self.id, self.parent.start.id, self.children)
        # Remove from Parent and Delete Connection
        if self.parent is not None:
            del self.parent.start.children[self.id]
        # Delete Children and Connections
        if propogate:
            cks = list(self.children.keys())
            for ck in cks:
                deleted_node_ids_child = self.children[ck].end.delete(propogate=propogate)
                deleted_node_ids.extend(deleted_node_ids_child)
        # Delete Self
        deleted_node_ids.append(self.id)
        # del self

        return list(set(deleted_node_ids))
    
    def get_dict(self, children=True, I=False, history=False):
        '''
        Get Dict Data
        '''
        # Init
        d = {}
        # Get
        d["id"] = self.id
        d["parent"] = self.parent.start.id if self.parent is not None else None
        if children: d["children"] = list(self.children.keys())
        if I: d["I"] = self.I.tolist()
        if history:
            d["history_length"] = self.history_length
            d["history"] = [h.tolist() for h in self.history]
        
        return d

# Main Vars
PIXELDATA_DIMENSIONS = 4 # RGB - 3, RGBA - 4
EFFECT_TREE_ROOT_ID = "input"
EFFECT_TREE = {
    "root": EFFECT_TREE_NODE(EFFECT_TREE_ROOT_ID),
    "nodes": {},
    "node_id_counter": 1
}
DISPLAY_GRID = {
    "grid": [["1"]],
    "params": {
        "grid_cell_space": [0, 0],
        "grid_border_space": [0, 0]
    },
    "overall": {
        "grid_size": [1, 1],
        "image_size": [512, 512]
    }
}