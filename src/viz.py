from aco import Model, Ant
from mesa.visualization import SolaraViz, make_space_component

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

SpaceGraph = make_space_component(agent_portrayal)

page = SolaraViz(
    model,
    components=[SpaceGraph],
    model_params=model_params,
    name="ACO",
)
#page