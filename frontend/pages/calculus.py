import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style

@rx.page(route="/calculus", title="Calculus")
def calculus_page() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Calculus", font_size="2em"),
            rx.text("This is the calculus page. You can add your calculus components here."),
            padding="1em",
            margin_left=rx.cond(SidebarState.is_collapsed, "60px", "250px"),
            transition="margin-left 0.3s ease-in-out",
        ),
        style=style.base_style,
    )
