import reflex as rx

config = rx.Config(
    app_name="Mathgnosis",
    api_url="http://127.0.0.1:8000",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
