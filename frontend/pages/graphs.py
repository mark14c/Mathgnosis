"""Welcome to Reflex! This file outlines the Reflex UI."""

from rxconfig import config

import reflex as rx

from ..components.sidebar import sidebar
from .. import style


@rx.page(route="/graphs", title="Graphs")
def graphs() -> rx.Component:
    """The graphs page.

    Returns:
        The UI for the graphs page.
    """
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Graphs", font_size="2em"),
            rx.text("This is the graphs page."),
            padding="1em",
        ),
        style=style.app_style,
    )
