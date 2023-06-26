from MaxHeap import MaxHeap


def main():
    # Example usage
    heap = MaxHeap()
    heap.push(5)
    heap.push(10)
    heap.push(20)
    heap.push(2)
    print(heap.peek())
    print(heap.pop())
    print(heap.peek())


if __name__ == "__main__":
    main()
