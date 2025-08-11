import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template
import httpx
import json

class VectorsState(rx.State):
    vector_inputs: list[str] = ["1, 2, 3", "4, 5, 6"]
    matrix_input: str = "1, 0, 0\n0, 1, 0\n0, 0, 1"
    scalar_input: str = "3"
    operation: str = "add"
    result: str = ""
    error_message: str = ""

    def add_vector(self):
        self.vector_inputs.append("")

    def remove_vector(self, index: int):
        if len(self.vector_inputs) > 1:
            self.vector_inputs.pop(index)

    def handle_vector_input(self, value: str, index: int):
        self.vector_inputs[index] = value

    async def _calculate(self):
        async with self:
            self.error_message = ""
            self.result = ""
            try:
                vectors = [[float(n.strip()) for n in v_str.split(',')] for v_str in self.vector_inputs if v_str.strip()]
                if not vectors:
                    self.error_message = "Please enter at least one vector."
                    return

                payload = {"vectors": vectors, "operation": self.operation}
                if self.operation == "scalar_multiplication":
                    payload["scalar"] = float(self.scalar_input)
                if self.operation == "linear_transformation":
                    payload["matrix"] = [[float(n.strip()) for n in row.split(',')] for row in self.matrix_input.strip().split('\n')]

                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/vectors/calculate", json=payload, timeout=10.0)
                
                if resp.status_code == 200:
                    self.result = json.dumps(resp.json()["result"], indent=2)
                else:
                    self.error_message = f"Error: {resp.text}"
            except Exception as e:
                self.error_message = f"Invalid input or calculation error: {e}"

    def calculate(self):
        return rx.background(self._calculate)

@rx.page(route="/vectors", title="Vectors")
def vectors_page() -> rx.Component:
    operations = [
        "add", "subtract", "dot_product", "cross_product", "scalar_multiplication",
        "norm", "orthonormalize", "projection", "cosine_similarity", "linear_transformation"
    ]
    content = rx.vstack(
        rx.heading("Define Vectors", size="6"),
        rx.text("Enter each vector with comma-separated values."),
        rx.foreach(
            rx.Var.range(rx.length(VectorsState.vector_inputs)),
            lambda i: rx.hstack(
                rx.input(
                    placeholder=f"Vector {i+1}",
                    value=VectorsState.vector_inputs[i],
                    on_change=lambda val: VectorsState.handle_vector_input(val, i),
                    width="100%",
                    style=style.input_style
                ),
                rx.button("X", on_click=lambda: VectorsState.remove_vector(i), size="1", color_scheme="red", style=style.button_style),
            )
        ),
        rx.button("Add Vector", on_click=VectorsState.add_vector, margin_top="0.5em", style=style.button_style),
        
        rx.heading("Select Operation", size="6", margin_top="1.5em"),
        rx.select(operations, default_value="add", on_change=VectorsState.set_operation),
        
        rx.cond(VectorsState.operation == "scalar_multiplication",
            rx.input(placeholder="Scalar", value=VectorsState.scalar_input, on_change=VectorsState.set_scalar_input, style=style.input_style)
        ),
        rx.cond(VectorsState.operation == "linear_transformation",
            rx.text_area(placeholder="Transformation Matrix", value=VectorsState.matrix_input, on_change=VectorsState.set_matrix_input, style=style.textarea_style)
        ),

        rx.button("Calculate", on_click=VectorsState.calculate, margin_top="1em", size="3", style=style.button_style),
        
        rx.heading("Result", size="6", margin_top="1.5em"),
        rx.cond(
            VectorsState.error_message,
            rx.callout.root(rx.callout.icon(rx.icon("alert-triangle")), rx.callout.text(VectorsState.error_message), color_scheme="red"),
        ),
        rx.code_block(VectorsState.result, language="json", width="100%"),
        width="100%",
        spacing="4",
        align_items="start",
    )
    return template(title="Vectors", content=content)
