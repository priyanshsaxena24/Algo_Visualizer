from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import deque
import traceback

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# BFS
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

            # Add unvisited neighbors to the queue
            for neighbor in graph.get(vertex, []):  # Use get() to avoid KeyError
                if neighbor not in visited:
                    queue.append(neighbor)

    return order, steps

# DFS
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

            # Add neighbors in reverse order to maintain DFS consistency
            for neighbor in reversed(graph.get(vertex, [])):  # Use get() to avoid KeyError
                if neighbor not in visited:
                    stack.append(neighbor)

    return order, steps

# Algorithm Mapping
algorithm_mapping = {
    'bfs': bfs_with_steps,
    'dfs': dfs_with_steps,
}

# API Route
@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    data = request.json
    if not data or 'algorithm' not in data or 'input' not in data:
        return jsonify({'error': 'Invalid request. Missing required fields: algorithm, input.'}), 400

    algorithm = data['algorithm']
    input_data = data.get('input', [])
    graph = data.get('graph')    # For BFS/DFS

    if algorithm not in algorithm_mapping:
        return jsonify({'error': f'Algorithm "{algorithm}" is not supported.'}), 400

    try:
        if algorithm in ['bfs', 'dfs']:
            if not graph or not isinstance(graph, dict):
                return jsonify({'error': 'Graph data must be a dictionary.'}), 400

            # Validate that all neighbors exist as keys in the graph
            for node, neighbors in graph.items():
                if not isinstance(neighbors, list):
                    return jsonify({'error': f'Neighbors of node "{node}" must be a list.'}), 400
                for neighbor in neighbors:
                    if neighbor not in graph:
                        return jsonify({'error': f'Graph is invalid. Node "{neighbor}" is referenced as a neighbor but does not exist as a key.'}), 400

            start_node = input_data[0]
            if start_node not in graph:
                return jsonify({'error': f'Starting node "{start_node}" not found in the graph.'}), 400

            order, steps = algorithm_mapping[algorithm](graph, start_node)
            return jsonify({'order': order, 'steps': steps})

    except KeyError as e:
        error_message = f"Graph is invalid. Missing key for node: {str(e)}"
        print("KeyError Traceback:", traceback.format_exc())
        return jsonify({'error': error_message}), 400
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print("Exception Traceback:", traceback.format_exc())
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
