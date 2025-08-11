import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template

@rx.page(route="/settings", title="Settings")
def settings_page() -> rx.Component:
    content = rx.vstack(
        rx.text("This is the settings page. You can add your settings components here."),
    )
    return template(title="Settings", content=content)