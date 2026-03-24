from utils import translate_states
from streamlit_agraph import Node, Edge, Config

yellow = "#F3FF90"
edge_color = "#BBBBBB"
green = "#9BEC00"

# graph configurations
layout = {
        "randomSeed": 2,
        "improvedLayout": True,
        "clusterThreshold": 10,
        "hierarchical": {
          "enabled":False,
          "levelSeparation": 200,
          "nodeSpacing": 250,
          "treeSpacing": 250,
          "blockShifting": False,
          "edgeMinimization": False,
          "parentCentralization": False,
          "direction": "LR",        # UD, DU, LR, RL
          "sortMethod": "directed",  # hubsize, directed
          "shakeTowards": "roots",  # roots, leaves
      },
    }


# define edges and nodes once
def define_edges(coffee_model, texts):
    edges = []
    for transition in list(coffee_model.transition_probabilities.keys()):
        from_state, command = translate_states(transition, texts)
        states = []
        probs = []
        for probability in list(coffee_model.transition_probabilities[transition].values()):
            probs.append(probability)
        for state in list(coffee_model.transition_probabilities[transition].keys()):
            states.append(state)
        for i in range(len(states)):
            if probs[i] > 0.0:
                id, command = translate_states(states[i], texts)
                edges.append(Edge(from_state, id, label=str(probs[i]), color=edge_color))
    return edges

def define_nodes(coffee_model, texts):
    nodes = []
    for state in coffee_model.states:
        id, command = translate_states(state, texts)
        nodes.append(Node(id, state, color=yellow, size=35))
    return nodes

def define_config(width, height):
    config = Config(height=height, width=width, physics=False, hierarchical=False,)
    config.layout = layout
    config.save("config.json")
    return config