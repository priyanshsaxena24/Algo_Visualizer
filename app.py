from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import deque
import traceback

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Sorting Algorithms
def bubble_sort_with_steps(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append(arr[:])  # Capture current state
    return arr, steps

def merge_sort_with_steps(arr):
    steps = []

    def merge_sort(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]

            merge_sort(L)
            merge_sort(R)

            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                steps.append(arr[:])
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
                steps.append(arr[:])

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
                steps.append(arr[:])

    merge_sort(arr)
    return arr, steps

def quick_sort_with_steps(arr):
    steps = []

    def quick_sort(arr, start, end):
        if start < end:
            pivot_index = partition(arr, start, end)
            steps.append(arr[:])  # Capture current state
            quick_sort(arr, start, pivot_index - 1)
            quick_sort(arr, pivot_index + 1, end)

    def partition(arr, start, end):
        pivot = arr[end]
        i = start - 1
        for j in range(start, end):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[end] = arr[end], arr[i + 1]
        return i + 1

    quick_sort(arr, 0, len(arr) - 1)
    return arr, steps

def insertion_sort_with_steps(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        steps.append(arr[:])  # Capture current state
    return arr, steps

def selection_sort_with_steps(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr[:])  # Capture current state
    return arr, steps

def heap_sort_with_steps(arr):
    steps = []

    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    def heap_sort(arr):
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
            steps.append(arr[:])

        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            heapify(arr, i, 0)
            steps.append(arr[:])

    heap_sort(arr)
    return arr, steps

def counting_sort_with_steps(arr):
    if not arr:
        return arr, []
    steps = []
    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1
        steps.append(count[:])  # Capture the count array state

    sorted_arr = []
    for i, c in enumerate(count):
        sorted_arr.extend([i] * c)

    return sorted_arr, steps

def radix_sort_with_steps(arr):
    if not arr:
        return arr, []
    steps = []

    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]
        steps.append(arr[:])  # Capture the current state

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

    return arr, steps

# Graph Algorithms
def bfs_with_steps(graph, start):
    visited = set()
    queue = deque([start])
    order = []
    steps = []

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            steps.append({"current": vertex, "queue": list(queue)})

            for neighbor in graph.get(vertex, []):  # Use get() to avoid KeyError
                if neighbor not in visited:
                    queue.append(neighbor)

    return order, steps

def dfs_with_steps(graph, start):
    visited = set()
    stack = [start]
    order = []
    steps = []

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            steps.append({'current': vertex, 'stack': list(stack)})

            for neighbor in reversed(graph.get(vertex, [])):  # Use get() to avoid KeyError
                if neighbor not in visited:
                    stack.append(neighbor)

    return order, steps

# Algorithm Mapping
algorithm_mapping = {
    'bubble_sort': bubble_sort_with_steps,
    'merge_sort': merge_sort_with_steps,
    'quick_sort': quick_sort_with_steps,
    'insertion_sort': insertion_sort_with_steps,
    'selection_sort': selection_sort_with_steps,
    'heap_sort': heap_sort_with_steps,
    'counting_sort': counting_sort_with_steps,
    'radix_sort': radix_sort_with_steps,
    'bfs': bfs_with_steps,
    'dfs': dfs_with_steps,
}

# API Route
@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    try:
        data = request.json
        if not data or 'algorithm' not in data or 'input' not in data:
            return jsonify({'error': 'Invalid request. Missing required fields: algorithm, input.'}), 400

        algorithm = data['algorithm']
        input_data = data.get('input', [])
        graph = data.get('graph', None)

        if algorithm not in algorithm_mapping:
            return jsonify({'error': f'Algorithm "{algorithm}" is not supported.'}), 400

        if algorithm in ['bfs', 'dfs']:
            if not graph or not isinstance(graph, dict):
                return jsonify({'error': 'Graph data must be a valid dictionary.'}), 400
            start_node = input_data[0]
            if start_node not in graph:
                return jsonify({'error': f'Starting node "{start_node}" not found in the graph.'}), 400
            order, steps = algorithm_mapping[algorithm](graph, start_node)
            return jsonify({'order': order, 'steps': steps})

        # Sorting Algorithms
        result, steps = algorithm_mapping[algorithm](input_data)
        return jsonify({'result': result, 'steps': steps})

    except KeyError as e:
        return jsonify({'error': f'Missing key in input: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid value in input: {str(e)}'}), 400
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
