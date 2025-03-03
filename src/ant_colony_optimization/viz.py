from mesa.visualization import SolaraViz, make_space_component

from ant_colony_optimization.core import Model

model_params = {
    "size": {
        "type": "SliderInt",
        "label": "size:",
        "value": 30,
        "min": 5,
        "max": 30,
        "step": 1,
    },
    "num_ants": {
        "type": "SliderInt",
        "label": "Number of ants:",
        "value": 15,
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "temperature": {
        "type": "SliderFloat",
        "label": "temperature:",
        "value": 2,
        "min": 0,
        "max": 5,
        "step": 0.2,
    },
    "pheromone_exp": {
        "type": "SliderFloat",
        "label": "success exp:",
        "value": 2.1,
        "min": 1,
        "max": 10,
        "step": 0.1,
    },
    "num_food": 50,
    "num_food_sources": {
        "type": "SliderInt",
        "label": "number of food sources:",
        "value": 2,
        "min": 1,
        "max": 10,
        "step": 1,
    },
    "food_decay": {
        "type": "SliderFloat",
        "label": "food decay factor:",
        "value": 0.99,
        "min": 0.75,
        "max": 1.0,
        "step": 0.01,
    },
    "pheromone_max": 100,
    "pheromone_init": 10,
    "pheromone_decay": {
        "type": "SliderFloat",
        "label": "decay factor:",
        "value": 0.8,
        "min": 0.1,
        "max": 1.0,
        "step": 0.05,
    },
}

model = Model()


def agent_portrayal(agent):
    return {
        "color": "tab:blue",
        "size": 50,
    }


property_portrayal = {
    "food": {
        "color": "tab:red",
        # "size": 10,
        "alpha": 0.8,
    },
    "ant_colony": {
        "color": "tab:green",
        "stroke": "blue",
        #   "size": 10,
        "alpha": 0.8,
        "colorbar": False,
    },
    "pheromone": {
        "color": "blue",
        "stroke": "blue",
        # "size": 10,
        "alpha": 0.8,
        "vmin": 0,
        "vmax": model_params["pheromone_max"],
    },
}

SpaceGraph = make_space_component(
    agent_portrayal, propertylayer_portrayal=property_portrayal
)

page = SolaraViz(
    model,
    components=[SpaceGraph],
    model_params=model_params,
    name="ACO",
)
