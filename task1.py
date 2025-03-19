import random
import time
from collections import OrderedDict


MAGIC_NUM = 100_000
OPERATIONS = ['Range', 'Update']


array = [random.randint(0, MAGIC_NUM) for _ in range(MAGIC_NUM)]
test_tasks = [(random.choice(OPERATIONS), random.randint(0, MAGIC_NUM-1), random.randint(0, MAGIC_NUM-1)) for _ in range(MAGIC_NUM // 2)]


class LRUCache:
    """
    LRU Cache implementation using OrderedDict.
    Implements the decorator pattern for caching function results.
    """
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Extract L and R from either positional or keyword arguments
            # Assuming L and R are the second and third arguments after 'array'
            if len(args) >= 3:
                L, R = args[1], args[2]
            else:
                L = kwargs.get('L')
                R = kwargs.get('R')
                if L is None or R is None:
                    raise ValueError("L and R must be provided either as positional or keyword arguments")

            # Create cache key using only L and R
            key = (L, R)
            
            # If key exists in cache, move it to the end (most recently used)
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            
            # Calculate result with all original arguments
            result = func(*args, **kwargs)
            
            # Add to cache
            self.cache[key] = result
            
            # If cache is full, remove least recently used item
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
            
            return result
        
        # Add cache_clear method to the wrapper
        def cache_clear():
            self.cache.clear()
        
        def cache_partial_clear(index):
            for key in list(self.cache.keys()):
                if key[0] <= index <= key[1]:
                    self.cache.pop(key)
        
        wrapper.cache_clear = cache_clear
        wrapper.cache_partial_clear = cache_partial_clear
        return wrapper


def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])  # Fixed to include R


def update_no_cache(array, index, value):
    array[index] = value
    return index

@LRUCache(capacity=1000)
def range_sum_with_cache(array, L, R):
    return sum(array[L:R+1])  # Fixed to include R

def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache.cache_partial_clear(index)  # Clear some cached results when array is modified
    return index


if __name__ == "__main__":
    # print("Testing without cache...")
    # measure time
    start_time = time.time()
    for task in test_tasks:
        if task[0] == 'Range':
            range_sum_no_cache(array, task[1], task[2])
        else:
            update_no_cache(array, task[1], task[2])
    end_time = time.time()
    print(f"Execution time without caching: {end_time - start_time:.2f} seconds")

    # print("\nTesting with LRU cache...")
    # Test with cache
    start_time = time.time()
    for task in test_tasks:
        if task[0] == 'Range':
            range_sum_with_cache(array, task[1], task[2])
        else:
            update_with_cache(array, task[1], task[2])
    end_time = time.time()
    print(f"Execution time with LRU cache: {end_time - start_time:.2f} seconds")
