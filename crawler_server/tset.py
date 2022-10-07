import asyncio
import time


async def main():
    print('hello 任務開始')
    await asyncio.sleep(2)
    print('hello 任務結束')


print('hello 開始')
asyncio.create_task(main())
asyncio.run_coroutine_threadsafe()
print('hello 結束')
input('a')
