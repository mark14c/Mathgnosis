import reflex as rx

class History(rx.Model, table=True):
    page: str
    input: str
    operation: str
    output: str

class LatestHistory(rx.Model, table=True):
    page: str
    input: str
    operation: str
    output: str