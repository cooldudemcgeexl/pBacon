import time
import numba.typed
import pandas as pd
from numba import jit, typed, types


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

def read_casts(casts_array):
    actors = dict()
    movies = dict()
    for row in casts_array:
        actor = row[2]
        movie = row[1][2:]
        if actor not in actors:
            actors[actor] = [movie] 
        else:
            actors[actor].append(movie)
        if movie not in movies:
            movies[movie] = [actor]   
        else:
            movies[movie].append(actor)
    
    return movies, actors


@benchmark
def get_neighbors(parent_actor, actors, movies):
    neighbors = set()
    for movie in movies[parent_actor]:
        for actor in actors[movie]:
            if actor != parent_actor:
                neighbors.add(actor)
    return neighbors


def read_casts_csv():
    casts = pd.read_csv('casts.csv')
    casts = casts.loc[casts['actor'].str.len() > 5]
    return casts.to_numpy()


def main():
    casts_ndarray= read_casts_csv()
    actors, movies = read_casts(casts_ndarray)
    print(get_neighbors('Barbra Streisand', actors, movies))


if __name__ == "__main__":
    main()