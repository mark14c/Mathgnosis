import reflex as rx
from frontend.style import PRIMARY_COLOR

class SidebarState(rx.State):
    """The state for the sidebar."""
    is_collapsed: bool = False

    def toggle_collapse(self):
        """Toggle the collapsed state of the sidebar."""
        self.is_collapsed = not self.is_collapsed

def sidebar_item(text: str, href: str, icon: str) -> rx.Component:
    """A sidebar item with an icon and text."""
    return rx.link(
        rx.button(
            rx.hstack(
                rx.icon(tag=icon, size=20),
                rx.text(text, size="3"),
                spacing="3",
            ),
            width="100%",
            justify_content="flex-start",
            variant="ghost",
            color_scheme="gray",
        ),
        href=href,
        width="100%",
    )

def sidebar():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Mathgnosis", size="5", color="black"),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="pin_left", size=20),
                    on_click=SidebarState.toggle_collapse,
                    variant="ghost",
                    color_scheme="gray",
                ),
                width="100%",
                align_items="center",
            ),
            rx.divider(),
            rx.cond(
                ~SidebarState.is_collapsed,
                rx.vstack(
                    sidebar_item("Calculator", "/calculator", "calculator"),
                    sidebar_item("Complex Numbers", "/complex", "blending_mode"),
                    sidebar_item("Matrices", "/matrices", "grid"),
                    sidebar_item("Vectors", "/vectors", "arrow_right"),
                    sidebar_item("Calculus", "/calculus", "function"),
                    sidebar_item("Discrete Maths", "/discrete_maths", "component_1"),
                    sidebar_item("Statistics", "/statistics", "bar_chart"),
                    sidebar_item("Probability", "/probability", "pie_chart"),
                    sidebar_item("Equations", "/equations", "equal_to"),
                    sidebar_item("Graphs", "/graphs", "activity_log"),
                    sidebar_item("Unit Conversion", "/unit_conversion", "file_ruler"),
                    sidebar_item("History", "/history", "archive"),
                    sidebar_item("Settings", "/settings", "gear"),
                    spacing="2",
                    align_items="flex-start",
                    width="100%",
                ),
            ),
            spacing="4",
            align_items="flex-start",
            width="100%",
        ),
        position="fixed",
        left="0px",
        top="0px",
        z_index="5",
        h="100%",
        width=rx.cond(SidebarState.is_collapsed, "60px", "250px"),
        p="4",
        bg=PRIMARY_COLOR,
        box_shadow="2px 0 5px rgba(0, 0, 0, 0.1)",
        transition="width 0.3s ease-in-out",
    )