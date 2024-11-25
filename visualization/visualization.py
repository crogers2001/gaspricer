import pyglet
from pyglet.shapes import Rectangle, Circle
from pyglet.gl import glClearColor

glClearColor(211 / 255.0, 211 / 255.0, 211 / 255.0, 1.0)

def visualize(visualization_data):
    # Extract static and dynamic data
    static_data = visualization_data["static"]
    dynamic_data = visualization_data["dynamic"]

    # Configuration for visualization
    cell_size = 100  # Size of each grid cell in pixels
    window_width = len(static_data) * cell_size
    window_height = len(static_data[0]) * cell_size
    window = pyglet.window.Window(window_width, window_height, "Gas Market Simulator Visualization")
    glClearColor(211 / 255.0, 211 / 255.0, 211 / 255.0, 1.0)
    batch = pyglet.graphics.Batch()

    # Drawing static map elements
    static_elements = []
    for x in range(len(static_data)):
        for y in range(len(static_data[0])):
            if "roadway" in static_data[x][y]:
                # class Rectangle(
                #     x: float,
                #     y: float,
                #     width: float,
                #     height: float,
                #     color: tuple[int, int, int, int] | tuple[int, int, int] = (255, 255, 255, 255),
                #     blend_src: int = GL_SRC_ALPHA,
                #     blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
                #     batch: Batch | None = None,
                #     group: Group | None = None,
                #     program: ShaderProgram | None = None
                # )
                size = cell_size * 0.4
                # height = cell_size if "vertical" in static_data[x][y]["roadway"].orientation else size
                # width = size if "vertical" in static_data[x][y]["roadway"].orientation else cell_size

                static_elements.append(Rectangle(
                    x * cell_size + ((cell_size - size) // 2),
                    y * cell_size + ((cell_size - size) // 2),
                    size,  # Width for horizontal, thin for vertical
                    size,
                    color=(230, 142, 0),  # Orange
                    batch=batch
                ))
            if "intersection" in static_data[x][y]:
                static_elements.append(Rectangle(
                    x * cell_size + cell_size // 4,
                    y * cell_size + cell_size // 4,
                    cell_size // 2,
                    cell_size // 2,
                    color=(198, 3, 252),  # Purple
                    batch=batch
                ))
            if "gas_station" in static_data[x][y]:
                color = (0, 195, 255) if "dqn" in static_data[x][y] else (255, 0, 0)  # Red or Bue
                center_x = x * cell_size + (cell_size // 4)
                center_y = y * cell_size + 3 * (cell_size // 4)
                radius = cell_size // 6

                static_elements.append(Circle( # Border
                    center_x,
                    center_y,
                    radius + 4,
                    color=(0, 0, 0),
                    batch=batch
                ))

                static_elements.append(Circle(
                    center_x,
                    center_y,
                    radius,
                    color=color,
                    batch=batch
                ))

    # Drawing dynamic elements (e.g., cars)
    dynamic_elements = []

    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        for car in dynamic_elements:
            car.delete()  # Clear previous dynamic elements

        # Redraw cars and other dynamic items
        for item in dynamic_data:
            for car_position in item.get("cars", []):  # Assuming car positions are tuples (x, y)
                car_x, car_y = car_position
                dynamic_elements.append(Circle(
                    car_x * cell_size + cell_size // 2,
                    car_y * cell_size + cell_size // 2,
                    cell_size // 6,
                    color=(0, 0, 255),  # Blue for cars
                    batch=batch
                ))
    
    def update(dt):
        # Update dynamic data each frame
        if visualization_data["dynamic"]:
            visualization_data["dynamic"] = visualization_data["dynamic"][1:]  # Advance in time
    
    # Schedule updates
    pyglet.clock.schedule_interval(update, 1 / 60.0)  # 60 FPS

    # Run the Pyglet application
    pyglet.app.run()
