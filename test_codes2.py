import threading
import time

# Function for the first thread
def thread1_function():
    for i in range(5):
        print("Thread 1: Iteration", i)
        time.sleep(1)

# Function for the second thread
def thread2_function():
    for i in range(5):
        print("Thread 2: Iteration", i)
        time.sleep(1)

# Main program
if __name__ == "__main__":
    # Create two threads
    thread1 = threading.Thread(target=thread1_function)
    thread2 = threading.Thread(target=thread2_function)

    # Start the threads
    thread1.start()
    thread2.start()

    # Main program loop
    for i in range(5):
        print("Main Program: Iteration", i)
        time.sleep(1)

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    print("Main Program: All threads have finished")

