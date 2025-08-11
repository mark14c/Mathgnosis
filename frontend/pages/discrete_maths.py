import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template
import httpx
import json

class DiscreteMathsState(rx.State):
    # --- Number Theory ---
    nt_numbers_input: str = ""
    nt_modulo_input: str = ""
    nt_result: str = ""

    # --- Set Operations ---
    set_inputs: list[str] = ["", ""]
    set_op_result: str = ""

    # --- Boolean Logic ---
    bool_inputs: str = "true, false"
    bool_operation: str = "and"
    bool_result: str = ""
    
    # --- Graph Theory ---
    graph_adj_list: str = "A: B(7), C(9), F(14)\nB: C(10), D(15)\nC: D(11), F(2)\nD: E(6)\nE: F(9)"
    graph_is_directed: bool = False
    graph_start_node: str = "A"
    graph_end_node: str = "E"
    graph_analyses: list[str] = ["bfs", "dijkstra"]
    graph_result: dict = {}

    # --- Generic Error ---
    error_message: str = ""

    # --- Event Handlers ---
    def add_set_input(self):
        self.set_inputs.append("")

    def remove_set_input(self, index: int):
        if len(self.set_inputs) > 2:
            self.set_inputs.pop(index)

    def handle_set_input_change(self, value: str, index: int):
        self.set_inputs[index] = value

    # --- API Calls ---
    async def _run_number_theory_op(self, op: str):
        async with self:
            self.error_message = ""
            self.nt_result = ""
            endpoint = f"{self.get_api_url()}/api/discrete_maths/{op}"
            payload = {}
            try:
                if op in ["gcd", "lcm"]:
                    numbers = [int(n.strip()) for n in self.nt_numbers_input.split(',')]
                    payload = {"numbers": numbers}
                elif op == "modulo":
                    dividend, divisor = map(int, self.nt_modulo_input.split(','))
                    payload = {"dividend": dividend, "divisor": divisor}
                elif op == "prime_factorization":
                    number = int(self.nt_numbers_input)
                    payload = {"number": number}
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(endpoint, json=payload)
                
                if response.status_code == 200:
                    self.nt_result = str(response.json()["result"])
                else:
                    self.error_message = f"Error: {response.text}"
            except Exception as e:
                self.error_message = f"Invalid input: {e}"

    def run_number_theory_op(self, op: str):
        return rx.background(self._run_number_theory_op, op)

    async def _run_set_op(self, op: str):
        async with self:
            self.error_message = ""
            self.set_op_result = ""
            endpoint = f"{self.get_api_url()}/api/discrete_maths/{op}"
            try:
                parsed_sets = []
                for s_str in self.set_inputs:
                    s_str = s_str.strip()
                    if not s_str: continue
                    try:
                        s = json.loads(s_str.replace("'", '"'))
                        parsed_sets.append(s)
                    except (json.JSONDecodeError, TypeError):
                        parsed_sets.append([item.strip() for item in s_str.split(',')])

                if not parsed_sets or (len(parsed_sets) < 2 and op != "set_union"):
                    self.error_message = "This operation requires at least two valid sets."
                    return

                async with httpx.AsyncClient() as client:
                    response = await client.post(endpoint, json={"sets": parsed_sets})

                if response.status_code == 200:
                    self.set_op_result = str(response.json()["result"])
                else:
                    self.error_message = f"Error: {response.text}"
            except Exception as e:
                self.error_message = f"Invalid input format: {e}"

    def run_set_op(self, op: str):
        return rx.background(self._run_set_op, op)

    async def _run_bool_op(self):
        async with self:
            self.error_message = ""
            self.bool_result = ""
            endpoint = f"{self.get_api_url()}/api/discrete_maths/boolean_logic"
            try:
                inputs = [val.strip().lower() == 'true' for val in self.bool_inputs.split(',')]
                payload = {"inputs": inputs, "operation": self.bool_operation}
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(endpoint, json=payload)

                if response.status_code == 200:
                    self.bool_result = str(response.json()["result"])
                else:
                    self.error_message = f"Error: {response.text}"
            except Exception as e:
                self.error_message = f"Invalid input: {e}"

    def run_bool_op(self):
        return rx.background(self._run_bool_op)

    async def _run_graph_analysis(self):
        async with self:
            self.error_message = ""
            self.graph_result = {}
            endpoint = f"{self.get_api_url()}/api/discrete_maths/graph_analysis"
            try:
                payload = {
                    "adjacency_list_str": self.graph_adj_list,
                    "is_directed": self.graph_is_directed,
                    "analyses": self.graph_analyses,
                    "start_node": self.graph_start_node,
                    "end_node": self.graph_end_node,
                }
                async with httpx.AsyncClient() as client:
                    response = await client.post(endpoint, json=payload, timeout=20.0)
                
                if response.status_code == 200:
                    self.graph_result = response.json()["result"]
                else:
                    self.error_message = f"Error: {response.text}"
            except Exception as e:
                self.error_message = f"An error occurred: {e}"

    def run_graph_analysis(self):
        return rx.background(self._run_graph_analysis)

# --- UI Components ---
def create_analysis_checkboxes() -> rx.Component:
    algorithms = [
        "bfs", "dfs", "dijkstra", "bellman_ford", "floyd_warshall", "prims", 
        "kruskals", "kahns", "tarjans", "warshall_transitive_closure", 
        "max_flow_min_cut", "bipartite_check", "vertex_cover", "independent_set"
    ]
    return rx.checkbox_group(
        rx.grid(
            *[
                rx.checkbox(algo, value=algo)
                for algo in algorithms
            ],
            columns="3",
            spacing="1",
            width="100%",
        ),
        value=DiscreteMathsState.graph_analyses,
        on_change=DiscreteMathsState.set_graph_analyses,
    )

def render_graph_results(results: dict) -> rx.Component:
    return rx.vstack(
        *[
            rx.vstack(
                rx.heading(key.replace('_', ' ').title(), size="sm"),
                rx.code_block(
                    json.dumps(value, indent=2), 
                    language="json",
                    width="100%",
                    max_height="300px",
                    overflow="auto",
                ),
                align_items="start",
                width="100%",
            )
            for key, value in results.items()
        ],
        spacing="4",
        width="100%",
    )

@rx.page(route="/discrete_maths", title="Discrete Mathematics")
def discrete_maths_page() -> rx.Component:
    content = rx.accordion.root(
        # Number Theory Section
        rx.accordion.item(
            header="Number Theory",
            content=rx.vstack(
                rx.card(
                    rx.vstack(
                        rx.heading("GCD, LCM, Prime Factorization", size="sm"),
                        rx.input(placeholder="Numbers (e.g., 48, 18)", on_change=DiscreteMathsState.set_nt_numbers_input, style=style.input_style),
                        rx.hstack(
                            rx.button("GCD", on_click=lambda: DiscreteMathsState.run_number_theory_op("gcd"), style=style.button_style),
                            rx.button("LCM", on_click=lambda: DiscreteMathsState.run_number_theory_op("lcm"), style=style.button_style),
                            rx.button("Factorize", on_click=lambda: DiscreteMathsState.run_number_theory_op("prime_factorization"), style=style.button_style),
                        ),
                        rx.heading("Modulo", size="sm", margin_top="1em"),
                        rx.input(placeholder="Dividend, Divisor (e.g., 10, 3)", on_change=DiscreteMathsState.set_nt_modulo_input, style=style.input_style),
                        rx.button("Modulo", on_click=lambda: DiscreteMathsState.run_number_theory_op("modulo"), style=style.button_style),
                        rx.text("Result:", weight="bold", margin_top="1em"),
                        rx.code(DiscreteMathsState.nt_result, variant="surface"),
                    ),
                ),
                spacing="4",
            ),
        ),
        # Set Operations Section
        rx.accordion.item(
            header="Set Operations",
            content=rx.vstack(
                rx.card(
                    rx.vstack(
                        rx.heading("Enter Sets", size="sm"),
                        rx.text("Use comma-separated values (e.g., 1,2,3) or list format (e.g., [1, 2, \"a\"])"),
                        rx.foreach(
                            DiscreteMathsState.set_inputs,
                            lambda item, i: rx.hstack(
                                rx.input(
                                    placeholder=f"Set {i+1}",
                                    value=item,
                                    on_change=lambda val: DiscreteMathsState.handle_set_input_change(val, i),
                                    width="100%",
                                    style=style.input_style
                                ),
                                rx.button("-", on_click=lambda: DiscreteMathsState.remove_set_input(i), size="1", style=style.button_style),
                            )
                        ),
                        rx.button("Add Set", on_click=DiscreteMathsState.add_set_input, margin_top="0.5em", style=style.button_style),
                        rx.hstack(
                            rx.button("Union", on_click=lambda: DiscreteMathsState.run_set_op("set_union"), style=style.button_style),
                            rx.button("Intersection", on_click=lambda: DiscreteMathsState.run_set_op("set_intersection"), style=style.button_style),
                            rx.button("Difference (A-B)", on_click=lambda: DiscreteMathsState.run_set_op("set_difference"), style=style.button_style),
                            rx.button("Cartesian Product", on_click=lambda: DiscreteMathsState.run_set_op("set_cartesian_product"), style=style.button_style),
                        ),
                        rx.text("Result:", weight="bold", margin_top="1em"),
                        rx.code(DiscreteMathsState.set_op_result, variant="surface"),
                    )
                ),
                spacing="4",
            ),
        ),
        # Boolean Logic Section
        rx.accordion.item(
            header="Boolean Logic",
            content=rx.card(
                rx.vstack(
                    rx.heading("Boolean Inputs", size="sm"),
                    rx.text("Enter 'true' or 'false', comma-separated."),
                    rx.input(
                        value=DiscreteMathsState.bool_inputs,
                        on_change=DiscreteMathsState.set_bool_inputs,
                        style=style.input_style
                    ),
                    rx.select(
                        ["and", "or", "not", "nand", "nor", "xor", "xnor", "implies"],
                        default_value="and",
                        on_change=DiscreteMathsState.set_bool_operation,
                    ),
                    rx.button("Evaluate", on_click=DiscreteMathsState.run_bool_op, style=style.button_style),
                    rx.text("Result:", weight="bold", margin_top="1em"),
                    rx.code(DiscreteMathsState.bool_result, variant="surface"),
                )
            ),
        ),
        # Graph Theory Section
        rx.accordion.item(
            header="Graph Theory",
            content=rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading("Graph Input", size="5"),
                        rx.text("Enter Adjacency List:", size="sm"),
                        rx.text_area(
                            value=DiscreteMathsState.graph_adj_list,
                            on_change=DiscreteMathsState.set_graph_adj_list,
                            placeholder="A: B(1), C(4)\nB: C(2), D(5)\nC: D(1)\nD:",
                            height="200px",
                            width="100%",
                            style=style.textarea_style
                        ),
                        rx.hstack(
                            rx.text("Graph Type:", size="sm"),
                            rx.switch(
                                is_checked=DiscreteMathsState.graph_is_directed,
                                on_change=DiscreteMathsState.set_graph_is_directed,
                            ),
                            rx.text(rx.cond(DiscreteMathsState.graph_is_directed, "Directed", "Undirected")),
                            spacing="2",
                        ),
                        rx.heading("Analysis Options", size="5", margin_top="1em"),
                        create_analysis_checkboxes(),
                        rx.hstack(
                            rx.input(
                                placeholder="Start Node (e.g., A)",
                                value=DiscreteMathsState.graph_start_node,
                                on_change=DiscreteMathsState.set_graph_start_node,
                                style=style.input_style
                            ),
                            rx.input(
                                placeholder="End Node (for Max Flow)",
                                value=DiscreteMathsState.graph_end_node,
                                on_change=DiscreteMathsState.set_graph_end_node,
                                style=style.input_style
                            ),
                            width="100%",
                        ),
                        rx.button("Analyze Graph", on_click=DiscreteMathsState.run_graph_analysis, margin_top="1em", width="100%", style=style.button_style),
                        spacing="4",
                        width="50%",
                        align_items="start",
                    ),
                    rx.vstack(
                        rx.heading("Analysis Results", size="5"),
                        rx.cond(
                            DiscreteMathsState.graph_result,
                            render_graph_results(DiscreteMathsState.graph_result),
                            rx.text("Run analysis to see results."),
                        ),
                        spacing="4",
                        width="50%",
                        align_self="stretch",
                        height="100%",
                    ),
                    spacing="6",
                    width="100%",
                    align_items="start",
                ),
                rx.cond(
                    DiscreteMathsState.error_message,
                    rx.callout.root(
                        rx.callout.icon(rx.icon("alert-triangle")),
                        rx.callout.text(DiscreteMathsState.error_message),
                        color_scheme="red", role="alert",
                    ),
                ),
            ),
        ),
        collapsible=True, type="multiple", width="100%", default_value=["graph_theory"],
    )
    return template(title="Discrete Mathematics", content=content)