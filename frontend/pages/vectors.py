import reflex as rx
from frontend.components.sidebar import sidebar
from frontend.style import base_style, card_style

def vectors_page():
    return rx.box(
        sidebar(),
        rx.box(
            rx.card(
                rx.heading("Vectors", font_size="2em"),
                rx.text("This is the vectors page. You can add your vectors components here."),
                style=card_style
            ),
            margin_left="250px",
            padding="1em",
            style=base_style,
        ),
    )
