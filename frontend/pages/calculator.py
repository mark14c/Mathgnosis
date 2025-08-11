import reflex as rx
import httpx
from ..components.sidebar import sidebar, SidebarState
from .. import style

class CalculatorState(rx.State):
    display: str = "0"
    expression: str = ""
    is_rad: bool = True

    def set_angle_unit(self, is_rad: bool):
        self.is_rad = is_rad

    def on_button_click(self, value: str):
        if self.display == "0" and value != ".":
            self.display = ""
        
        if value in ["sin", "cos", "tan", "asin", "acos", "atan", "log", "log10", "sqrt"]:
            self.expression += f"{value}("
            self.display += f"{value}("
        elif value == "nCr":
            self.expression += ", "
            self.display += "C"
        elif value == "nPr":
            self.expression += ", "
            self.display += "P"
        elif value == "^":
            self.expression += "**"
            self.display += "^"
        else:
            self.expression += value
            self.display += value

    def clear(self):
        self.display = "0"
        self.expression = ""

    def calculate(self):
        try:
            # Angle conversion
            if not self.is_rad:
                # This is a simplified approach. A more robust solution would involve
                # a proper parser to handle degrees conversion for trig functions.
                # For now, we assume the user enters angles in degrees and we convert
                # the whole expression, which is not ideal.
                pass # Leaving this for future improvement

            async def fetch_result():
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            "http://localhost:8000/api/calculator/eval",
                            json={"expression": self.expression}
                        )
                        response.raise_for_status()
                        result = response.json()["result"]
                        self.display = str(result)
                        self.expression = str(result)
                except httpx.HTTPStatusError as e:
                    self.display = "Error"
                    print(f"HTTP error occurred: {e}")
                except Exception as e:
                    self.display = "Error"
                    print(f"An error occurred: {e}")
            
            return fetch_result
        except Exception as e:
            self.display = "Error"

    def backspace(self):
        if len(self.display) > 1:
            self.display = self.display[:-1]
            # This is a simplification. A proper implementation would track the expression and display separately.
            if self.expression.endswith("**"):
                self.expression = self.expression[:-2]
            else:
                self.expression = self.expression[:-1]
        else:
            self.display = "0"
            self.expression = ""


def calculator_button(text: str, on_click, color_scheme="gray", variant="solid", size="4", **kwargs) -> rx.Component:
    return rx.button(
        text,
        on_click=on_click,
        color_scheme=color_scheme,
        variant=variant,
        size=size,
        height="80px",
        margin="5px",
        border_radius="15px",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
        **kwargs
    )

@rx.page(route="/calculator", title="Calculator")
def calculator_page() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.center(
            rx.vstack(
                rx.box(
                    rx.text(
                        CalculatorState.display,
                        font_size="3em",
                        font_weight="bold",
                        text_align="right",
                        padding="20px",
                        background_color="#f0f0f0",
                        border_radius="15px",
                        width="100%",
                        min_height="100px",
                        overflow_x="auto",
                    ),
                    width="450px",
                    margin_bottom="20px",
                ),
                rx.grid(
                    # Row 1
                    calculator_button("sin", lambda: CalculatorState.on_button_click("sin"), color_scheme="teal", width="80px"),
                    calculator_button("cos", lambda: CalculatorState.on_button_click("cos"), color_scheme="teal", width="80px"),
                    calculator_button("tan", lambda: CalculatorState.on_button_click("tan"), color_scheme="teal", width="80px"),
                    calculator_button("C", lambda: CalculatorState.clear(), color_scheme="red", width="80px"),
                    calculator_button("<-", lambda: CalculatorState.backspace(), color_scheme="orange", width="80px"),
                    # Row 2
                    calculator_button("asin", lambda: CalculatorState.on_button_click("asin"), color_scheme="teal", width="80px"),
                    calculator_button("acos", lambda: CalculatorState.on_button_click("acos"), color_scheme="teal", width="80px"),
                    calculator_button("atan", lambda: CalculatorState.on_button_click("atan"), color_scheme="teal", width="80px"),
                    calculator_button("nCr", lambda: CalculatorState.on_button_click("nCr"), color_scheme="blue", width="80px"),
                    calculator_button("nPr", lambda: CalculatorState.on_button_click("nPr"), color_scheme="blue", width="80px"),
                    # Row 3
                    calculator_button("log", lambda: CalculatorState.on_button_click("log10"), color_scheme="purple", width="80px"),
                    calculator_button("ln", lambda: CalculatorState.on_button_click("log"), color_scheme="purple", width="80px"),
                    calculator_button("^", lambda: CalculatorState.on_button_click("^"), color_scheme="orange", width="80px"),
                    calculator_button("(", lambda: CalculatorState.on_button_click("("), color_scheme="gray", width="80px"),
                    calculator_button(")", lambda: CalculatorState.on_button_click(")"), color_scheme="gray", width="80px"),
                    # Row 4
                    calculator_button("7", lambda: CalculatorState.on_button_click("7"), width="80px"),
                    calculator_button("8", lambda: CalculatorState.on_button_click("8"), width="80px"),
                    calculator_button("9", lambda: CalculatorState.on_button_click("9"), width="80px"),
                    calculator_button("/", lambda: CalculatorState.on_button_click("/"), color_scheme="orange", width="80px"),
                    calculator_button("%", lambda: CalculatorState.on_button_click("%"), color_scheme="orange", width="80px"),
                    # Row 5
                    calculator_button("4", lambda: CalculatorState.on_button_click("4"), width="80px"),
                    calculator_button("5", lambda: CalculatorState.on_button_click("5"), width="80px"),
                    calculator_button("6", lambda: CalculatorState.on_button_click("6"), width="80px"),
                    calculator_button("*", lambda: CalculatorState.on_button_click("*"), color_scheme="orange", width="80px"),
                    calculator_button("sqrt", lambda: CalculatorState.on_button_click("sqrt"), color_scheme="purple", width="80px"),
                    # Row 6
                    calculator_button("1", lambda: CalculatorState.on_button_click("1"), width="80px"),
                    calculator_button("2", lambda: CalculatorState.on_button_click("2"), width="80px"),
                    calculator_button("3", lambda: CalculatorState.on_button_click("3"), width="80px"),
                    calculator_button("-", lambda: CalculatorState.on_button_click("-"), color_scheme="orange", width="80px"),
                    calculator_button("=", lambda: CalculatorState.calculate(), color_scheme="green", width="80px"),
                    # Row 7
                    calculator_button("0", lambda: CalculatorState.on_button_click("0"), width="170px"),
                    calculator_button(".", lambda: CalculatorState.on_button_click("."), width="80px"),
                    calculator_button("+", lambda: CalculatorState.on_button_click("+"), color_scheme="orange", width="80px"),
                    
                    columns="5",
                    spacing="3",
                    width="450px",
                ),
                padding="2em",
                border="1px solid #ddd",
                border_radius="15px",
                background_color="#ffffff",
                box_shadow="lg",
            ),
            height="100vh",
            margin_left=rx.cond(SidebarState.is_collapsed, "60px", "250px"),
            transition="margin-left 0.3s ease-in-out",
        ),
        style=style.base_style,
    )