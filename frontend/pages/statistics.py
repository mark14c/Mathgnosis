import reflex as rx
from frontend.components.sidebar import sidebar

def statistics_page():
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Statistics", font_size="2em"),
            margin_left="250px",
            padding="1em",
        ),
    )
