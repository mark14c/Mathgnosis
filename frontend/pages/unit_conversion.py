"""Welcome to Reflex! This file outlines the Reflex UI."""

from rxconfig import config

import reflex as rx

from ..components.sidebar import sidebar
from .. import style


@rx.page(route="/unit_conversion", title="Unit Conversion")
def unit_conversion() -> rx.Component:
    """The unit conversion page.

    Returns:
        The UI for the unit conversion page.
    """
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Unit Conversion", font_size="2em"),
            rx.text("This is the unit conversion page."),
            padding="1em",
        ),
        style=style.app_style,
    )
