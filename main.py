import random
import curses
import asyncio


async def blink(canvas):
    window_tmp = curses.initscr()

    x_max, y_max = window_tmp.getmaxyx()
    data_x, data_y = [], []
    for i in range(10):
        data_x.append(random.randint(1, x_max - 1))
        data_y.append(random.randint(1, y_max - 1))

    for i in range(10):
        canvas.border()
        curses.curs_set(False)
        row, column = data_x[i], data_y[i]
        symbol = "*"
        data_sec = [2, 0.3, 0.5, 0.3]

        for j in range(4):
            if j % 2 != 0:
                canvas.addstr(row, column, symbol)
                canvas.refresh()
                await asyncio.sleep(data_sec[j])
            elif j == 0:
                canvas.addstr(row, column, symbol, curses.A_DIM)
                canvas.refresh()
                await asyncio.sleep(data_sec[j])
            else:
                canvas.addstr(row, column, symbol, curses.A_BOLD)
                canvas.refresh()
                await asyncio.sleep(data_sec[j])


if __name__ == '__main__':
    curses.update_lines_cols()
    asyncio.run(curses.wrapper(blink))

# async def count_to_three():
#     print("Веду отсчёт. 1")
#     await asyncio.sleep(0)
#     print("Веду отсчёт. 2")
#     await asyncio.sleep(0)
#     print("Веду отсчёт. 3")
#     await asyncio.sleep(0)
#
# if __name__ == '__main__':
#     asyncio.run(count_to_three())

