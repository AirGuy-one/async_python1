import random
import curses
import asyncio

from rocket_options import get_frame_size, display_rocket
from rocket_pictures import rocket_frame1
from stars_options import draw_one_star


async def blink(canvas):

    list_of_symbols = ["*", "+", "•"]

    # Here we get info about sizes of screen
    window_width, window_height = canvas.getmaxyx()

    canvas.border()
    curses.curs_set(False)

    # Here we get info about sizes of rocket
    rocket_frame_x, rocket_frame_y = get_frame_size(rocket_frame1)
    rocket_frame_x = int(rocket_frame_x / 2)

    # Here we specify that process still running
    # instead of we don't click any keyboard button
    canvas.nodelay(True)

    asyncio.create_task(
        display_rocket(canvas, rocket_frame_x, rocket_frame_y, window_width, window_height)
    )

    # Here we're drawing the stars
    for i in range(40):
        wait_time = random.uniform(0.05, 0.15)
        asyncio.create_task(
            draw_one_star(window_width, window_height, list_of_symbols, canvas)
        )
        await asyncio.sleep(wait_time)


def main():
    curses.update_lines_cols()

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(curses.wrapper(blink))
    main_loop.run_forever()


if __name__ == '__main__':
    main()
