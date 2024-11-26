class Roadway:

    def __init__(self, coordinate, v_orientation, speed_limit):
        self.coordinate = coordinate # acts as ID 
        self.speed_limit = speed_limit
        self.orientation = v_orientation # used for rendering. Currently doesn't work well since there can be horizontal and vertical roadways entering an intersection.
        self.distance = 300 # meters

