import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template

@rx.page(route="/history", title="History")
def history_page() -> rx.Component:
    content = rx.vstack(
        rx.text("This is the history page. You can add your history components here."),
    )
    return template(title="History", content=content)