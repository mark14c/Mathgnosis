import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style

def template(title: str, content: rx.Component) -> rx.Component:
    return rx.box(
        sidebar(),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading(title, font_size="2em", margin_bottom="1em"),
                    content,
                    padding="2em",
                    border="1px solid #ddd",
                    border_radius="15px",
                    box_shadow="lg",
                ),
                style=style.card_style
            ),
            height="100vh",
            width="100%",
            margin_left=rx.cond(SidebarState.is_collapsed, "60px", "250px"),
            transition="margin-left 0.3s ease-in-out",
        ),
    )
