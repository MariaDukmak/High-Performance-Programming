import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2) # wait for 2 seconds
    logging.info("Thread %s: finishing", name)

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     threads = list()
#     for index in range(3):
#         logging.info("Main    : create and start thread %d.", index)
#         x = threading.Thread(target=thread_function, args=(index,))
#         threads.append(x)
#         x.start()
#
#     for index, thread in enumerate(threads):
#         logging.info("Main    : before joining thread %d.", index)
#         thread.join()
#         logging.info("Main    : thread %d done", index)


#Draai de code een aantal maal, en observeer wat er gebeurt. Zie je opvallende dingen?
# De threads worden soms eerst geexecuted voor dat de main eindigt en soms anderom en ook door elkaar heen.



import concurrent.futures

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))

# Draai het programma een aantal malen en observeer het gedrag.
# op dit mainer worden the threads eerst afgesloten voordat er verder gagaan met de main