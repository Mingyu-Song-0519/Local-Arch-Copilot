from pathlib import Path
import networkx as nx
from arch_copilot.domain.entities.project import FileNode, ProjectStructure
from arch_copilot.infrastructure.graph_engine.graph_engine import GraphEngine

def debug_graph():
    engine = GraphEngine()
    project = ProjectStructure(root_path=Path("/test"))
    project.add_file(FileNode(path=Path("a.py"), imports={"b"}))
    project.add_file(FileNode(path=Path("b.py"), imports={"c"}))
    project.add_file(FileNode(path=Path("c.py"), imports={"a"}))
    
    engine.build_graph(project)
    print(f"Nodes: {list(engine.graph.nodes)}")
    print(f"Edges: {list(engine.graph.edges)}")
    
    cycles = list(nx.simple_cycles(engine.graph))
    print(f"Cycles found: {cycles}")
    
    violations = engine.detect_cycles()
    print(f"Violations count: {len(violations)}")

if __name__ == "__main__":
    debug_graph()
