import random
import curses
import asyncio


async def blink(canvas):

    list_of_symbols = ["*", "+", "•"]

    window_tmp = curses.initscr()

    x_max, y_max = window_tmp.getmaxyx()

    canvas.border()
    curses.curs_set(False)

    async def tmp():
        row = random.randint(1, x_max - 1)
        column = random.randint(1, y_max - 1)
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

    for i in range(50):
        wait_time = random.uniform(0.2, 0.5)
        asyncio.create_task(tmp())
        await asyncio.sleep(wait_time)
    

if __name__ == '__main__':
    curses.update_lines_cols()

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(curses.wrapper(blink))
    main_loop.run_forever()
