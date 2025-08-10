import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style

@rx.page(route="/complex", title="Complex Numbers")
def complex_page() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Complex Numbers", font_size="2em"),
            rx.text("This is the complex numbers page. You can add your complex number components here."),
            padding="1em",
            margin_left=rx.cond(SidebarState.is_collapsed, "60px", "250px"),
            transition="margin-left 0.3s ease-in-out",
        ),
        style=style.base_style,
    )
