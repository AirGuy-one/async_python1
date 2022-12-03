import random
import curses
import asyncio


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

    asyncio.create_task(fire(canvas, 7, 20))


    for i in range(50):
        wait_time = random.uniform(0.2, 0.5)
        asyncio.create_task(tmp())
        await asyncio.sleep(wait_time)
    

if __name__ == '__main__':
    curses.update_lines_cols()

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(curses.wrapper(blink))
    main_loop.run_forever()
