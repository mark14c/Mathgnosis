import reflex as rx

class History(rx.Model, table=True):
    input: str
    operation: str
    output: str

class LatestHistory(rx.Model, table=True):
    input: str
    operation: str
    output: str
