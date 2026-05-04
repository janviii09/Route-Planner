from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.utils import load_graph
from src.router import Router
from src.kruskal import kruskal
from src.traffic import TrafficManager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(title="AI Route Planner Backend API")

# Allow CORS for potential web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the graph globally for the API
graph = load_graph('data/city_graph.json', 'data/traffic_weights.json')
traffic_manager = TrafficManager(graph)
router = Router(graph)

class RouteRequest(BaseModel):
    src: str
    dest: str
    emergency_mode: bool = False
    has_negative_weights: bool = False
    has_heuristic: bool = True
    hour: int = 6

@app.get("/")
def read_root():
    return RedirectResponse(url="/ui/index.html")

@app.post("/api/route")
def get_route(req: RouteRequest):
    if req.src not in graph.nodes or req.dest not in graph.nodes:
        raise HTTPException(status_code=400, detail="Invalid source or destination node.")
        
    traffic_manager.apply_traffic(req.hour)
    
    result = router.find_route(
        req.src, 
        req.dest, 
        req.emergency_mode, 
        req.has_negative_weights, 
        req.has_heuristic
    )
    return result

@app.get("/api/mst")
def get_mst(hour: int = 6):
    traffic_manager.apply_traffic(hour)
    mst_edges, total_weight, full_cost, trace = kruskal(graph)
    edges_list = [{"u": e.u, "v": e.v, "weight": e.weight} for e in mst_edges]
    return {"total_weight": total_weight, "full_cost": full_cost, "edges": edges_list, "trace": trace}

@app.get("/api/peak_congestion")
def get_peak_congestion(u: str, v: str, start_hour: int, end_hour: int):
    peak = traffic_manager.get_peak_congestion(u, v, start_hour, end_hour)
    if peak == -1:
        raise HTTPException(status_code=404, detail="Edge not found")
    return {"u": u, "v": v, "start_hour": start_hour, "end_hour": end_hour, "peak_weight": peak}

@app.get("/api/graph")
def get_graph_data(hour: int = 6):
    traffic_manager.apply_traffic(hour)
    nodes = {node_id: {"x": node.x, "y": node.y} for node_id, node in graph.nodes.items()}
    edges = [{"u": edge.u, "v": edge.v, "weight": edge.weight, "base_weight": edge.base_weight} for edge in graph.edges]
    return {"nodes": nodes, "edges": edges}

app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
