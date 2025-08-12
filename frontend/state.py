import reflex as rx
from Mathgnosis.models.history import History, LatestHistory

class HistoryState(rx.State):
    
    history: list[History] = []
    latest_history: list[LatestHistory] = []

    def get_history(self):
        with rx.session() as session:
            self.history = session.query(History).all()
            self.latest_history = session.query(LatestHistory).all()

    def add_history(self, input, operation, output):
        with rx.session() as session:
            session.add(
                History(
                    input=input,
                    operation=operation,
                    output=output
                )
            )
            session.commit()
        self.get_history()

    def add_latest_history(self, input, operation, output):
        with rx.session() as session:
            if len(self.latest_history) >= 5:
                oldest = session.query(LatestHistory).first()
                session.delete(oldest)
            session.add(
                LatestHistory(
                    input=input,
                    operation=operation,
                    output=output
                )
            )
            session.commit()
        self.get_history()
