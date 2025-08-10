import reflex as rx

def sidebar():
    return rx.box(
        rx.vstack(
            rx.link("Calculator", href="/calculator"),
            rx.link("Complex Numbers", href="/complex"),
            rx.link("Matrices", href="/matrices"),
            rx.link("Vectors", href="/vectors"),
            rx.link("Calculus", href="/calculus"),
            rx.link("Discrete Maths", href="/discrete_maths"),
            rx.link("Statistics", href="/statistics"),
            rx.link("Probability", href="/probability"),
            rx.link("History", href="/history"),
            rx.link("Settings", href="/settings"),
            spacing="4",
            align_items="flex-start",
        ),
        position="fixed",
        left="0px",
        top="0px",
        z_index="5",
        h="100%",
        w="250px",
        p="4",
        bg="#f0f0f0",
    )