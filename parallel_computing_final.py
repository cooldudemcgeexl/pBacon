# -*- coding: utf-8 -*-

import pandas as pd
import time

def benchmark(func):
    """Custom benchmark decorator"""
    iterations = 100

    def inner(*args, **kwargs):
        elapsed = []
        for i in range(iterations):
            start = time.time()
            ret_val = func(*args,**kwargs)
            end = time.time()
            elapsed.append(end - start)

        avg_time = sum(elapsed)/len(elapsed)

        print(f'{func.__name__} {iterations} iterations:  Avg Elapsed = {avg_time} seconds')  
        return ret_val
    return inner

'''
Below is the sequential version of the shortest path search.
'''

casts = pd.read_csv('casts.csv')
person1 = 'Jack Nance'
person2 = 'Demi Moore'
finalActor = ''
data = pd.DataFrame()

def actorList (actorInput):
  aa = pd.DataFrame()
  movies = pd.DataFrame()
  if(type(actorInput) == str):
    movies = casts[(casts.actor == actorInput)]
    for row in movies.movie:
      aa = aa.append(casts[(casts.movie ==row)])
  else:
    for actors in actorInput.actor:
      movies = casts[(casts.actor == actors)]
      for row in movies.movie:
        aa = aa.append(casts[(casts.movie ==row)])
  return aa

# returnedActors = actorList(person1)
# count = 1
# while finalActor != person2:
#   # print(count)
#   data = pd.DataFrame()
#   for actor in returnedActors.actor:
#     if(actor == person2):
#       finalActor = actor;
#       break;
#     data = data.append(actorList(actor))
#   count = count + 1
#   returnedActors = data


'''
Below is the multi-threaded version of the above code.
'''

from multiprocessing import Process
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import numpy as np

@benchmark
def main():
  person1 = 'Jack Nance'
  person2 = 'Demi Moore'
  finalActor = ''

  returnedActors = actorList(person1)
  count = 1

  executor = ThreadPoolExecutor(max_workers = 1)
  print(returnedActors.size)

  while finalActor != person2:
    
    block = np.array_split(returnedActors, 1)

    returnedActors = pd.DataFrame()
    feedback = pd.DataFrame()

    for data in block:
      returnData = executor.submit(actorList, data)
      feedback = returnData.result()
      returnedActors = returnedActors.append(feedback)
    returnedActors = returnedActors.drop_duplicates(subset=["movie", "actor"], keep='first')  
    for actor in returnedActors.actor:
      if(actor == person2):
        finalActor = actor;
        break;
    print(returnedActors.size)
    count = count + 1
  # print(count)   
  print(finalActor)
  return

if __name__ == '__main__':
  main()