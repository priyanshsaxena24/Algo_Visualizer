import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Tree from 'react-d3-tree';

const App = () => {
    const [selectedCategory, setSelectedCategory] = useState('');
    const [algorithm, setAlgorithm] = useState('');
    const [inputData, setInputData] = useState('');
    const [graph, setGraph] = useState('');
    const [steps, setSteps] = useState([]);
    const [currentStepIndex, setCurrentStepIndex] = useState(0);
    const [isAnimating, setIsAnimating] = useState(false);

    const sortingAlgorithms = [
        'bubble_sort',
        'merge_sort',
        'quick_sort',
        'insertion_sort',
        'selection_sort',
        'heap_sort',
        'counting_sort',
        'radix_sort',
    ];

    const graphAlgorithms = ['bfs', 'dfs'];

    const handleSubmit = async () => {
        const payload = { algorithm };

        if (selectedCategory === 'sorting') {
            if (!inputData) {
                alert('Please enter input data.');
                return;
            }
            payload.input = inputData.split(',').map(Number); // Convert input to array
        } else if (selectedCategory === 'graphs') {
            if (!graph) {
                alert('Please enter a valid graph in JSON format.');
                return;
            }
            try {
                payload.graph = JSON.parse(graph);
                payload.input = [inputData]; // Starting node
            } catch (error) {
                alert('Invalid graph format. Please enter valid JSON.');
                return;
            }
        }

        try {
            console.log('Payload:', payload); // Debugging
            const response = await axios.post('http://localhost:5000/run-algorithm', payload);
            setSteps(response.data.steps || []);
            setCurrentStepIndex(0);
            setIsAnimating(false);
        } catch (error) {
            console.error('Error:', error.response?.data || error.message);
            alert(error.response?.data?.error || 'Something went wrong! Please check your input.');
        }
    };

    useEffect(() => {
        let interval;
        if (isAnimating && steps.length > 0) {
            interval = setInterval(() => {
                setCurrentStepIndex((prevIndex) => {
                    if (prevIndex < steps.length - 1) {
                        return prevIndex + 1;
                    } else {
                        clearInterval(interval);
                        setIsAnimating(false);
                        return prevIndex;
                    }
                });
            }, 1000); // Adjust delay for animation speed
        }
        return () => clearInterval(interval);
    }, [isAnimating, steps]);

    const startAnimation = () => {
        if (steps.length === 0) {
            alert('No steps to animate. Please run an algorithm first.');
            return;
        }
        setIsAnimating(true);
    };

    // Transform graph into Tree format
    const transformGraphToTree = (graph, currentNode = null, visited = new Set()) => {
        if (!currentNode || visited.has(currentNode)) return null;

        visited.add(currentNode);

        return {
            name: currentNode,
            children: (graph[currentNode] || [])
                .filter((child) => !visited.has(child)) // Avoid cycles
                .map((child) => transformGraphToTree(graph, child, visited)),
        };
    };

    const renderTree = () => {
        if (!graph) return null;

        const parsedGraph = JSON.parse(graph);
        const treeData = transformGraphToTree(parsedGraph, inputData); // Start from the inputData node

        if (!treeData) {
            return <div>No valid tree structure found. Check the input graph.</div>;
        }

        return (
            <div id="treeWrapper" style={{ width: '100%', height: '400px' }}>
                <Tree
                    data={treeData}
                    orientation="vertical"
                    nodeSize={{ x: 200, y: 100 }}
                    translate={{ x: 300, y: 50 }}
                    renderCustomNodeElement={(rd3tProps) => {
                        const { nodeDatum } = rd3tProps;
                        return (
                            <g>
                                <circle
                                    r={15}
                                    fill={
                                        steps[currentStepIndex]?.current === nodeDatum.name
                                            ? 'red'
                                            : 'blue'
                                    }
                                    stroke="black"
                                    strokeWidth="2"
                                />
                                <text
                                    x={20}
                                    fill="black"
                                    fontSize="12"
                                    dominantBaseline="middle"
                                >
                                    {nodeDatum.name}
                                </text>
                            </g>
                        );
                    }}
                />
            </div>
        );
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial', maxWidth: '800px', margin: 'auto' }}>
            <h1>Algorithm Visualizer</h1>

            {/* Navbar */}
            <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'center' }}>
                <button
                    onClick={() => {
                        setSelectedCategory('sorting');
                        setAlgorithm('');
                        setSteps([]);
                    }}
                    style={{
                        padding: '10px 20px',
                        marginRight: '10px',
                        backgroundColor: selectedCategory === 'sorting' ? 'blue' : 'gray',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer',
                    }}
                >
                    Sorting Algorithms
                </button>
                <button
                    onClick={() => {
                        setSelectedCategory('graphs');
                        setAlgorithm('');
                        setSteps([]);
                    }}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: selectedCategory === 'graphs' ? 'blue' : 'gray',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer',
                    }}
                >
                    Graph Algorithms
                </button>
            </div>

            {/* Dropdown for Algorithm Selection */}
            {selectedCategory && (
                <div>
                    <label>
                        <strong>Select Algorithm:</strong>
                        <select
                            value={algorithm}
                            onChange={(e) => setAlgorithm(e.target.value)}
                            style={{ marginLeft: '10px' }}
                        >
                            <option value="">-- Select --</option>
                            {selectedCategory === 'sorting' &&
                                sortingAlgorithms.map((algo) => (
                                    <option key={algo} value={algo}>
                                        {algo.replace('_', ' ').toUpperCase()}
                                    </option>
                                ))}
                            {selectedCategory === 'graphs' &&
                                graphAlgorithms.map((algo) => (
                                    <option key={algo} value={algo}>
                                        {algo.toUpperCase()}
                                    </option>
                                ))}
                        </select>
                    </label>
                </div>
            )}
            <br />

            {/* Inputs for Sorting Algorithms */}
            {selectedCategory === 'sorting' && algorithm && (
                <div>
                    <label>
                        <strong>Input Array:</strong>
                        <input
                            type="text"
                            placeholder="e.g., 5, 3, 8, 4"
                            value={inputData}
                            onChange={(e) => setInputData(e.target.value)}
                            style={{ marginLeft: '10px', width: '300px' }}
                        />
                    </label>
                </div>
            )}

            {/* Inputs for Graph Algorithms */}
            {selectedCategory === 'graphs' && algorithm && (
                <div>
                    <label>
                        <strong>Graph (JSON):</strong>
                        <textarea
                            placeholder='e.g., {"A": ["B", "C"], "B": ["D"], "C": []}'
                            value={graph}
                            onChange={(e) => setGraph(e.target.value)}
                            style={{ marginLeft: '10px', width: '300px', height: '100px' }}
                        />
                    </label>
                    <br />
                    <label>
                        <strong>Starting Node:</strong>
                        <input
                            type="text"
                            placeholder="e.g., A"
                            value={inputData}
                            onChange={(e) => setInputData(e.target.value)}
                            style={{ marginLeft: '10px', width: '300px' }}
                        />
                    </label>
                </div>
            )}
            <br />

            {/* Run and Animate Buttons */}
            <button onClick={handleSubmit} style={{ padding: '10px 20px', fontSize: '16px' }}>
                Run Algorithm
            </button>
            <button
                onClick={startAnimation}
                style={{
                    padding: '10px 20px',
                    fontSize: '16px',
                    marginLeft: '10px',
                    backgroundColor: isAnimating ? 'gray' : 'green',
                    color: 'white',
                    cursor: isAnimating ? 'not-allowed' : 'pointer',
                }}
                disabled={isAnimating}
            >
                Start Animation
            </button>

            {/* Visualization */}
            <div style={{ marginTop: '30px' }}>
                {selectedCategory === 'sorting' && steps.length > 0 && (
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-end' }}>
                        {steps[currentStepIndex]?.map((value, idx) => (
                            <div
                                key={idx}
                                style={{
                                    width: '20px',
                                    height: `${value * 10}px`,
                                    margin: '0 5px',
                                    backgroundColor: 'blue',
                                }}
                            ></div>
                        ))}
                    </div>
                )}

                {selectedCategory === 'graphs' && renderTree()}
            </div>
        </div>
    );
};

export default App;
