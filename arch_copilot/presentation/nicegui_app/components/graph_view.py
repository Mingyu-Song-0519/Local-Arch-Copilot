"""
Graph View Component (using NetworkX & Cytoscape-like library or SVG)

NiceGUI에서 의존성 그래프를 시각적으로 표현합니다.
"""

from pathlib import Path
import json
from nicegui import ui
import networkx as nx


class GraphView:
    """의존성 그래프 시각화 컴포넌트"""

    def __init__(self, container_classes: str = 'w-full h-[600px] border border-zinc-800 rounded-3xl overflow-auto bg-zinc-950/50 relative') -> None:
        self.container_classes = container_classes

    def render(self, graph: nx.DiGraph):
        """Vis.js Network를 사용하여 신경망 느낌의 인터랙티브 그래프를 렌더링합니다."""
        print(f"DEBUG: Rendering neural graph with {len(graph.nodes)} nodes.")
        
        with ui.column().classes('w-full h-[700px] bg-zinc-950/40 border border-zinc-800 rounded-3xl overflow-hidden relative'):
            if not graph or len(graph.nodes) == 0:
                ui.label('No graph data available.').classes('m-auto text-zinc-500')
                return

            # 제목 및 안내
            with ui.row().classes('absolute top-4 left-6 z-10 items-center gap-3'):
                ui.icon('hub', color='primary').classes('text-xl animate-pulse')
                ui.label(f'Architectural Neural Network ({len(graph.nodes)} nodes)').classes('text-[10px] text-primary tracking-widest uppercase font-black opacity-80')

            # 1. 시각화 데이터 준비 (신경망 효과 극대화)
            nodes_data = []
            edges_data = []
            # 선명하고 사이버틱한 색상 조합
            layer_colors = {
                'domain': '#818cf8',      # Indigo (Core)
                'application': '#22d3ee', # Cyan (Flow)
                'infrastructure': '#a78bfa', # Violet (Base)
                'presentation': '#f472b6',   # Pink (Interface)
                None: '#4b5563'           # Gray
            }
            
            for node, attr in graph.nodes(data=True):
                path = Path(node)
                layer = attr.get('layer')
                color = layer_colors.get(layer, layer_colors[None])
                
                nodes_data.append({
                    'id': str(node),
                    'label': path.name,
                    'title': f"<b>Path:</b> {node}<br><b>Layer:</b> {layer or 'Unknown'}",
                    'color': {
                        'background': color,
                        'border': color,
                        'highlight': {'background': '#ffffff', 'border': color},
                        'hover': {'background': '#ffffff', 'border': color}
                    },
                    'font': {'color': color, 'size': 10, 'face': 'Inter', 'vadjust': -25},
                    'shape': 'dot',
                    'size': 8 if layer == 'domain' else 5,
                    'shadow': {'enabled': True, 'color': color, 'size': 15, 'x': 0, 'y': 0} # 글로잉 효과
                })

            for u, v, data in graph.edges(data=True):
                is_violation = data.get('has_violation', False)
                v_msg = data.get('violation_message', 'Architecture Violation')
                
                edge_style = {
                    'from': str(u),
                    'to': str(v),
                    'arrows': {'to': {'enabled': True, 'scaleFactor': 0.5}},
                    'color': {'color': '#ef4444' if is_violation else '#334155', 
                              'opacity': 0.8 if is_violation else 0.3, 
                              'highlight': '#ef4444' if is_violation else '#818cf8'},
                    'width': 2.5 if is_violation else 0.5,
                    'dashes': is_violation,
                    'hoverWidth': 3.0
                }
                
                if is_violation:
                    edge_style['title'] = f"""
                        <div style="padding: 10px; background: #000; border: 1px solid #ef4444; border-radius: 8px; color: #fff; font-size: 11px;">
                            <strong style="color: #ef4444;">⚠️ VIOLATION</strong><br>
                            {v_msg}
                        </div>
                    """
                
                edges_data.append(edge_style)

            # 2. 캔버스 엘리먼트
            target_id = f"neural_net_{abs(hash(str(graph.nodes)))}"
            canvas = ui.element('div').classes('w-full h-full').props(f'id="{target_id}"')
            
            # 3. 브라우저에서 신경망 레이아웃 엔진 구동
            js_code = f"""
            (function() {{
                const start = () => {{
                    const container = document.getElementById('{target_id}');
                    if (!container || typeof vis === 'undefined') {{
                        setTimeout(start, 500);
                        return;
                    }}
                    const data = {{
                        nodes: new vis.DataSet({json.dumps(nodes_data)}),
                        edges: new vis.DataSet({json.dumps(edges_data)})
                    }};
                    const options = {{
                        physics: {{
                            enabled: true,
                            solver: 'forceAtlas2Based',
                            forceAtlas2Based: {{
                                gravitationalConstant: -80,
                                centralGravity: 0.005,
                                springLength: 120,
                                springConstant: 0.08,
                                damping: 0.4,
                                avoidOverlap: 1
                            }},
                            stabilization: {{ iterations: 70, updateInterval: 10 }}
                        }},
                        interaction: {{
                            hover: true,
                            tooltipDelay: 100,
                            zoomView: true,
                            dragView: true,
                            navigationButtons: false
                        }},
                        nodes: {{ borderWidth: 2 }},
                        edges: {{ smooth: {{ type: 'continuous' }} }}
                    }};
                    const network = new vis.Network(container, data, options);
                    
                    // 초기 배치 완료 후 최적 줌
                    network.once('stabilizationIterationsDone', () => {{
                        network.fit({{ animation: true }});
                    }});
                }};
                start();
            }})();
            """
            ui.run_javascript(js_code)
