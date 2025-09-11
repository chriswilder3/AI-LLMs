import asyncio
import time

async def task_function(task_msg, delay):
    print("task displays : ", task_msg)

    await asyncio.sleep(delay)

    return {"completed": task_msg}

async def main():
    start = time.time()

    task1 = asyncio.create_task(task_function("t1",2))
    task2 = asyncio.create_task(task_function("t2",1))
    task3 = asyncio.create_task(task_function("t3",3))

    results = await asyncio.gather(task1, task2, task3)

    end = time.time()
    print(" results : ",results, ", The time consumed : ", end-start)

if __name__ == "__main__":
    asyncio.run(main())