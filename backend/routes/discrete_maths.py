from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Tuple, Optional
import math
from itertools import product
import re
import networkx as nx

router = APIRouter(
    prefix="/discrete_maths",
    tags=["discrete_maths"],
)

# --- Number Theory ---
class NumbersRequest(BaseModel):
    numbers: List[int]

class ModuloRequest(BaseModel):
    dividend: int
    divisor: int

class FactorizationRequest(BaseModel):
    number: int

class GenericResponse(BaseModel):
    result: Any

@router.post("/gcd", response_model=GenericResponse)
def get_gcd(req: NumbersRequest):
    if len(req.numbers) < 2:
        raise HTTPException(400, "GCD requires at least two numbers.")
    result = math.gcd(*req.numbers)
    return {"result": result}

@router.post("/lcm", response_model=GenericResponse)
def get_lcm(req: NumbersRequest):
    if len(req.numbers) < 2:
        raise HTTPException(400, "LCM requires at least two numbers.")
    result = req.numbers[0]
    for i in range(1, len(req.numbers)):
        result = (result * req.numbers[i]) // math.gcd(result, req.numbers[i])
    return {"result": result}

@router.post("/modulo", response_model=GenericResponse)
def get_modulo(req: ModuloRequest):
    return {"result": req.dividend % req.divisor}

@router.post("/prime_factorization", response_model=GenericResponse)
def get_prime_factorization(req: FactorizationRequest):
    n = req.number
    factors = {}
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
       factors[n] = factors.get(n, 0) + 1
    return {"result": factors}

# --- Set Operations ---
class SetsRequest(BaseModel):
    sets: List[List[Any]]

@router.post("/set_union", response_model=GenericResponse)
def get_set_union(req: SetsRequest):
    if not req.sets:
        return {"result": []}
    result_set = set(req.sets[0])
    for s in req.sets[1:]:
        result_set.update(s)
    return {"result": sorted(list(result_set))}

@router.post("/set_intersection", response_model=GenericResponse)
def get_set_intersection(req: SetsRequest):
    if not req.sets:
        return {"result": []}
    result_set = set(req.sets[0])
    for s in req.sets[1:]:
        result_set.intersection_update(s)
    return {"result": sorted(list(result_set))}

@router.post("/set_difference", response_model=GenericResponse)
def get_set_difference(req: SetsRequest):
    if len(req.sets) < 2:
        raise HTTPException(400, "Difference requires at least two sets.")
    set_a = set(req.sets[0])
    set_b = set(req.sets[1])
    return {"result": sorted(list(set_a - set_b))}

@router.post("/set_cartesian_product", response_model=GenericResponse)
def get_cartesian_product(req: SetsRequest):
    if len(req.sets) < 2:
        raise HTTPException(400, "Cartesian product requires at least two sets.")
    result = list(product(*req.sets))
    return {"result": result}

# --- Boolean Logic ---
class BooleanRequest(BaseModel):
    inputs: List[bool]
    operation: str

@router.post("/boolean_logic", response_model=GenericResponse)
def evaluate_boolean_logic(req: BooleanRequest):
    op = req.operation.lower()
    inputs = req.inputs
    if len(inputs) < 1:
        raise HTTPException(400, "At least one input is required.")
    if op == 'not' and len(inputs) != 1:
        raise HTTPException(400, "NOT operation takes exactly one input.")
    if op != 'not' and len(inputs) < 2:
        raise HTTPException(400, "This operation requires at least two inputs.")

    result = False
    if op == 'and':
        result = all(inputs)
    elif op == 'or':
        result = any(inputs)
    elif op == 'not':
        result = not inputs[0]
    elif op == 'nand':
        result = not all(inputs)
    elif op == 'nor':
        result = not any(inputs)
    elif op == 'xor':
        result = (sum(inputs) % 2) != 0
    elif op == 'xnor':
        result = (sum(inputs) % 2) == 0
    elif op == 'implies':
        if len(inputs) != 2:
            raise HTTPException(400, "IMPLIES operation takes exactly two inputs.")
        result = not inputs[0] or inputs[1]
    else:
        raise HTTPException(400, f"Unknown operation: {op}")
    return {"result": result}

# --- Graph Theory ---
class GraphAnalysisRequest(BaseModel):
    adjacency_list_str: str
    is_directed: bool
    analyses: List[str]
    start_node: Optional[str] = None
    end_node: Optional[str] = None

def parse_adjacency_list(adj_str: str, is_directed: bool):
    G = nx.DiGraph() if is_directed else nx.Graph()
    nodes = set()
    
    for line in adj_str.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.split(':', 1)
        u = parts[0].strip()
        nodes.add(u)
        
        if len(parts) > 1 and parts[1].strip():
            neighbors = parts[1].split(',')
            for neighbor in neighbors:
                neighbor = neighbor.strip()
                match = re.match(r'(.+)\(.+)\)', neighbor)
                if match:
                    v, weight = match.groups()
                    v = v.strip()
                    G.add_edge(u, v, weight=float(weight))
                else:
                    v = neighbor
                    G.add_edge(u, v, weight=1.0) # Default weight
                nodes.add(v)
    
    # Add nodes that might be mentioned but don't have their own adj list entry
    for node in nodes:
        if not G.has_node(node):
            G.add_node(node)
            
    return G

@router.post("/graph_analysis", response_model=GenericResponse)
def analyze_graph(req: GraphAnalysisRequest):
    try:
        G = parse_adjacency_list(req.adjacency_list_str, req.is_directed)
    except Exception as e:
        raise HTTPException(400, f"Error parsing graph: {e}")

    results = {}
    
    # Basic Analysis
    results['vertices'] = list(G.nodes())
    results['edges'] = [f"({u}, {v}, w={d['weight']})" for u, v, d in G.edges(data=True)]
    if req.is_directed:
        results['degrees'] = {node: {'in': G.in_degree(node), 'out': G.out_degree(node)} for node in G.nodes()}
    else:
        results['degrees'] = dict(G.degree())
    try:
        results['adjacency_matrix'] = nx.to_numpy_array(G, nodelist=sorted(G.nodes())).tolist()
    except Exception:
        results['adjacency_matrix'] = "Could not generate matrix."

    # Advanced Analysis
    for analysis in req.analyses:
        try:
            if analysis == 'bfs' and req.start_node:
                results['bfs'] = list(nx.bfs_edges(G, source=req.start_node))
            elif analysis == 'dfs' and req.start_node:
                results['dfs'] = list(nx.dfs_edges(G, source=req.start_node))
            elif analysis == 'dijkstra' and req.start_node:
                results['dijkstra'] = nx.single_source_dijkstra_path(G, source=req.start_node)
            elif analysis == 'bellman_ford' and req.start_node:
                results['bellman_ford'] = nx.single_source_bellman_ford_path(G, source=req.start_node)
            elif analysis == 'floyd_warshall':
                results['floyd_warshall'] = dict(nx.floyd_warshall(G))
            elif analysis == 'prims':
                mst = nx.minimum_spanning_tree(G, algorithm='prim')
                results['prims'] = [f"({u}, {v}, w={d['weight']})" for u, v, d in mst.edges(data=True)]
            elif analysis == 'kruskals':
                mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
                results['kruskals'] = [f"({u}, {v}, w={d['weight']})" for u, v, d in mst.edges(data=True)]
            elif analysis == 'kahns' and req.is_directed:
                results['kahns'] = list(nx.topological_sort(G))
            elif analysis == 'tarjans' and req.is_directed:
                results['tarjans'] = [list(scc) for scc in nx.strongly_connected_components(G)]
            elif analysis == 'warshall_transitive_closure':
                tc = nx.transitive_closure(G)
                results['warshall_transitive_closure'] = list(tc.edges())
            elif analysis == 'max_flow_min_cut' and req.start_node and req.end_node:
                flow_value, flow_dict = nx.maximum_flow(G, req.start_node, req.end_node)
                results['max_flow_min_cut'] = {'max_flow': flow_value, 'min_cut_partition': nx.minimum_cut(G, req.start_node, req.end_node)[1]}
            elif analysis == 'bipartite_check':
                results['bipartite_check'] = nx.is_bipartite(G)
            elif analysis == 'vertex_cover':
                results['vertex_cover'] = list(nx.min_weighted_vertex_cover(G))
            elif analysis == 'independent_set':
                results['independent_set'] = list(nx.maximal_independent_set(G))

        except Exception as e:
            results[analysis] = f"Error: {e}"

    return {"result": results}
