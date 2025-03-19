
from functools import lru_cache
from splay_tree import SplayTree
import timeit
import matplotlib.pyplot as plt

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1: return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)


class SplayTreeCache:
    class SplayTreeElement:
        def __init__(self, key, value):
            self.key = key
            self.value = value
        
        def __lt__(self, other):
            return self.key < other.key
        
        def __gt__(self, other):
            return self.key > other.key
        
        def __eq__(self, other):
            return self.key == other.key

    def __init__(self):
        self.tree = SplayTree()

    def __call__(self, func):
        def wrapper(n):
            if n <= 1: return n
            element = self.SplayTreeElement(n, None)
            element = self.tree.find(element)
            if element is None:
                element = self.SplayTreeElement(n, func(n))
                self.tree.insert(element)
            return element.value
        wrapper.clear_cache = self.clear_cache
        return wrapper
    
    def clear_cache(self):
        self.tree.clear()


@SplayTreeCache()
def fibonacci_splay(n):
    if n <= 1: return n
    return fibonacci_splay(n-1) + fibonacci_splay(n-2)

if __name__ == "__main__":
    # Test with LRU cache
    tests = [i for i in range(0, 1000, 50)]
    lru_cache_results = []
    splay_tree_results = []

    # Setup timeit for both functions
    for i in tests:
        # Measure LRU cache implementation
        lru_time = timeit.Timer(
            lambda: fibonacci_lru(i),
            # setup='from __main__ import fibonacci_lru; fibonacci_lru.cache_clear()'
        ).timeit(number=100) / 100
        lru_cache_results.append(lru_time)
        
        # Measure Splay tree implementation
        splay_time = timeit.Timer(
            lambda: fibonacci_splay(i),
            # setup='from __main__ import fibonacci_splay; fibonacci_splay.clear_cache()'
        ).timeit(number=100) / 100
        # splay_time = 0
        splay_tree_results.append(splay_time)
    
    # Print results in fixed-width format
    print("n         LRU Cache Time (s)  Splay Tree Time (s) ")
    print("-" * 50)
    for n, (lru_time, splay_time) in zip(tests, zip(lru_cache_results, splay_tree_results)):
        print(f"{n:<9} {lru_time:>16.8f}  {splay_time:>16.8f}")

    # Create the comparison graph
    plt.figure(figsize=(10, 6))
    plt.plot(tests, lru_cache_results, 'o-', label='LRU Cache')
    plt.plot(tests, splay_tree_results, 'x-', label='Splay Tree')
    
    plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
    plt.xlabel('Число Фібоначчі (n)')
    plt.ylabel('Середній час виконання (секунди)')
    plt.grid(True)
    plt.legend()
    
    # Scientific notation for y-axis
    plt.ticklabel_format(axis='y', style='scientific', scilimits=(0,0))
    
    # Save the plot
    plt.savefig('fibonacci_comparison.png')
    plt.close()



