import time
from functools import wraps


def benchmark(iterations=1):
    def bench_wrapper(fun): 
        @wraps(fun)
        def ret_fun(*args,**kwargs):
            elapsed = []
            for _ in range(iterations):
                start = time.time()
                ret_val = fun(*args,**kwargs)
                end = time.time()
                elapsed.append(end - start)

            avg_time = sum(elapsed)/len(elapsed)

            print(f'{fun.__name__} {iterations} iterations:  Avg Elapsed = {avg_time}')  
            return ret_val
        return ret_fun
    return bench_wrapper