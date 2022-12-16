import random
import curses
import asyncio
from rocket_options import read_controls, draw_frame, get_frame_size
from rocket_pictures import rocket_frame1, rocket_frame2


async def blink(canvas):

    list_of_symbols = ["*", "+", "•"]

    window_tmp = curses.initscr()

    # Here we get info about sizes of screen
    window_width, window_height = window_tmp.getmaxyx()

    canvas.border()
    curses.curs_set(False)

    async def draw_one_star():
        # Here we determine which coordinates inside border the star has
        row_inside_border = random.randint(2, window_width - 2)
        column_inside_border = random.randint(2, window_height - 2)
        star_symbol = random.choice(list_of_symbols)

        while True:
            canvas.addstr(
                row_inside_border, column_inside_border,
                star_symbol, curses.A_DIM)
            await asyncio.sleep(2)

            canvas.addstr(row_inside_border, column_inside_border, star_symbol)
            await asyncio.sleep(0.3)

            canvas.addstr(
                row_inside_border, column_inside_border,
                star_symbol, curses.A_BOLD)
            await asyncio.sleep(0.5)

            canvas.addstr(row_inside_border, column_inside_border, star_symbol)
            await asyncio.sleep(0.3)

    # Here we get info about sizes of rocket
    rocket_frame_x, rocket_frame_y = get_frame_size(rocket_frame1)
    rocket_frame_x = int(rocket_frame_x / 2)

    # Here we specify that process still running
    # instead of we don't click any keyboard button
    canvas.nodelay(True)

    async def display_rocket():
        rows_direction, columns_direction, space_pressed = 0, 0, False
        # We're init vars that denote the position of the rocket at a certain time
        rows, columns = 0, 0

        while True:
            read_var = read_controls(canvas)

            # Here we indefinitely check that any button is pressed
            if read_var[0] != -200:
                rows_direction, columns_direction, space_pressed = read_var
                rows += rows_direction
                columns += columns_direction
                await asyncio.sleep(0)

            # Here we need to check that rocket is in play field and
            # if it is not in field we return it back
            # To do it we determine the coordinates of corners of rocket
            # To determine the coordinates we
            rocket_corner_x_right = 5 + 1 + rows + rocket_frame_x - 1
            rocket_corner_x_left = 5 + 1 + rows
            rocket_corner_y_right = 30 + 4 + columns + rocket_frame_y - 1
            rocket_corner_y_left = 30 + 4 + columns
            if rocket_corner_x_left <= 0:
                rows += 1
            elif rocket_corner_x_right >= window_width:
                rows -= 1
            elif rocket_corner_y_left <= 0:
                columns += 1
            elif rocket_corner_y_right >= window_height:
                columns -= 1

            draw_frame(canvas, 5 + rows, 30 + columns, rocket_frame1)
            canvas.refresh()
            await asyncio.sleep(0.08)

            draw_frame(canvas, 5 + rows, 30 + columns,
                       rocket_frame1, negative=True)
            canvas.refresh()
            await asyncio.sleep(0)

            draw_frame(canvas, 5 + rows, 30 + columns, rocket_frame2)
            canvas.refresh()
            await asyncio.sleep(0.08)

            draw_frame(canvas, 5 + rows, 30 + columns,
                       rocket_frame2, negative=True)
            canvas.refresh()
            await asyncio.sleep(0)

            some_text = " "
            canvas.addstr(9 + rows, 34 + columns, some_text)
            await asyncio.sleep(0)

    asyncio.create_task(display_rocket())

    # Here we're drawing the stars
    for i in range(40):
        wait_time = random.uniform(0.05, 0.15)
        asyncio.create_task(draw_one_star())
        await asyncio.sleep(wait_time)


def main():
    curses.update_lines_cols()

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(curses.wrapper(blink))
    main_loop.run_forever()


if __name__ == '__main__':
    main()
