import reflex as rx

config = rx.Config(
    app_name="Mathgnosis",
    api_url="http://127.0.0.1:8000",
    db_url="sqlite:///data/history.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
