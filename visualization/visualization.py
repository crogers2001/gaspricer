import pyglet
from pyglet.shapes import Rectangle, Circle
from pyglet.gl import glClearColor

glClearColor(211 / 255.0, 211 / 255.0, 211 / 255.0, 1.0)

def visualize(visualization_data):
    static_data = visualization_data["static"]
    gas_station_order = visualization_data["gas_station_order"]
    dynamic_data = visualization_data["dynamic"]

    cell_size = 100  # Size of each grid cell in pixels
    window_width = len(static_data) * cell_size
    window_height = len(static_data[0]) * cell_size
    window = pyglet.window.Window(window_width, window_height, "Gas Market Simulator Visualization")
    glClearColor(211 / 255.0, 211 / 255.0, 211 / 255.0, 1.0)
    batch = pyglet.graphics.Batch()

    static_elements = []

    for x in range(len(static_data)):
        for y in range(len(static_data[0])):
            if "roadway" in static_data[x][y]:
                size = cell_size * 0.4
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
                color = (0, 195, 255) if "dqn" in static_data[x][y] else (255, 0, 0)  # Red or Blue
                center_x = x * cell_size + (cell_size // 4)
                center_y = y * cell_size + 3 * (cell_size // 4)
                radius = cell_size // 6

                static_elements.append(Circle(  # Border
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

# Gas Station numbering
    gas_station_ct = 0
    for item in gas_station_order:
        (x,y), _ = item
        center_x = x * cell_size + (cell_size // 4)
        center_y = y * cell_size + 3 * (cell_size // 4)
        radius = cell_size // 6
        if gas_station_ct > 0:
            static_elements.append(pyglet.text.Label(
                str(gas_station_ct),
                font_name='Arial',
                font_size=radius,
                color=(0,0,0,255),
                x=center_x,
                y=center_y,
                anchor_x='center',
                anchor_y='center',
                batch=batch
            ))
        gas_station_ct += 1


    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    pyglet.app.run()