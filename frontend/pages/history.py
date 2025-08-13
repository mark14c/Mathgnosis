import reflex as rx
from frontend.state import HistoryState
from frontend.components.page_layout import template

def create_history_table(title, history_list):
    return rx.vstack(
        rx.heading(title, size="6"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Page"),
                    rx.table.column_header_cell("Input"),
                    rx.table.column_header_cell("Operation"),
                    rx.table.column_header_cell("Output"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    history_list,
                    lambda item: rx.table.row(
                        rx.table.cell(item.page),
                        rx.table.cell(item.input),
                        rx.table.cell(item.operation),
                        rx.table.cell(item.output),
                    )
                )
            )
        ),
        align_items="left",
        width="100%",
    )

@rx.page(route="/history", title="History", on_load=HistoryState.get_history)
def history_page() -> rx.Component:
    content = rx.vstack(
        rx.heading("Calculation History", size="8", padding_bottom="1rem"),
        create_history_table("Latest History", HistoryState.latest_history),
        rx.spacer(padding="1rem"),
        create_history_table("Full History", HistoryState.history),
        spacing="4",
        width="100%",
        padding="1rem",
    )
    return template(title="History", content=content)
