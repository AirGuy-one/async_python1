import random
import curses
import asyncio
from addition_func import read_controls, draw_frame, get_frame_size, fire


rocket_frame1 = """
      .
     .'.
     |o|
    .'o'.
    |.-.|
    '   '
     ( )
      )
     ( )"""

rocket_frame2 = """
      .
     .'.
     |o|
    .'o'.
    |.-.|
    '   '
      )
     ( )
      ("""


async def blink(canvas):

    list_of_symbols = ["*", "+", "•"]

    window_tmp = curses.initscr()

    x_max, y_max = window_tmp.getmaxyx()

    canvas.border()
    curses.curs_set(False)

    async def tmp():
        row = random.randint(2, x_max - 2)
        column = random.randint(2, y_max - 2)
        symbol = random.choice(list_of_symbols)

        while True:
            canvas.addstr(row, column, symbol, curses.A_DIM)
            canvas.refresh()
            await asyncio.sleep(2)

            canvas.addstr(row, column, symbol)
            canvas.refresh()
            await asyncio.sleep(0.3)

            canvas.addstr(row, column, symbol, curses.A_BOLD)
            canvas.refresh()
            await asyncio.sleep(0.5)

            canvas.addstr(row, column, symbol)
            canvas.refresh()
            await asyncio.sleep(0.3)

    """ Here we get info about sizes of rocket """
    # rocket_frame_x, rocket_frame_y = get_frame_size(rocket_frame1)


    """ Here we specify that process still running instead of we dont click any keyboard button """
    canvas.nodelay(True)


    async def rocket():
        rows_direction, columns_direction, space_pressed = 0, 0, False
        rows, columns = 0, 0

        while True:
            read_var = read_controls(canvas)


            """ Here we indefinitely check that any button is pressed """
            if read_var[0] != -200:
                rows_direction, columns_direction, space_pressed = read_var
                rows += rows_direction
                columns += columns_direction
                await asyncio.sleep(0)

            draw_frame(canvas, 5 + rows, 30 + columns, rocket_frame1)
            canvas.refresh()
            await asyncio.sleep(0.08)

            draw_frame(canvas, 5 + rows, 30 + columns, rocket_frame1, negative=True)
            canvas.refresh()
            await asyncio.sleep(0)

            draw_frame(canvas, 5 + rows, 30 + columns, rocket_frame2)
            canvas.refresh()
            await asyncio.sleep(0.08)

            draw_frame(canvas, 5 + rows, 30 + columns, rocket_frame2, negative=True)
            canvas.refresh()
            await asyncio.sleep(0)

            some_text = " "
            canvas.addstr(9 + rows, 34 + columns, some_text)
            await asyncio.sleep(0)


            """ Here we check the status of the rows_direction and columns_direction variables in the code """
            # finish = str(rows_direction) + " and " + str(columns_direction)
            # canvas.addstr(10, 40, finish)
            # canvas.refresh()
            # await asyncio.sleep(0)


    asyncio.create_task(rocket())

    for i in range(40):
        wait_time = random.uniform(0.05, 0.15)
        asyncio.create_task(tmp())
        await asyncio.sleep(wait_time)


    ## "FIRE IS GOING" BUTTON ACTION
    # asyncio.create_task(fire(canvas, 5, 36))


if __name__ == '__main__':
    curses.update_lines_cols()

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(curses.wrapper(blink))
    main_loop.run_forever()
