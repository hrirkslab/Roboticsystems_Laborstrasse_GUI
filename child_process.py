import sys
import time

if __name__ == "__main__":
    # Simulate some work
    time.sleep(2)
    # Send a message to the parent process
    sys.stdout.write("Hello from child process!\n")
    sys.stdout.flush()
