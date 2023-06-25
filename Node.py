import threading


class Node:
    def __init__(self, elem):
        self.left = None
        self.right = None
        self.elem = elem
        self.lock = threading.Lock()

    def lock(self):
        self.lock.acquire()

    def unlock(self):
        self.lock.release()
