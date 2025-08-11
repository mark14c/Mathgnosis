import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
import httpx

class ComplexState(rx.State):
    # Polar to Rectangular
    polar_input: str = ""
    rectangular_output: str = ""

    # Rectangular to Polar
    rectangular_input: str = ""
    polar_output: str = ""

    # Complex Arithmetic
    complex_numbers_input: str = ""
    operation: str = "add"
    arithmetic_result: str = ""

    @rx.background
    async def polar_to_rectangular(self):
        async with self:
            try:
                r, theta = map(float, self.polar_input.split(','))
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.get_api_url()}/api/complex/polar_to_rectangular", json={"r": r, "theta": theta}
                    )
                if response.status_code == 200:
                    self.rectangular_output = response.json()["result"]
                else:
                    self.rectangular_output = f"Error: {response.text}"
            except Exception:
                self.rectangular_output = f"Error: Invalid input format."

    @rx.background
    async def rectangular_to_polar(self):
        async with self:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.get_api_url()}/api/complex/rectangular_to_polar", json={"rect_str": self.rectangular_input}
                    )
                if response.status_code == 200:
                    self.polar_output = response.json()["result"]
                else:
                    self.polar_output = f"Error: {response.text}"
            except Exception as e:
                self.polar_output = f"Error: {e}"

    @rx.background
    async def calculate_arithmetic(self):
        async with self:
            try:
                numbers = [s.strip() for s in self.complex_numbers_input.split(',')]
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.get_api_url()}/api/complex/arithmetic", json={"numbers": numbers, "operation": self.operation}
                    )
                if response.status_code == 200:
                    self.arithmetic_result = response.json()["result"]
                else:
                    self.arithmetic_result = f"Error: {response.text}"
            except Exception as e:
                self.arithmetic_result = f"Error: {e}"


def complex_page() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Complex Numbers", font_size="2em", margin_bottom="1em"),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Conversions", value="conversions"),
                    rx.tabs.trigger("Arithmetic", value="arithmetic"),
                ),
                rx.tabs.content(
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.heading("Polar to Rectangular", size="md"),
                                rx.input(
                                    placeholder="Enter r,θ (e.g., 5,36.87)",
                                    on_change=ComplexState.set_polar_input,
                                    width="100%",
                                ),
                                rx.button("Convert", on_click=ComplexState.polar_to_rectangular, width="100%"),
                                rx.text("Result:", weight="bold"),
                                rx.code(ComplexState.rectangular_output, variant="surface"),
                                spacing="4",
                            ),
                            width="100%",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.heading("Rectangular to Polar", size="md"),
                                rx.input(
                                    placeholder="Enter a+bj (e.g., 3+4j)",
                                    on_change=ComplexState.set_rectangular_input,
                                    width="100%",
                                ),
                                rx.button("Convert", on_click=ComplexState.rectangular_to_polar, width="100%"),
                                rx.text("Result:", weight="bold"),
                                rx.code(ComplexState.polar_output, variant="surface"),
                                spacing="4",
                            ),
                            width="100%",
                        ),
                        spacing="6",
                        width="100%",
                    ),
                    value="conversions",
                ),
                rx.tabs.content(
                    rx.card(
                        rx.vstack(
                            rx.heading("Complex Number Arithmetic", size="md"),
                            rx.text("Enter complex numbers separated by commas."),
                            rx.textarea(
                                placeholder="e.g., 1+2j, 3-4j, 5+6j",
                                on_change=ComplexState.set_complex_numbers_input,
                                width="100%",
                            ),
                            rx.select(
                                ["add", "subtract", "multiply", "divide"],
                                default_value="add",
                                on_change=ComplexState.set_operation,
                            ),
                            rx.button("Calculate", on_click=ComplexState.calculate_arithmetic, width="100%"),
                            rx.text("Result:", weight="bold"),
                            rx.code(ComplexState.arithmetic_result, variant="surface"),
                            spacing="4",
                        ),
                        width="100%",
                    ),
                    value="arithmetic",
                ),
                defaultValue="conversions",
                width="100%",
            ),
            padding="1em",
            margin_left=rx.cond(SidebarState.is_collapsed, "60px", "250px"),
            transition="margin-left 0.3s ease-in-out",
            width="100%",
        ),
        style=style.base_style,
    )