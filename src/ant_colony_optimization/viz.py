from mesa.visualization import SolaraViz, make_space_component

from ant_colony_optimization.core import Model

model_params = {
    "size": 5,
    "n_ants": 10,
    "ant_vision": 1,
    "n_foodpile": 1,
}

model = Model(**model_params)


def agent_portrayal(agent):
    return {
        "color": "tab:blue",
        "size": 50,
    }


property_portrayal = {
    "food": {
    "color": "tab:red",
   # "size": 10,
    "alpha": 0.8
    },
    "ant_colony": {
        "color": "tab:green",
     #   "size": 10,
        "alpha": 0.8
    }
}

SpaceGraph = make_space_component(agent_portrayal, propertylayer_portrayal=property_portrayal)

page = SolaraViz(
    model,
    components=[SpaceGraph],
    model_params=model_params,
    name="ACO",
)
page

