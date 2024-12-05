class ObserverController:
    def __init__(self):
        super().__init__()
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)
        return observer

    async def notify_observers(self, state, source):
        for observer in self._observers:
            await observer.update(state, source)

