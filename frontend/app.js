const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');
let graphData = null;
let currentPath = [];
let mstEdges = [];

// DOM Elements
const srcSelect = document.getElementById('srcNode');
const destSelect = document.getElementById('destNode');
const btnRoute = document.getElementById('findRouteBtn');
const btnMst = document.getElementById('findMstBtn');
const resultsPanel = document.getElementById('results');

const timeSlider = document.getElementById('timeSlider');
const timeDisplay = document.getElementById('timeDisplay');
const edgeSelect = document.getElementById('edgeSelect');
const queryCongestionBtn = document.getElementById('queryCongestionBtn');
const congestionResult = document.getElementById('congestionResult');

// Fetch Graph Data
async function init() {
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    try {
        const res = await fetch('/api/graph');
        graphData = await res.json();
        populateSelects();
        drawGraph();
    } catch (err) {
        console.error("Failed to load graph", err);
    }
}

function resizeCanvas() {
    const container = canvas.parentElement;
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    if (graphData) drawGraph();
}

function populateSelects() {
    const nodes = Object.keys(graphData.nodes);
    srcSelect.innerHTML = '';
    destSelect.innerHTML = '';
    nodes.forEach(node => {
        srcSelect.add(new Option(node, node));
        destSelect.add(new Option(node, node));
    });
    if (nodes.length > 1) destSelect.selectedIndex = 1;

    edgeSelect.innerHTML = '';
    graphData.edges.forEach(edge => {
        const name = `${edge.u} - ${edge.v}`;
        edgeSelect.add(new Option(name, name));
    });
}

function getGraphBounds() {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (let id in graphData.nodes) {
        const n = graphData.nodes[id];
        if (n.x < minX) minX = n.x;
        if (n.y < minY) minY = n.y;
        if (n.x > maxX) maxX = n.x;
        if (n.y > maxY) maxY = n.y;
    }
    return { minX, minY, maxX, maxY };
}

function transform(x, y) {
    const bounds = getGraphBounds();
    const padding = 100;
    
    // Scale to fit canvas
    const scaleX = (canvas.width - padding * 2) / (bounds.maxX - bounds.minX || 1);
    const scaleY = (canvas.height - padding * 2) / (bounds.maxY - bounds.minY || 1);
    const scale = Math.min(scaleX, scaleY);

    // Center in canvas
    const cx = (bounds.maxX + bounds.minX) / 2;
    const cy = (bounds.maxY + bounds.minY) / 2;

    const tx = canvas.width / 2 + (x - cx) * scale;
    const ty = canvas.height / 2 + (y - cy) * scale;

    return { x: tx, y: ty };
}

function drawGraph() {
    if (!graphData) return;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw all edges
    ctx.lineWidth = 2;
    ctx.font = '14px Inter';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    graphData.edges.forEach(edge => {
        const u = graphData.nodes[edge.u];
        const v = graphData.nodes[edge.v];
        const p1 = transform(u.x, u.y);
        const p2 = transform(v.x, v.y);

        // Check if edge is in MST
        const isMst = mstEdges.some(e => (e.u === edge.u && e.v === edge.v) || (e.u === edge.v && e.v === edge.u));
        
        // Thicken if traffic is high
        const multiplier = edge.base_weight ? (edge.weight / edge.base_weight) : 1;
        const thickness = isMst ? 6 : (2 + (multiplier - 1) * 3);
        
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        
        // Color redder if congested
        if (isMst) {
            ctx.strokeStyle = '#10b981';
        } else if (multiplier >= 2.5) {
            ctx.strokeStyle = '#ef4444'; // Heavy traffic
        } else if (multiplier >= 1.5) {
            ctx.strokeStyle = '#f59e0b'; // Medium traffic
        } else {
            ctx.strokeStyle = '#475569'; // Normal
        }
        
        ctx.lineWidth = thickness;
        ctx.stroke();

        // Edge weight
        const mx = (p1.x + p2.x) / 2;
        const my = (p1.y + p2.y) / 2;
        
        ctx.fillStyle = '#1e293b';
        ctx.beginPath();
        ctx.arc(mx, my, 12, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#94a3b8';
        ctx.fillText(edge.weight, mx, my);
    });

    // Draw active path
    if (currentPath && currentPath.length > 0) {
        ctx.beginPath();
        for (let i = 0; i < currentPath.length; i++) {
            const node = graphData.nodes[currentPath[i]];
            const p = transform(node.x, node.y);
            if (i === 0) ctx.moveTo(p.x, p.y);
            else ctx.lineTo(p.x, p.y);
        }
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 6;
        ctx.stroke();
    }

    // Draw nodes
    for (let id in graphData.nodes) {
        const node = graphData.nodes[id];
        const p = transform(node.x, node.y);
        
        const isStart = currentPath.length > 0 && currentPath[0] === id;
        const isEnd = currentPath.length > 0 && currentPath[currentPath.length - 1] === id;
        
        ctx.beginPath();
        ctx.arc(p.x, p.y, 20, 0, Math.PI * 2);
        
        if (isStart) ctx.fillStyle = '#3b82f6';
        else if (isEnd) ctx.fillStyle = '#ef4444';
        else ctx.fillStyle = '#1e293b';
        
        ctx.fill();
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.fillStyle = '#f8fafc';
        ctx.fillText(id, p.x, p.y);
    }
}

btnRoute.addEventListener('click', async () => {
    const payload = {
        src: srcSelect.value,
        dest: destSelect.value,
        emergency_mode: document.getElementById('emergencyMode').checked,
        has_negative_weights: document.getElementById('negativeWeights').checked,
        has_heuristic: document.getElementById('useHeuristic').checked,
        hour: parseInt(timeSlider.value)
    };

    const res = await fetch('/api/route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    
    const data = await res.json();
    
    mstEdges = []; // Clear MST
    currentPath = data.path || [];
    drawGraph();

    // Update UI
    resultsPanel.classList.remove('hidden');
    document.getElementById('algoName').textContent = data.algorithm;
    document.getElementById('totalCost').textContent = data.cost;
    
    const pathNodesContainer = document.getElementById('pathNodes');
    pathNodesContainer.innerHTML = '';
    
    if (currentPath.length === 0) {
        pathNodesContainer.innerHTML = '<span style="color: #ef4444;">No Path Found</span>';
    } else {
        currentPath.forEach((node, index) => {
            const span = document.createElement('div');
            span.className = 'path-node';
            span.textContent = node;
            pathNodesContainer.appendChild(span);
            
            if (index < currentPath.length - 1) {
                const arrow = document.createElement('span');
                arrow.className = 'path-arrow';
                arrow.innerHTML = '&rarr;';
                pathNodesContainer.appendChild(arrow);
            }
        });
    }
});

btnMst.addEventListener('click', async () => {
    const res = await fetch(`/api/mst?hour=${timeSlider.value}`);
    const data = await res.json();
    
    currentPath = []; // Clear Route
    mstEdges = data.edges || [];
    drawGraph();
    
    resultsPanel.classList.remove('hidden');
    document.getElementById('algoName').textContent = "Kruskal's MST";
    document.getElementById('totalCost').textContent = data.total_weight;
    
    const pathNodesContainer = document.getElementById('pathNodes');
    pathNodesContainer.innerHTML = '<span style="color: #10b981;">Showing Minimum Spanning Tree</span>';
});

// Time slider event
timeSlider.addEventListener('input', async (e) => {
    const hour = parseInt(e.target.value);
    const ampm = hour >= 12 && hour < 24 ? 'pm' : 'am';
    const displayHour = hour > 12 ? hour - 12 : hour;
    timeDisplay.textContent = `${displayHour.toString().padStart(2, '0')}:00 ${ampm}`;
    
    // Fetch updated graph with new weights
    try {
        const res = await fetch(`/api/graph?hour=${hour}`);
        graphData = await res.json();
        drawGraph();
        
        // Automatically re-run route if we have one showing
        if (currentPath.length > 0 && document.getElementById('algoName').textContent !== "Kruskal's MST") {
            btnRoute.click();
        }
    } catch (err) {
        console.error("Failed to update time", err);
    }
});

// Peak Congestion Query Event
queryCongestionBtn.addEventListener('click', async () => {
    const edgeParts = edgeSelect.value.split(' - ');
    const u = edgeParts[0];
    const v = edgeParts[1];
    const startHour = document.getElementById('startHour').value;
    const endHour = document.getElementById('endHour').value;
    
    try {
        const res = await fetch(`/api/peak_congestion?u=${u}&v=${v}&start_hour=${startHour}&end_hour=${endHour}`);
        const data = await res.json();
        if (res.ok) {
            congestionResult.innerHTML = `Peak Weight: <span style="font-size: 1.2rem">${data.peak_weight}</span>`;
        } else {
            congestionResult.textContent = 'Error: ' + data.detail;
        }
    } catch (err) {
        congestionResult.textContent = 'Failed to fetch peak congestion';
    }
});

init();
