import pyglet
from pyglet.shapes import Rectangle, Circle
from pyglet.gl import glClearColor
from datetime import datetime, timedelta
from globals import DEBUG_VISUALIZATION
def debug(str):
    if DEBUG_VISUALIZATION:
        print(str)

        
glClearColor(211 / 255.0, 211 / 255.0, 211 / 255.0, 1.0)

def visualize(visualization_data):
    static_data = visualization_data["static"]
    gas_station_order = visualization_data["gas_station_order"]
    dynamic_data = visualization_data["dynamic"]

    cell_size = 100  # Size of each grid cell in pixels
    window_width = len(static_data) * cell_size * 2
    window_height = len(static_data[0]) * cell_size
    window = pyglet.window.Window(window_width, window_height, "Gas Market Simulator Visualization")
    glClearColor(211 / 255.0, 211 / 255.0, 211 / 255.0, 1.0)
    batch = pyglet.graphics.Batch()

    static_elements = []

    # Static map elements
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





    gui_right_offset = 100

    def convert_seconds_to_timestamp(total_seconds):
        start_date = datetime(2023, 1, 1)
        new_date = start_date + timedelta(seconds=total_seconds)
        timestamp = new_date.strftime("%b %d, %Y - %H:%M:%S")
        return timestamp

    # Time display
    seconds = 0
    seconds_label = pyglet.text.Label(
        convert_seconds_to_timestamp(seconds),
        font_name='Arial',
        font_size=20,
        color=(0,0,0,255),
        x=window_width - 460,
        y=window_height - 40,
        anchor_x='left',
        anchor_y='center',
        batch=batch
    )

    # Button to increment by a second
    button0_width = 70
    button0_height = 30
    button0_x = window_width - 440 - gui_right_offset
    button0_y = window_height - 100
    # Button to increment by a minute
    button1_width = 70
    button1_height = 30
    button1_x = window_width - 345 - gui_right_offset
    button1_y = window_height - 100
    # Button to increment by an hour
    button2_width = 70
    button2_height = 30
    button2_x = window_width - 250 - gui_right_offset
    button2_y = window_height - 100
    # Button to increment by a day
    button3_width = 70
    button3_height = 30
    button3_x = window_width - 145 - gui_right_offset
    button3_y = window_height - 100
    # Button to increment by a month
    button4_width = 70
    button4_height = 30
    button4_x = window_width - 40 - gui_right_offset
    button4_y = window_height - 100
    # Reset seconds to 0
    reset_width = 100
    reset_height = 30
    reset_x = window_width - 265 - gui_right_offset
    reset_y = window_height - 140

    # Button 0
    button0 = Rectangle(
        button0_x, button0_y, button0_width, button0_height, color=(100, 200, 100), batch=batch
    )
    button0_label = pyglet.text.Label(
        "+sec",
        font_name='Arial',
        font_size=14,
        color=(0,0,0,255),
        x=button0_x + button0_width // 2,
        y=button0_y + button0_height // 2,
        anchor_x='center',
        anchor_y='center',
        batch=batch
    )
    # Button 1
    button1 = Rectangle(
        button1_x, button1_y, button1_width, button1_height, color=(100, 200, 100), batch=batch
    )
    button1_label = pyglet.text.Label(
        "+min",
        font_name='Arial',
        font_size=14,
        color=(0,0,0,255),
        x=button1_x + button1_width // 2,
        y=button1_y + button1_height // 2,
        anchor_x='center',
        anchor_y='center',
        batch=batch
    )
    # Button 2
    button2 = Rectangle(
        button2_x, button2_y, button2_width, button2_height, color=(100, 200, 100), batch=batch
    )
    button2_label = pyglet.text.Label(
        "+hour",
        font_name='Arial',
        font_size=14,
        color=(0,0,0,255),
        x=button2_x + button2_width // 2,
        y=button2_y + button2_height // 2,
        anchor_x='center',
        anchor_y='center',
        batch=batch
    )
    # Button 3
    button3 = Rectangle(
        button3_x, button3_y, button3_width, button3_height, color=(100, 200, 100), batch=batch
    )
    button3_label = pyglet.text.Label(
        "+day",
        font_name='Arial',
        font_size=14,
        color=(0,0,0,255),
        x=button3_x + button3_width // 2,
        y=button3_y + button3_height // 2,
        anchor_x='center',
        anchor_y='center',
        batch=batch
    )
    # Button 4
    button4 = Rectangle(
        button4_x, button4_y, button4_width, button4_height, color=(100, 200, 100), batch=batch
    )
    button4_label = pyglet.text.Label(
        "+month",
        font_name='Arial',
        font_size=14,
        color=(0,0,0,255),
        x=button4_x + button4_width // 2,
        y=button4_y + button4_height // 2,
        anchor_x='center',
        anchor_y='center',
        batch=batch
    )
    # Reset button
    reset = Rectangle(
        reset_x, reset_y, reset_width, reset_height, color=(66, 164, 245), batch=batch
    )
    reset_label = pyglet.text.Label(
        "reset time",
        font_name='Arial',
        font_size=14,
        color=(0,0,0,255),
        x=reset_x + reset_width // 2,
        y=reset_y + reset_height // 2,
        anchor_x='center',
        anchor_y='center',
        batch=batch
    )


    # Initializing car count labels
    car_count_labels = []

    def update_car_count_labels(car_counts):
        for label in car_count_labels:
            label.delete()
        car_count_labels.clear()

        for (coord_x, coord_y), num_cars in car_counts.items():
            label = pyglet.text.Label(
                str(num_cars),
                font_name="Arial",
                font_size=12,
                color=(0, 0, 0, 255),
                x=coord_x * cell_size + cell_size // 2,
                y=coord_y * cell_size + cell_size // 2,
                anchor_x="center",
                anchor_y="center",
                batch=batch,
            )
            car_count_labels.append(label)

    dqn_vars_label = pyglet.text.Label(
        "",
        font_name="Arial",
        font_size=16,
        color=(0, 0, 0, 255),
        x=window_width - 460,
        y=window_height - 300,
        anchor_x="left",
        anchor_y="center",
        multiline=True,  # Allow multiline text rendering
        width=400,
        batch=batch,
    )

    if seconds < len(dynamic_data):
        dqn_vars, car_counts = dynamic_data[seconds]
        formatted_text = "\n".join(f"{key}: {value}" for key, value in dqn_vars.items())
        dqn_vars_label.text = formatted_text
        update_car_count_labels(car_counts)
    else:
        dqn_vars_label.text = "No Data"
        update_car_count_labels({})

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        nonlocal seconds
        if button0_x <= x <= button0_x + button0_width and button0_y <= y <= button0_y + button0_height:
            seconds += 1
        elif button1_x <= x <= button1_x + button1_width and button1_y <= y <= button1_y + button1_height:
            seconds += 60
        elif button2_x <= x <= button2_x + button2_width and button2_y <= y <= button2_y + button2_height:
            seconds += 3600
        elif button3_x <= x <= button3_x + button3_width and button3_y <= y <= button3_y + button3_height:
            seconds += 86400
        elif button4_x <= x <= button4_x + button4_width and button4_y <= y <= button4_y + button4_height:
            seconds += 2592000
        elif reset_x <= x <= reset_x + reset_width and reset_y <= y <= reset_y + reset_height:
            seconds = 0
        else:
            return
        seconds_label.text = convert_seconds_to_timestamp(seconds)

        # Update dynamic data
        if seconds < len(dynamic_data):
            dqn_vars, car_counts = dynamic_data[seconds]
            formatted_text = "\n".join(f"{key}: {value}" for key, value in dqn_vars.items())
            dqn_vars_label.text = formatted_text
            update_car_count_labels(car_counts)
        else:
            dqn_vars_label.text = "No Data"
            update_car_count_labels({})


    @window.event
    def on_draw():
        window.clear()
        batch.draw()


    pyglet.app.run()