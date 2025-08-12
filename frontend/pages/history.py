import reflex as rx
from frontend.state import HistoryState
from frontend.components.page_layout import template

def create_history_table(title, history_list):
    return rx.vstack(
        rx.heading(title, size="md"),
        rx.table(
            headers=["Page", "Input", "Operation", "Output"],
            rows=[
                (
                    item.page,
                    item.input,
                    item.operation,
                    item.output,
                )
                for item in history_list
            ],
        ),
        align_items="left",
        width="100%",
    )

@rx.page(route="/history", title="History", on_load=HistoryState.get_history)
def history_page() -> rx.Component:
    content = rx.vstack(
        rx.heading("Calculation History", size="xl", padding_bottom="1rem"),
        create_history_table("Latest History", HistoryState.latest_history),
        rx.spacer(padding="1rem"),
        create_history_table("Full History", HistoryState.history),
        spacing="1.5em",
        width="100%",
        padding="1rem",
    )
    return template(title="History", content=content)
