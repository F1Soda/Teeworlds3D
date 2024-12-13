class PoolBase:
    def __init__(self, preload_count: int, preload_func, get_func, before_return_func):
        self.pool = []
        self._active = []

        self._preload_func = preload_func
        self._get_func = get_func
        self._before_return_func = before_return_func
        # self._contains_func = contains_func

        if preload_func is None:
            raise Exception("Preload function can't be None!")

        for i in range(preload_count):
            self.back_to_pool(preload_func())

    def get(self):
        if len(self.pool) > 0:
            item = self.pool.pop(0)
        else:
            item = self._preload_func()
        self._get_func(item)
        self._active.append(item)
        return item

    def back_to_pool(self, item):
        self._before_return_func(item)
        self.pool.append(item)
        try:
            self._active.remove(item)
            # print("removed from active: ", item)
        except:
            print(f"Atempt to delete {item}\n in follow list:")
            for item in self._active:
                print(item)
            # raise
            pass

    def back_to_pool_all(self):
        for active_item in self._active:
            self.back_to_pool(active_item)
