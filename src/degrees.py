import time

import numba.typed
import pandas as pd
from numba import jit

movies = {}
actors = {}
def benchmark(func):
    """Custom benchmark decorator"""
    iterations = 1000
    def inner(*args, **kwargs):
        elapsed = []
        for i in range(iterations):
            start = time.time()
            ret_val = func(*args,**kwargs)
            end = time.time()
            elapsed.append(end - start)

        avg_time = sum(elapsed)/len(elapsed)

        print(f'{func.__name__} {iterations} iterations:  Avg Elapsed = {avg_time}')  
        return ret_val
    return inner

def read_casts():
    casts = pd.read_csv('casts.csv')

    casts = casts.loc[casts['actor'].str.len() > 5]

    for index, row in casts.iterrows():
        actor = row['actor']
        movie = row['movie'][2:]
        if actor not in movies:
            movies[actor] = []
        if movie not in actors:
            actors[movie] = []
        
        movies[actor].append(movie)
        actors[movie].append(actor)

    
    return movies, actors

@benchmark
@jit(nopython=True)
def get_neighbors(parent_actor):
    neighbors = set()
    for movie in movies[parent_actor]:
        for actor in actors[movie]:
            if actor != parent_actor:
                neighbors.add(actor)
    return neighbors



def main():
    actors, movies = read_casts()
    print(get_neighbors('Barbra Streisand'))


if __name__ == "__main__":
    main()