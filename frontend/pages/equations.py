import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template
import httpx
import json

from ..state import State

class EquationsState(State):
    # --- Polynomial Solver ---
    poly_coeffs: str = "1, -3, 2" # For x^2 - 3x + 2 = 0
    poly_result: str = ""

    # --- Simultaneous Solver ---
    sim_a_matrix: str = "2, 1\n1, 3"
    sim_b_vector: str = "5, 5"
    sim_result: str = ""

    # --- Generic Error ---
    error_message: str = ""

    # --- API Calls ---
    async def _solve_polynomial(self):
        async with self:
            self.error_message = ""
            try:
                coeffs = [float(c.strip()) for c in self.poly_coeffs.split(',')]
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/equations/solve_polynomial", json={"coefficients": coeffs})
                if resp.status_code == 200:
                    self.poly_result = json.dumps(resp.json()["result"], indent=2)
                    self.save_to_history("equations", f"solve_polynomial({self.poly_coeffs})", "solve_polynomial", self.poly_result)
                else:
                    self.error_message = resp.text
            except Exception as e:
                self.error_message = f"Invalid input: {e}"

    def solve_polynomial(self):
        return rx.background(self._solve_polynomial)

    async def _solve_simultaneous(self):
        async with self:
            self.error_message = ""
            try:
                a_matrix = [[float(n.strip()) for n in row.split(',')] for row in self.sim_a_matrix.strip().split('\n')]
                b_vector = [float(n.strip()) for n in self.sim_b_vector.split(',')]
                payload = {"a_matrix": a_matrix, "b_vector": b_vector}
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/equations/solve_simultaneous", json=payload)
                if resp.status_code == 200:
                    self.sim_result = json.dumps(resp.json()["result"], indent=2)
                    self.save_to_history("equations", f"solve_simultaneous(A={self.sim_a_matrix}, b={self.sim_b_vector})", "solve_simultaneous", self.sim_result)
                else:
                    self.error_message = resp.text
            except Exception as e:
                self.error_message = f"Invalid input or calculation error: {e}"

    def solve_simultaneous(self):
        return rx.background(self._solve_simultaneous)

@rx.page(route="/equations", title="Equation Solvers")
def equations_page() -> rx.Component:
    content = rx.vstack(
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Polynomial Solver", value="poly"),
                rx.tabs.trigger("Simultaneous Equations", value="sim"),
            ),
            # Polynomial Tab
            rx.tabs.content(
                rx.card(
                    rx.vstack(
                        rx.heading("Polynomial Root Finder", size="5"),
                        rx.text("Enter coefficients in order of decreasing power (e.g., '1, -3, 2' for x^2 - 3x + 2)."),
                        rx.input(placeholder="Coefficients", value=EquationsState.poly_coeffs, on_change=EquationsState.set_poly_coeffs, style=style.input_style),
                        rx.button("Find Roots", on_click=EquationsState.solve_polynomial, style=style.button_style),
                        rx.heading("Solutions for x", size="sm", margin_top="1em"),
                        rx.code_block(EquationsState.poly_result, width="100%"),
                        align_items="start", spacing="3",
                    )
                ), value="poly"
            ),
            # Simultaneous Equations Tab
            rx.tabs.content(
                rx.card(
                    rx.vstack(
                        rx.heading("Simultaneous Linear Equations (Ax = b)", size="5"),
                        rx.text("Coefficient Matrix (A)"),
                        rx.text_area(placeholder="A Matrix", value=EquationsState.sim_a_matrix, on_change=EquationsState.set_sim_a_matrix, style=style.textarea_style),
                        rx.text("Constants Vector (b)"),
                        rx.input(placeholder="b Vector", value=EquationsState.sim_b_vector, on_change=EquationsState.set_sim_b_vector, style=style.input_style),
                        rx.button("Solve", on_click=EquationsState.solve_simultaneous, style=style.button_style),
                        rx.heading("Solution Vector (x)", size="sm", margin_top="1em"),
                        rx.code_block(EquationsState.sim_result, width="100%"),
                        align_items="start", spacing="3",
                    )
                ), value="sim"
            ),
            defaultValue="poly",
        ),
        rx.cond(
            EquationsState.error_message,
            rx.callout.root(rx.callout.icon(rx.icon("alert-triangle")), rx.callout.text(EquationsState.error_message), color_scheme="red", role="alert"),
        ),
    )
    return template(title="Equation Solvers", content=content)
