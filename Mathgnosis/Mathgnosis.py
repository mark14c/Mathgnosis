import reflex as rx
from frontend.components.sidebar import sidebar
from frontend.pages.calculator import calculator_page
from frontend.pages.complex import complex_page
from frontend.pages.matrices import matrices_page
from frontend.pages.vectors import vectors_page
from frontend.pages.calculus import calculus_page
from frontend.pages.discrete_maths import discrete_maths_page
from frontend.pages.statistics import statistics_page
from frontend.pages.probability import probability_page
from frontend.pages.history import history_page
from frontend.pages.settings import settings_page
from frontend.pages.equations import equations_page
from frontend.pages.graphs import graphs_page
from frontend.pages.unit_conversion import unit_conversion_page

class State(rx.State):
    """The app state."""

def index() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Welcome to Mathgnosis!", font_size="2em"),
            rx.text("Your one-stop solution for all things math."),
            margin_left="250px",
            padding="1em",
        ),
    )

app = rx.App()
app.add_page(index)
app.add_page(calculator_page, route="/calculator")
app.add_page(complex_page, route="/complex")
app.add_page(matrices_page, route="/matrices")
app.add_page(vectors_page, route="/vectors")
app.add_page(calculus_page, route="/calculus")
app.add_page(discrete_maths_page, route="/discrete_maths")
app.add_page(statistics_page, route="/statistics")
app.add_page(probability_page, route="/probability")
app.add_page(history_page, route="/history")
app.add_page(settings_page, route="/settings")
app.add_page(equations_page, route="/equations")
app.add_page(graphs_page, route="/graphs")
app.add_page(unit_conversion_page, route="/unit_conversion")
