class FIFOQueue:
    def __init__(self):
        # Initialize an empty list to represent the queue
        self.queue = []

    def enqueue(self, item):
        # Add an item to the end of the queue
        self.queue.append(item)
        print(f"Enqueued: {item}")

    def dequeue(self):
        # Remove and return the item at the front of the queue
        if not self.is_empty():
            item = self.queue.pop(0)
            print(f"Dequeued: {item}")
            return item
        else:
            print("Queue is empty. Cannot dequeue.")
            return None

    def is_empty(self):
        # Check if the queue is empty
        return len(self.queue) == 0

    def size(self):
        # Return the number of items in the queue
        return len(self.queue)

    def peek(self):
        # Return the item at the front of the queue without removing it
        if not self.is_empty():
            return self.queue[0]
        else:
            print("Queue is empty. Cannot peek.")
            return None

# Example usage:
if __name__ == "__main__":
    fifo_queue = FIFOQueue()

    # Enqueue some items
    fifo_queue.enqueue("Item 1")
    fifo_queue.enqueue("Item 2")
    fifo_queue.enqueue("Item 3")

    # Check the size of the queue
    print(f"Queue size: {fifo_queue.size()}")

    # Peek at the front item
    print(f"Front item: {fifo_queue.peek()}")

    # Dequeue items
    fifo_queue.dequeue()
    fifo_queue.dequeue()
    fifo_queue.dequeue()

    # Try to dequeue from an empty queue
    fifo_queue.dequeue()
