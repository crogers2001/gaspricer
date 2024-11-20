class GlobalClock:
    _instance = None # Class variable that stores the single instance of the global clock

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.current_time = 0

    def get_time(self):
        return self.current_time
    
    def tick(self):
        self.current_time += 1