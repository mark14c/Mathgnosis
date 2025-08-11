import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
import httpx

class CalculusState(rx.State):
    # Differentiation
    diff_function: str = ""
    diff_variables: str = ""
    diff_result: str = ""

    # Gradient
    grad_function: str = ""
    grad_result: str = ""

    # API call error
    error_message: str = ""

    async def _get_derivative(self):
        async with self:
            self.error_message = ""
            self.diff_result = ""
            try:
                vars_list = [v.strip() for v in self.diff_variables.split(',')]
                if not self.diff_function or not vars_list:
                    self.error_message = "Function and variables cannot be empty."
                    return

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.get_api_url()}/api/calculus/differentiate",
                        json={"function_str": self.diff_function, "variables": vars_list},
                        timeout=10,
                    )
                
                if response.status_code == 200:
                    self.diff_result = str(response.json()["result"])
                else:
                    self.error_message = f"Error: {response.json()['detail']}"

            except Exception as e:
                self.error_message = f"An unexpected error occurred: {e}"

    def get_derivative(self):
        return rx.background(self._get_derivative)

    async def _get_gradient(self):
        async with self:
            self.error_message = ""
            self.grad_result = ""
            try:
                if not self.grad_function:
                    self.error_message = "Function cannot be empty."
                    return

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.get_api_url()}/api/calculus/gradient",
                        json={"function_str": self.grad_function},
                        timeout=10,
                    )

                if response.status_code == 200:
                    self.grad_result = response.json()["result"]
                else:
                    self.error_message = f"Error: {response.json()['detail']}"

            except Exception as e:
                self.error_message = f"An unexpected error occurred: {e}"
    
    def get_gradient(self):
        return rx.background(self._get_gradient)


def create_calculus_card(title: str, content: rx.Component) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title, size="md"),
            content,
            spacing="4",
        ),
        width="100%",
    )

def calculus_page() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Calculus", font_size="2em", margin_bottom="1em"),
            rx.accordion.root(
                rx.accordion.item(
                    header="Differentiation",
                    content=rx.vstack(
                        create_calculus_card(
                            "Partial Derivative",
                            rx.vstack(
                                rx.input(
                                    placeholder="e.g., x**2 + y**3",
                                    on_change=CalculusState.set_diff_function,
                                ),
                                rx.input(
                                    placeholder="e.g., x, y",
                                    on_change=CalculusState.set_diff_variables,
                                ),
                                rx.button("Calculate", on_click=CalculusState.get_derivative),
                                rx.text("Result:", weight="bold"),
                                rx.code(CalculusState.diff_result, variant="surface"),
                            ),
                        ),
                        create_calculus_card(
                            "Gradient",
                            rx.vstack(
                                rx.input(
                                    placeholder="e.g., x**2*y + sin(z)",
                                    on_change=CalculusState.set_grad_function,
                                ),
                                rx.button("Calculate Gradient", on_click=CalculusState.get_gradient),
                                rx.text("Result (Gradient Vector):", weight="bold"),
                                rx.code(CalculusState.grad_result, variant="surface"),
                            ),
                        ),
                        rx.cond(
                            CalculusState.error_message,
                            rx.callout.root(
                                rx.callout.icon(rx.icon("alert-triangle")),
                                rx.callout.text(CalculusState.error_message),
                                color_scheme="red",
                                role="alert",
                            ),
                        ),
                        spacing="4",
                    ),
                ),
                rx.accordion.item(header="Integration", content=rx.text("Integration tools will be available here.")),
                rx.accordion.item(header="Differential Equations", content=rx.text("ODE solvers will be available here.")),
                rx.accordion.item(header="Transforms", content=rx.text("Laplace and Fourier transforms will be available here.")),
                collapsible=True,
                type="multiple",
                width="100%",
            ),
            padding="1em",
            margin_left=rx.cond(SidebarState.is_collapsed, "60px", "250px"),
            transition="margin-left 0.3s ease-in-out",
            width="100%",
        ),
        style=style.base_style,
    )