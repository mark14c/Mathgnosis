import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template
from ..state import State

@rx.page(route="/settings", title="Settings")
def settings_page() -> rx.Component:
    content = rx.vstack(
        rx.hstack(
            rx.text("Theme"),
            rx.spacer(),
            rx.button(
                rx.color_mode_cond(light="Dark", dark="Light"),
                on_click=State.toggle_color_mode,
            ),
        ),
    )
    return template(title="Settings", content=content)