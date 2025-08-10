import reflex as rx
from frontend.components.sidebar import sidebar

def settings_page():
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Settings", font_size="2em"),
            margin_left="250px",
            padding="1em",
        ),
    )
