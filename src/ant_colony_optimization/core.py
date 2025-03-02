import mesa
from mesa.space import MultiGrid, PropertyLayer


class Model(mesa.Model):
    def __init__(self, size: int, n_ants: int, ant_vision=1, n_foodpile=1):
        super().__init__()
        self.n_ants = n_ants

        food_layer = self.init_food(size, n_ants)
        pheromone_layer = PropertyLayer(
            name="pheromone", width=size, height=size, default_value=0, dtype=int
        )
        self.grid = MultiGrid(
            width=size,
            height=size,
            torus=True,
            property_layers=[food_layer, pheromone_layer],
        )
        self.anthill_pos = (size // 2, size // 2)
        for i in range(n_ants):
            agent = Ant(self)
            (x,) = self.rng.integers(0, self.grid.width, size=1)
            (y,) = self.rng.integers(0, self.grid.height, size=1)
            self.grid.place_agent(agent, (int(x), int(y)))

    def init_food(self, size, n_foodpile=1):
        food_layer = PropertyLayer(
            name="food", width=size, height=size, default_value=0, dtype=int
        )
        n_foodpile = 1
        for _ in range(n_foodpile):
            (x,) = self.rng.integers(0, size, size=1)
            (y,) = self.rng.integers(0, size, size=1)
            food_layer.set_cell((int(x), int(y)), 40)
        return food_layer

    def step(self):
        for agent_class in self.agent_types:
            self.agents_by_type[agent_class].shuffle_do("step")


def dist(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class Ant(mesa.Agent):
    def __init__(self, model, carrying_capacity=1):
        super().__init__(model)
        # TODO @property
        self.food_bag = 0
        self.carrying_capacity = carrying_capacity
        # self.model = model

    def step(self):
        if self.food_bag == 0:
            self.explore()
        elif self.pos == self.model.anthill_pos:
            self.food_bag -= 1
            print(f"Ant {self.unique_id} returned food!")
        else:
            self.return_to_anthill()

    def return_to_anthill(self):
        # #we assume ants remember the way back to the anthill
        # #compute the closet cell to the anthill
        # #which neighboring cell is closest to anthill?
        # neighbor_distances = {}
        # for neighbor_cell in self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False):
        #     neighbor_distances[neighbor_cell] = dist(neighbor_cell, self.anthill_pos)
        # #if there is a tie, choose a random one
        # move_candidates = [k for k, v in neighbor_distances.items() if v == min(neighbor_distances.values())]
        # if len(move_candidates) > 1:
        #     move = self.rng.choice(move_candidates)
        # else:
        #     move = move_candidates[0]
        # self.model.grid.move_agent(self, move)
        pass

    def explore(self):
        # move to a random neighboring cell
        print("position is", type(self.pos), self.pos)
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.rng.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
