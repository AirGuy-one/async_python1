import random
import curses
import asyncio


SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 97
RIGHT_KEY_CODE = 100
UP_KEY_CODE = 119 #w
DOWN_KEY_CODE = 115 #s


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""
    
    rows_direction = columns_direction = 0
    space_pressed = False

    pressed_key_code = canvas.getch()

    # if pressed_key_code == 81:
    #     # https://docs.python.org/3/library/curses.html#curses.window.getch
    #     return -200, 0, False

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
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""

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

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)

def get_frame_size(text):
    """ Calculate size of multiline text fragment, return pair — number of rows and columns. """

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns

async def fire(canvas, start_row, start_column, rows_speed=-1, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

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
