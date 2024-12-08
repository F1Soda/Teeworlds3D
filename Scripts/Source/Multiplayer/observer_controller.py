class ObserverController:
    def __init__(self):
        super().__init__()
        self._observers = {}

    def add_observer(self, observer_id, observer):
        self._observers[observer_id] = observer
        return observer

    def remove_observer(self, observer_id):
        """Remove an observer from the list."""
        if observer_id in self._observers:
            del self._observers[observer_id]

    async def notify_observers(self, state, source):
        error_observers_id = []
        for observer in self._observers.values():
            try:
                await observer.update(state, source)
            except Exception as e:
                print(e)
                error_observers_id.append(observer.get_id())

        for error_observer_id in error_observers_id:
            print("ERROR: Remove error observer")
            del self._observers[error_observer_id]
