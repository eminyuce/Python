from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # Output: 55
print(fibonacci.cache_info())  # Output: CacheInfo(hits=18, misses=11, maxsize=None, currsize=11)

# lru_cache is a decorator that caches the results of a function so that when it is called with the same arguments, 
# the cached result is returned.
