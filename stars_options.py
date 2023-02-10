import random
import curses
import asyncio


async def draw_one_star(window_width, window_height, list_of_symbols, canvas, wait_time):
    # Here we determine which coordinates inside border the star has
    row_inside_border = random.randint(2, window_width - 2)
    column_inside_border = random.randint(2, window_height - 2)
    star_symbol = random.choice(list_of_symbols)

    while True:
        await asyncio.sleep(wait_time)

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


