import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from typing import List

PLOT_COLORS = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3"]

class GraphingState(rx.State):
    # --- 2D Graphing ---
    equations_2d: List[str] = ["sin(x)", "cos(x)"]
    
    # --- 3D Graphing ---
    equations_3d: List[str] = ["sin(x**2 + y**2)", "cos(x*y)"]

    # --- 2D Event Handlers ---
    def add_equation_2d(self):
        self.equations_2d.append("")

    def update_equation_2d(self, index: int, value: str):
        self.equations_2d[index] = value

    def remove_equation_2d(self, index: int):
        self.equations_2d.pop(index)

    # --- 3D Event Handlers ---
    def add_equation_3d(self):
        self.equations_3d.append("")

    def update_equation_3d(self, index: int, value: str):
        self.equations_3d[index] = value

    def remove_equation_3d(self, index: int):
        self.equations_3d.pop(index)

    # --- Computed Properties for Live-Updating Graphs ---
    @rx.var
    def figure_2d(self) -> go.Figure:
        import plotly.graph_objects as go
        import numpy as np
        import sympy as sp
        fig = go.Figure()
        x_vals = np.linspace(-10, 10, 400)
        x = sp.symbols('x')
        
        for i, eq_str in enumerate(self.equations_2d):
            if not eq_str.strip():
                continue
            try:
                expr = sp.sympify(eq_str)
                f = sp.lambdify(x, expr, 'numpy')
                y_vals = f(x_vals)
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=eq_str, line=dict(color=PLOT_COLORS[i % len(PLOT_COLORS)])))
            except Exception:
                # Silently fail on invalid equations
                continue
        
        fig.update_layout(title="2D Graph", xaxis_title="x", yaxis_title="y")
        return fig

    @rx.var
    def figure_3d(self) -> go.Figure:
        import plotly.graph_objects as go
        import numpy as np
        import sympy as sp
        fig = go.Figure()
        x_range = np.linspace(-5, 5, 50)
        y_range = np.linspace(-5, 5, 50)
        x_grid, y_grid = np.meshgrid(x_range, y_range)
        x, y = sp.symbols('x y')

        for i, eq_str in enumerate(self.equations_3d):
            if not eq_str.strip():
                continue
            try:
                expr = sp.sympify(eq_str)
                f = sp.lambdify((x, y), expr, 'numpy')
                z_grid = f(x_grid, y_grid)
                fig.add_trace(go.Surface(x=x_grid, y=y_grid, z=z_grid, name=eq_str, colorscale=PLOT_COLORS[i % len(PLOT_COLORS)], showscale=False, opacity=0.8))
            except Exception:
                continue
        
        fig.update_layout(title="3D Graph", scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"))
        return fig

def graphs_page() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Interactive Graphing", font_size="2em", margin_bottom="1em"),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("2D Graphs", value="2d"),
                    rx.tabs.trigger("3D Graphs", value="3d"),
                ),
                # 2D Graphing Tab
                rx.tabs.content(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Equations (y = f(x))", size="md"),
                            rx.foreach(
                                rx.Var.range(len(GraphingState.equations_2d)),
                                lambda i: rx.hstack(
                                    rx.input(
                                        placeholder="e.g., x**2",
                                        value=GraphingState.equations_2d[i],
                                        on_change=lambda val: GraphingState.update_equation_2d(i, val),
                                        width="100%",
                                    ),
                                    rx.button("X", on_click=lambda: GraphingState.remove_equation_2d(i), color_scheme="red"),
                                )
                            ),
                            rx.button("Add Equation", on_click=GraphingState.add_equation_2d, margin_top="1em"),
                            align_items="start",
                            spacing="3",
                            width="30%",
                        ),
                        rx.plotly(data=GraphingState.figure_2d, layout={}, width="70%", height="500px"),
                        spacing="6",
                        width="100%",
                    ),
                    value="2d",
                ),
                # 3D Graphing Tab
                rx.tabs.content(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Equations (z = f(x, y))", size="md"),
                            rx.foreach(
                                rx.Var.range(len(GraphingState.equations_3d)),
                                lambda i: rx.hstack(
                                    rx.input(
                                        placeholder="e.g., sin(x*y)",
                                        value=GraphingState.equations_3d[i],
                                        on_change=lambda val: GraphingState.update_equation_3d(i, val),
                                        width="100%",
                                    ),
                                    rx.button("X", on_click=lambda: GraphingState.remove_equation_3d(i), color_scheme="red"),
                                )
                            ),
                            rx.button("Add Equation", on_click=GraphingState.add_equation_3d, margin_top="1em"),
                            align_items="start",
                            spacing="3",
                            width="30%",
                        ),
                        rx.plotly(data=GraphingState.figure_3d, layout={}, width="70%", height="500px"),
                        spacing="6",
                        width="100%",
                    ),
                    value="3d",
                ),
                defaultValue="2d",
            ),
            padding="1em",
            margin_left=rx.cond(SidebarState.is_collapsed, "60px", "250px"),
            transition="margin-left 0.3s ease-in-out",
            width="100%",
        ),
        style=style.base_style,
    )