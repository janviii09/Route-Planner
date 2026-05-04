# 🗺️ AI Route Planner & City Infrastructure Engine

> An advanced, interactive Graph Theory and Routing simulation system. Built with Python (FastAPI) and Vanilla JS + HTML5 Canvas.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern_API-009688.svg)
![Algorithms](https://img.shields.io/badge/Algorithms-Graph_Theory-ff69b4.svg)

## 📖 Overview
The **AI Route Planner** is a dynamic, multi-modal routing engine designed to solve complex spatial problems in a simulated city environment. Instead of relying on a single static algorithm, the system implements an intelligent **Algorithm Decision Logic** that dynamically selects the optimal algorithm based on user constraints (e.g., emergencies, negative weights, traffic patterns). 

Additionally, the system features a **City Planner Mode** that utilizes Kruskal's Algorithm and Disjoint Set Union (DSU) to visually animate the construction of a Minimum Spanning Tree (MST).

---

## ✨ Key Features

### 1. Intelligent Routing Mode
Dynamically switches between algorithms based on real-time constraints:
- **Dijkstra's Algorithm (Min-Heap):** The robust default for finding the shortest weighted path.
- **A* Search (Euclidean Heuristic):** Highly optimized spatial pathfinding for coordinate-based grids.
- **Breadth-First Search (BFS):** Used in "Emergency Mode" to find the path with the absolute fewest intersections, ignoring traffic weights entirely.
- **Bellman-Ford Algorithm:** Triggered when negative weights (e.g., toll rebates, carbon credits) are introduced into the network, safely preventing negative cycle traps.

### 2. Dynamic Traffic Heatmap & Segment Trees
- Time-series traffic data is modeled across the day (6 AM to Midnight).
- Arterial roads experience massive congestion spikes during rush hours.
- A **Segment Tree ($O(\log n)$)** is implemented to instantly query peak traffic congestion over specific time windows without linear scanning.

### 3. City Infrastructure Planner (MST Animation)
- Computes the minimum-cost network to connect all city zones.
- Visually **animates Kruskal's Greedy MST**.
- Highlights accepted edges in green and momentarily flashes rejected cycle-forming edges in red to demonstrate **Disjoint Set Union (DSU)** cycle detection in action.

---

## 🏗️ System Architecture

1. **Backend Core (`/src`):** Pure Python implementations of Graph Data Structures (Adjacency List), Segment Trees, DSU, and advanced routing algorithms.
2. **REST API (`api.py`):** A FastAPI layer that exposes the graph models and algorithms to web clients.
3. **Frontend Visualization (`/frontend`):** A sleek, dark-mode Vanilla JS application utilizing HTML5 `<canvas>` for zero-dependency, high-performance graph rendering and animation.

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- `pip` package manager

### Installation

1. **Clone the repository** and navigate to the project directory:
   ```bash
   git clone https://github.com/janviii09/Route-Planner.git
   cd Route-Planner
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Start the Backend Server**:
   ```bash
   python3 api.py
   ```

4. **Launch the UI**:
   Open your web browser and navigate to: [http://localhost:8000](http://localhost:8000)

---
