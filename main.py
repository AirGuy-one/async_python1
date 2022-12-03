import random
import curses
import asyncio


async def blink(canvas):
    window_tmp = curses.initscr()

    x_max, y_max = window_tmp.getmaxyx()

    canvas.border()
    curses.curs_set(False)
    symbol = "*"

    async def tmp():
        while True:
            row = random.randint(1, x_max - 1)
            column = random.randint(1, y_max - 1)

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

            

    asyncio.create_task(tmp())
    asyncio.create_task(tmp())
    asyncio.create_task(tmp())
    asyncio.create_task(tmp())
    asyncio.create_task(tmp())
    



if __name__ == '__main__':
    curses.update_lines_cols()

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(curses.wrapper(blink))
    main_loop.run_forever()
