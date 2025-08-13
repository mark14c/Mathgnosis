import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template
import httpx
import json

# --- Helper Data ---
DIST_PARAMS = {
    "bernoulli": ["p"], "binomial": ["n", "p"], "poisson": ["mu"],
    "normal": ["loc", "scale"], "geometric": ["p"], "beta": ["a", "b"],
    "gamma": ["a"], "hypergeometric": ["M", "n", "N"],
    "exponential": ["scale"], "chi_squared": ["df"],
}
HYPOTHESIS_TESTS = [
    "t_test_1_sample", "t_test_2_sample", "chi_squared_test", "f_test_anova"
]

from ..state import State

class ProbabilityState(State):
    # --- Section Control ---
    active_section: str = "standard_distributions"

    # --- Standard Distributions ---
    dist_name: str = "normal"
    dist_params: dict[str, str] = {"loc": "0", "scale": "1"}
    dist_calc_type: str = "pdf"
    dist_x1: str = "0.5"
    dist_x2: str = "1.0"
    dist_result: str = ""

    # --- Joint Distribution ---
    joint_rows: int = 2
    joint_cols: int = 2
    joint_table: list[list[str]] = [["0.1", "0.2"], ["0.3", "0.4"]]
    joint_result: str = ""

    # --- Custom PDF ---
    custom_pdf_str: str = "1/sqrt(2*pi) * exp(-x**2/2)"
    custom_lower_limit: str = "-1.0"
    custom_upper_limit: str = "1.0"
    custom_pdf_result: str = ""

    # --- Hypothesis Testing ---
    test_type: str = "t_test_1_sample"
    test_data1: str = "1.1, 1.2, 1.3, 1.4, 1.5"
    test_data2: str = "2.1, 2.2, 2.3, 2.4, 2.5"
    test_alpha: str = "0.05"
    test_mu: str = "0"
    test_result: str = ""

    # --- Generic Error ---
    error_message: str = ""

    # --- Event Handlers & Logic ---
    def on_dist_change(self, new_dist: str):
        self.dist_name = new_dist
        self.dist_params = {p: "" for p in DIST_PARAMS.get(new_dist, [])}

    def on_dist_param_change(self, param: str, value: str):
        self.dist_params[param] = value
    
    def on_joint_table_dim_change(self, value: str, is_rows: bool):
        try:
            dim = int(value)
            if is_rows: self.joint_rows = dim
            else: self.joint_cols = dim
            self.joint_table = [["0"] * self.joint_cols for _ in range(self.joint_rows)]
        except ValueError:
            pass # Ignore non-integer input

    def on_joint_table_cell_change(self, value: str, r: int, c: int):
        self.joint_table[r][c] = value

    # --- API Calls ---
    async def _run_dist_calc(self):
        async with self:
            self.error_message = ""
            try:
                payload = {
                    "dist_name": self.dist_name,
                    "params": {k: float(v) for k, v in self.dist_params.items()},
                    "calc_type": self.dist_calc_type,
                    "x1": float(self.dist_x1),
                    "x2": float(self.dist_x2) if self.dist_x2 else None,
                }
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/probability/standard_distribution", json=payload)
                if resp.status_code == 200: 
                    self.dist_result = str(resp.json()["result"])
                    self.save_to_history("probability", f"{self.dist_calc_type} for {self.dist_name}", f"params: {self.dist_params}, x1: {self.dist_x1}, x2: {self.dist_x2}", self.dist_result)
                else: self.error_message = resp.text
            except Exception as e: self.error_message = str(e)

    def run_dist_calc(self):
        return rx.background(self._run_dist_calc)

    async def _run_joint_calc(self):
        async with self:
            self.error_message = ""
            try:
                table = [[float(c) for c in r] for r in self.joint_table]
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/probability/joint_distribution", json={"table": table})
                if resp.status_code == 200: 
                    self.joint_result = json.dumps(resp.json()["result"], indent=2)
                    self.save_to_history("probability", "joint_distribution", f"table: {self.joint_table}", self.joint_result)
                else: self.error_message = resp.text
            except Exception as e: self.error_message = str(e)

    def run_joint_calc(self):
        return rx.background(self._run_joint_calc)

    async def _run_custom_pdf_calc(self):
        async with self:
            self.error_message = ""
            try:
                payload = {
                    "function_str": self.custom_pdf_str,
                    "lower_limit": float(self.custom_lower_limit),
                    "upper_limit": float(self.custom_upper_limit),
                }
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/probability/custom_pdf", json=payload)
                if resp.status_code == 200: 
                    self.custom_pdf_result = json.dumps(resp.json()["result"], indent=2)
                    self.save_to_history("probability", "custom_pdf", f"function: {self.custom_pdf_str}, limits: [{self.custom_lower_limit}, {self.custom_upper_limit}]", self.custom_pdf_result)
                else: self.error_message = resp.text
            except Exception as e: self.error_message = str(e)

    def run_custom_pdf_calc(self):
        return rx.background(self._run_custom_pdf_calc)

    async def _run_hypothesis_test(self):
        async with self:
            self.error_message = ""
            try:
                payload = {
                    "test_type": self.test_type,
                    "data1": [float(x.strip()) for x in self.test_data1.split(',')],
                    "data2": [float(x.strip()) for x in self.test_data2.split(',')] if self.test_data2 else None,
                    "alpha": float(self.test_alpha),
                    "mu": float(self.test_mu),
                }
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/probability/hypothesis_testing", json=payload)
                if resp.status_code == 200: 
                    self.test_result = json.dumps(resp.json()["result"], indent=2)
                    self.save_to_history("probability", f"{self.test_type}", f"data1: {self.test_data1}, data2: {self.test_data2}, alpha: {self.test_alpha}, mu: {self.test_mu}", self.test_result)
                else: self.error_message = resp.text
            except Exception as e: self.error_message = str(e)

    def run_hypothesis_test(self):
        return rx.background(self._run_hypothesis_test)

# --- UI Components ---
def create_card(*children, **props):
    return rx.card(rx.vstack(*children, spacing="3", align_items="start"), **props)

@rx.page(route="/probability", title="Probability")
def probability_page() -> rx.Component:
    content = rx.vstack(
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Standard Distributions", value="standard"),
                rx.tabs.trigger("Joint Distribution", value="joint"),
                rx.tabs.trigger("Custom PDF", value="custom"),
                rx.tabs.trigger("Hypothesis Testing", value="hypothesis"),
            ),
            # Standard Distributions
            rx.tabs.content(
                create_card(
                    rx.select(list(DIST_PARAMS.keys()), value=ProbabilityState.dist_name, on_change=ProbabilityState.on_dist_change),
                    rx.hstack(*[
                        rx.input(placeholder=param, value=ProbabilityState.dist_params.get(param, ""), on_change=lambda v, p=param: ProbabilityState.on_dist_param_change(p, v), style=style.input_style)
                        for param in DIST_PARAMS.get(ProbabilityState.dist_name, [])
                    ]),
                    rx.select(["pdf", "cdf", "between"], value=ProbabilityState.dist_calc_type, on_change=ProbabilityState.set_dist_calc_type),
                    rx.input(placeholder="x1", value=ProbabilityState.dist_x1, on_change=ProbabilityState.set_dist_x1, style=style.input_style),
                    rx.cond(ProbabilityState.dist_calc_type == "between", rx.input(placeholder="x2", value=ProbabilityState.dist_x2, on_change=ProbabilityState.set_dist_x2, style=style.input_style)),
                    rx.button("Calculate", on_click=ProbabilityState.run_dist_calc, style=style.button_style),
                    rx.code_block(ProbabilityState.dist_result, width="100%"),
                ), value="standard"
            ),
            # Joint Distribution
            rx.tabs.content(
                create_card(
                    rx.hstack(
                        rx.input(placeholder="Rows", value=str(ProbabilityState.joint_rows), on_change=lambda v: ProbabilityState.on_joint_table_dim_change(v, True), style=style.input_style),
                        rx.input(placeholder="Cols", value=str(ProbabilityState.joint_cols), on_change=lambda v: ProbabilityState.on_joint_table_dim_change(v, False), style=style.input_style),
                    ),
                    rx.vstack(
                        rx.foreach(
                            rx.Var.range(ProbabilityState.joint_rows),
                            lambda r: rx.hstack(
                                rx.foreach(
                                    rx.Var.range(ProbabilityState.joint_cols),
                                    lambda c: rx.input(
                                        value=ProbabilityState.joint_table[r][c],
                                        on_change=lambda v, r=r, c=c: ProbabilityState.on_joint_table_cell_change(v, r, c),
                                        style=style.input_style
                                    )
                                )
                            )
                        )
                    ),
                    rx.button("Calculate Marginals", on_click=ProbabilityState.run_joint_calc, style=style.button_style),
                    rx.code_block(ProbabilityState.joint_result, width="100%"),
                ), value="joint"
            ),
            # Custom PDF
            rx.tabs.content(
                create_card(
                    rx.input(placeholder="PDF function of x", value=ProbabilityState.custom_pdf_str, on_change=ProbabilityState.set_custom_pdf_str, style=style.input_style),
                    rx.hstack(
                        rx.input(placeholder="Lower Limit", value=ProbabilityState.custom_lower_limit, on_change=ProbabilityState.set_custom_lower_limit, style=style.input_style),
                        rx.input(placeholder="Upper Limit", value=ProbabilityState.custom_upper_limit, on_change=ProbabilityState.set_custom_upper_limit, style=style.input_style),
                    ),
                    rx.button("Calculate Area", on_click=ProbabilityState.run_custom_pdf_calc, style=style.button_style),
                    rx.code_block(ProbabilityState.custom_pdf_result, width="100%"),
                ), value="custom"
            ),
            # Hypothesis Testing
            rx.tabs.content(
                create_card(
                    rx.select(HYPOTHESIS_TESTS, value=ProbabilityState.test_type, on_change=ProbabilityState.set_test_type),
                    rx.text_area(placeholder="Data Sample 1 (comma-separated)", value=ProbabilityState.test_data1, on_change=ProbabilityState.set_test_data1, style=style.textarea_style),
                    rx.cond(ProbabilityState.test_type.contains("2_sample"), rx.text_area(placeholder="Data Sample 2", value=ProbabilityState.test_data2, on_change=ProbabilityState.set_test_data2, style=style.textarea_style)),
                    rx.cond(ProbabilityState.test_type.contains("1_sample"), rx.input(placeholder="Population Mean (mu)", value=ProbabilityState.test_mu, on_change=ProbabilityState.set_test_mu, style=style.input_style)),
                    rx.input(placeholder="Alpha", value=ProbabilityState.test_alpha, on_change=ProbabilityState.set_test_alpha, style=style.input_style),
                    rx.button("Run Test", on_click=ProbabilityState.run_hypothesis_test, style=style.button_style),
                    rx.code_block(ProbabilityState.test_result, width="100%"),
                ), value="hypothesis"
            ),
            defaultValue="standard",
        ),
        rx.cond(
            ProbabilityState.error_message,
            rx.callout.root(rx.callout.icon(rx.icon("alert_circle")), rx.callout.text(ProbabilityState.error_message), color_scheme="red", role="alert"),
        ),
    )
    return template(title="Probability", content=content)
