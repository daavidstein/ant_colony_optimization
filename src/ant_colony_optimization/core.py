import mesa
import numpy as np
from mesa.space import MultiGrid, SingleGrid, PropertyLayer
from collections import deque

def dist(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class PheromoneLayer(PropertyLayer):
    propertylayer_experimental_warning_given = True

    def __init__(self, size, max_val=20, init_val=2, decay_factor=0.9, exp=2):
        super().__init__(
            name="pheromone",
            width=size,
            height=size,
            default_value=init_val,
            dtype=np.int32,
        )
        self.exp = exp
        self.max_val = max_val
        self.init_val = init_val
        self.decay_factor = decay_factor

    def amount(self, positions):
        return np.array([self.data[x] for x in positions])

    def decay(self):
        self.modify_cells(lambda x: x * self.decay_factor)

    def drop(self, pos, val = None, const = 1):
        
        if val:
            val = 1 + val
            self.modify_cell(pos, lambda x: min(x + val**self.exp, self.max_val))
        else:
            self.modify_cell(pos, lambda x: x + const)



class FoodLayer(PropertyLayer):
    propertylayer_experimental_warning_given = True

    def __init__(self, size, random, n_food=40, num_sources=2):
        super().__init__(
            name="food", width=size, height=size, default_value=False, dtype=np.int32
        )
        self.n_food = n_food
        self.num_food_sources = num_sources
        for _ in range(num_sources):
            cells = self.select_cells(lambda x: x == 0)
            pos = random.choice(cells)
            self.set_cell(pos, n_food)

    def take(self, pos):
        val = self.data[pos]
        if val > 0:
            #self.set_cell(pos, val - 1)
            return True
        return False


class Model(mesa.Model):
    def __init__(
        self,
        size=11,
        num_ants=10,
        temperature=1,
        num_food=40,
        num_food_sources=2,
        food_decay=0.99,
        pheromone_exp=1.2,
        pheromone_max=20,
        pheromone_init=4,
        pheromone_decay=0.99,
    ):
        super().__init__()
        self.size = size
        self.home = (size // 2, size // 2)
        self.food = FoodLayer(
            size, self.random, n_food=num_food, num_sources=num_food_sources
        )
        self.pheromone = PheromoneLayer(
            size=size,
            exp=pheromone_exp,
            max_val=pheromone_max,
            init_val=pheromone_init,
            decay_factor=pheromone_decay,
        )
        ant_colony = PropertyLayer(
            name="ant_colony", width=size, height=size, default_value=False, dtype=bool
        )
        ant_colony.set_cell(self.home, True)
        self.grid = MultiGrid(
            width=size,
            height=size,
            torus=False,
            property_layers=[self.food, self.pheromone, ant_colony],
        )
        for i in range(num_ants):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(
                Ant(self, temperature=temperature, food_decay=food_decay), (x, y)
            )

    def step(self):
        self.pheromone.decay()
        for agent_class in self.agent_types:
            self.agents_by_type[agent_class].shuffle_do("step")


class Ant(mesa.Agent):
    def __init__(self, model, temperature=1, food_decay=0.9):
        super().__init__(model)
        self.pheromone = self.model.pheromone
        self.temperature = temperature
        self.decay = food_decay
        self.food = 0
        self.history = deque(maxlen=self.model.size // 2)

    @property
    def neighbors(self):
        neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        #don't return to a location you just left
        eligible_neighbors = tuple(pos for pos in neighbors if pos not in self.history)
        #eligible_neighbors = tuple(pos for pos in eligible_neighbors if self.model.grid.is_cell_empty(pos))
        return eligible_neighbors

    def step(self):
        #print(f"{self.unique_id} at {self.pos}")
        if self.pos == self.model.home:
            self.food = 0
        elif self.food == 0 and self.model.food.take(self.pos):
            self.food += 1
        #self.pheromone.drop(self.pos, self.food)
        self.pheromone.drop(self.pos)

        if self.neighbors:
            if self.food > 0:
                self.food *= self.decay
                pos = sorted(self.neighbors, key=lambda x: dist(x, self.model.home))[0]
            else:
                wts = self.pheromone.amount(self.neighbors)
                print(wts)
                if self.temperature > 0:
                    wts = np.exp(wts / self.temperature)
                wts = wts / wts.sum()
                (pos,) = self.random.choices(self.neighbors, wts)

            self.history.append(self.pos)
            self.model.grid.move_agent(self, tuple(pos))
        else:
            self.history.append((np.inf, np.inf))

#does the pheremone ever decay to zero?
