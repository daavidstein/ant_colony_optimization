from mesa.batchrunner import batch_run
from ant_colony_optimization.core import Model
import numpy as np
import pandas as pd
import multiprocessing as mp

SEED = 1

def main():

    pher_decay = np.linspace(0.75, 1, 5)
    food_decay = np.linspace(0.75, 1, 5)
    temperature = np.linspace(0, 3, 5)

    params = dict(
        pheromone_decay = pher_decay,
        food_decay = food_decay,
        temperature = temperature,
        size = 30,
        seed = [1,2]
    )

    print(f"cpu count: {mp.cpu_count() = }")
    results = batch_run(
        Model,
        parameters=params,
        iterations=1,
        max_steps=2000,
        number_processes=mp.cpu_count() - 1,
        data_collection_period=-1, #data collection period = 1 doesn't work
        display_progress=True,
    )
    print(results[0].keys())
    results_df = pd.DataFrame(results)
    results_df.to_csv("ant_batch.csv")

if __name__ == "__main__":
    main()