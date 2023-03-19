import curses
import asyncio

from rocket_pictures import rocket_frame1, rocket_frame2


SPACE_KEY_CODE = 32
# Here we're init wasd buttons
LEFT_KEY_CODE = 97
RIGHT_KEY_CODE = 100
UP_KEY_CODE = 119
DOWN_KEY_CODE = 115


def read_controls(canvas):
    """Read keys pressed and returns tuple with controls state."""
    rows_direction = columns_direction = 0
    space_pressed = False

    pressed_key_code = canvas.getch()

    if pressed_key_code == UP_KEY_CODE:
        rows_direction = -1
    elif pressed_key_code == DOWN_KEY_CODE:
        rows_direction = 1
    elif pressed_key_code == RIGHT_KEY_CODE:
        columns_direction = 1
    elif pressed_key_code == LEFT_KEY_CODE:
        columns_direction = -1
    elif pressed_key_code == SPACE_KEY_CODE:
        space_pressed = True
    else:
        return -200, 0, False

    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas, start_row, start_column, text, negative=False):
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not
            # in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


async def fire(
        canvas, start_row,
        start_column, rows_speed=-1,
        columns_speed=0):
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(1)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(1)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def display_rocket(canvas, rocket_frame_x, rocket_frame_y, window_width, window_height):
    rows_direction, columns_direction, space_pressed = 0, 0, False
    # We're init vars that denote the position of the rocket at a certain time
    rows, columns = 0, 0

    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        # Here we indefinitely check that any button is pressed
        if rows_direction != -200:
            rows += rows_direction
            columns += columns_direction
            await asyncio.sleep(0)

        # Here we need to check that rocket is in play field and
        # if it is not in field we return it back
        # To do it we determine the coordinates of corners of rocket
        # To determine the coordinates we
        y_edge_indent = 5
        x_edge_indent = 10
        line_should_be_considered = 1
        top = y_edge_indent + rows + line_should_be_considered
        bottom = y_edge_indent + rows + rocket_frame_y + line_should_be_considered
        indent_in_the_picture_of_rocket = 4
        left = x_edge_indent + columns + indent_in_the_picture_of_rocket
        right = x_edge_indent + columns + rocket_frame_x + indent_in_the_picture_of_rocket
        if top <= 0:
            rows += 1
        elif bottom >= window_width:
            rows -= 1
        elif left <= 0:
            columns += 1
        elif right >= window_height:
            columns -= 1

        draw_frame(canvas, y_edge_indent + rows, x_edge_indent + columns, rocket_frame1)
        canvas.refresh()
        await asyncio.sleep(0.08)

        draw_frame(canvas, y_edge_indent + rows, x_edge_indent + columns,
                   rocket_frame1, negative=True)
        canvas.refresh()
        await asyncio.sleep(0)

        draw_frame(canvas, y_edge_indent + rows, x_edge_indent + columns, rocket_frame2)
        canvas.refresh()
        await asyncio.sleep(0.08)

        draw_frame(canvas, y_edge_indent + rows, x_edge_indent + columns,
                   rocket_frame2, negative=True)
        canvas.refresh()
        await asyncio.sleep(0)

        some_text = " "
        canvas.addstr(9 + rows, 34 + columns, some_text)
        await asyncio.sleep(0)
