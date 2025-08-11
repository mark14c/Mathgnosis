import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template
import httpx
import json

class MatricesState(rx.State):
    matrix_inputs: list[str] = ["1, 2\n3, 4", "5, 6\n7, 8"]
    operation: str = "add"
    scalar_input: str = "2"
    result: str = ""
    error_message: str = ""

    def add_matrix(self):
        self.matrix_inputs.append("")

    def remove_matrix(self, index: int):
        if len(self.matrix_inputs) > 1:
            self.matrix_inputs.pop(index)

    def handle_matrix_input(self, value: str, index: int):
        self.matrix_inputs[index] = value

    def _parse_matrix(self, matrix_str: str) -> list[list[float]]:
        return [[float(n.strip()) for n in row.split(',')] for row in matrix_str.strip().split('\n')]

    async def _calculate(self):
        async with self:
            self.error_message = ""
            self.result = ""
            try:
                matrices = [self._parse_matrix(m_str) for m_str in self.matrix_inputs if m_str.strip()]
                if not matrices:
                    self.error_message = "Please enter at least one matrix."
                    return

                payload = {
                    "matrices": matrices,
                    "operation": self.operation,
                    "scalar": float(self.scalar_input) if self.scalar_input else 1.0
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.get_api_url()}/api/matrices/calculate",
                        json=payload,
                        timeout=20.0
                    )
                
                if response.status_code == 200:
                    res_data = response.json()["result"]
                    self.result = json.dumps(res_data, indent=2)
                else:
                    self.error_message = f"Error: {response.text}"

            except Exception as e:
                self.error_message = f"Invalid input format or calculation error: {e}"

    def calculate(self):
        return rx.background(self._calculate)

@rx.page(route="/matrices", title="Matrices")
def matrices_page() -> rx.Component:
    operations = [
        "add", "subtract", "multiply", "dot_product", "transpose", "adjoint", 
        "inverse", "determinant", "scalar_multiply", "rref", "null_space", 
        "range_space", "eigen", "norm", "exponentiation"
    ]
    
    content = rx.vstack(
        rx.heading("Define Matrices", size="6"),
        rx.text("Enter each matrix with commas separating values and new lines separating rows."),
        rx.foreach(
            MatricesState.matrix_inputs,
            lambda matrix, i: rx.hstack(
                rx.text_area(
                    placeholder=f"Matrix {i+1}",
                    value=matrix,
                    on_change=lambda val: MatricesState.handle_matrix_input(val, i),
                    height="120px",
                    width="250px",
                    style=style.textarea_style
                ),
                rx.button("X", on_click=lambda: MatricesState.remove_matrix(i), size="1", color_scheme="red", style=style.button_style),
                align="center",
            )
        ),
        rx.button("Add Matrix", on_click=MatricesState.add_matrix, margin_top="0.5em", style=style.button_style),
        
        rx.heading("Select Operation", size="6", margin_top="1.5em"),
        rx.select(
            operations,
            default_value="add",
            on_change=MatricesState.set_operation,
        ),
        rx.cond(
            MatricesState.operation == "scalar_multiply",
            rx.input(
                placeholder="Scalar Value",
                value=MatricesState.scalar_input,
                on_change=MatricesState.set_scalar_input,
                margin_top="0.5em",
                style=style.input_style
            )
        ),
        rx.button("Calculate", on_click=MatricesState.calculate, margin_top="1em", size="3", style=style.button_style),
        
        rx.heading("Result", size="6", margin_top="1.5em"),
        rx.cond(
            MatricesState.error_message,
            rx.callout.root(
                rx.callout.icon(rx.icon("alert-triangle")),
                rx.callout.text(MatricesState.error_message),
                color_scheme="red", role="alert",
            ),
        ),
        rx.code_block(
            MatricesState.result,
            language="json",
            width="100%",
            max_height="400px",
            overflow="auto",
        ),
        width="100%",
        spacing="4",
        align_items="start",
    )
    return template(title="Matrices", content=content)
