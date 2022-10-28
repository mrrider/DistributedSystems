import random
import multiprocessing

NUM_PROC = 2

def append_to_list(lst, num_items, taskId):
    for n in random.sample(range(200000), num_items):
        lst.append(n)
    print(taskId)
    
if __name__ == "__main__":
    jobs = []

    for i in range(NUM_PROC):
        process = multiprocessing.Process(
            target=append_to_list, 
            args=([], 100, i)
        )
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()