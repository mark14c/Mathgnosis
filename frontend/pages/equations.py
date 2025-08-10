"""Welcome to Reflex! This file outlines the Reflex UI."""

from rxconfig import config

import reflex as rx

from ..components.sidebar import sidebar
from .. import style


@rx.page(route="/equations", title="Equations")
def equations() -> rx.Component:
    """The equations page.

    Returns:
        The UI for the equations page.
    """
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Equations", font_size="2em"),
            rx.text("This is the equations page."),
            padding="1em",
        ),
        style=style.app_style,
    )
