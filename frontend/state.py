import reflex as rx
from Mathgnosis.models.history import History, LatestHistory

class State(rx.State):
    """The base state for the app."""
    color_mode: str = "light"

    def toggle_color_mode(self):
        if self.color_mode == "light":
            self.color_mode = "dark"
        else:
            self.color_mode = "light"
    
    def save_to_history(self, page, input, operation, output):
        with rx.session() as session:
            session.add(
                History(
                    page=page,
                    input=input,
                    operation=operation,
                    output=output
                )
            )
            session.commit()

        with rx.session() as session:
            latest_history = session.query(LatestHistory).all()
            if len(latest_history) >= 5:
                oldest = session.query(LatestHistory).order_by(LatestHistory.id).first()
                session.delete(oldest)
            
            session.add(
                LatestHistory(
                    page=page,
                    input=input,
                    operation=operation,
                    output=output
                )
            )
            session.commit()


class HistoryState(rx.State):
    
    history: list[History] = []
    latest_history: list[LatestHistory] = []

    def get_history(self):
        with rx.session() as session:
            self.history = session.query(History).all()[::-1]
            self.latest_history = session.query(LatestHistory).all()[::-1]