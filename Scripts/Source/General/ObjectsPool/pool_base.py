class PoolBase:
    def __init__(self, preload_count: int, preload_func, get_func, before_return_func):
        self._pool = []
        self._active = []

        self._preload_func = preload_func
        self._get_func = get_func
        self._before_return_func = before_return_func

        if preload_func is None:
            raise Exception("Preload function can't be None!")

        for i in range(preload_count):
            self.back_to_pool(preload_func())

    def get(self):
        if len(self._pool) > 0:
            item = self._pool.pop(0)
            print("GET")
        else:
            item = self._preload_func()
            print("CREATE")
        self._get_func(item)
        self._active.append(item)
        return item

    def back_to_pool(self, item):
        self._before_return_func(item)
        self._pool.append(item)
        self._active.remove(item)

    def back_to_pool_all(self):
        for active_item in self._active:
            self.back_to_pool(active_item)
