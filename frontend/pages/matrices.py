import reflex as rx
from frontend.components.sidebar import sidebar

def matrices_page():
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Matrices", font_size="2em"),
            margin_left="250px",
            padding="1em",
        ),
    )
