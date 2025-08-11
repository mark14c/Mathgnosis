import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template
import httpx
import json

REGRESSION_MODELS = ["linear", "multiple_linear", "polynomial", "logistic", "lasso", "ridge"]

class StatisticsState(rx.State):
    # --- Descriptive Stats ---
    desc_data1: str = "1, 2, 3, 4, 5, 6, 7, 8, 9"
    desc_data2: str = "2, 3, 4, 5, 6, 7, 8, 9, 10" # For concordance
    desc_result: str = ""

    # --- Predictive Stats ---
    pred_model: str = "linear"
    pred_x_data: str = "1\n2\n3\n4\n5"
    pred_y_data: str = "2, 4, 5, 4, 6"
    pred_poly_degree: str = "2"
    pred_alpha: str = "1.0"
    pred_result: str = ""

    # --- Generic Error ---
    error_message: str = ""

    # --- API Calls ---
    async def _get_descriptive_stats(self):
        async with self:
            self.error_message = ""
            try:
                payload = {
                    "data1": [float(x.strip()) for x in self.desc_data1.split(',')],
                    "data2": [float(x.strip()) for x in self.desc_data2.split(',')] if self.desc_data2 else None,
                }
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/statistics/descriptive", json=payload)
                if resp.status_code == 200:
                    self.desc_result = json.dumps(resp.json()["result"], indent=2)
                else:
                    self.error_message = resp.text
            except Exception as e:
                self.error_message = f"Invalid input: {e}"

    def get_descriptive_stats(self):
        return rx.background(self._get_descriptive_stats)

    async def _run_regression(self):
        async with self:
            self.error_message = ""
            try:
                # Parse X data, handling multiple columns
                x_data = [[float(val) for val in row.split(',')] for row in self.pred_x_data.strip().split('\n')]
                y_data = [float(y.strip()) for y in self.pred_y_data.split(',')]
                
                params = {}
                if self.pred_model == "polynomial":
                    params["degree"] = int(self.pred_poly_degree)
                elif self.pred_model in ["lasso", "ridge"]:
                    params["alpha"] = float(self.pred_alpha)

                payload = {
                    "x_data": x_data,
                    "y_data": y_data,
                    "model_type": self.pred_model,
                    "params": params,
                }
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/statistics/regression", json=payload)
                if resp.status_code == 200:
                    self.pred_result = json.dumps(resp.json()["result"], indent=2)
                else:
                    self.error_message = resp.text
            except Exception as e:
                self.error_message = f"Calculation error: {e}"

    def run_regression(self):
        return rx.background(self._run_regression)

# --- UI Components ---
def create_card(*children, **props):
    return rx.card(rx.vstack(*children, spacing="3", align_items="start"), **props)

@rx.page(route="/statistics", title="Statistics")
def statistics_page() -> rx.Component:
    content = rx.vstack(
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Descriptive Statistics", value="desc"),
                rx.tabs.trigger("Predictive Statistics", value="pred"),
            ),
            # Descriptive Statistics Tab
            rx.tabs.content(
                create_card(
                    rx.heading("Data Input", size="md"),
                    rx.text("Enter comma-separated numerical data."),
                    rx.text_area(placeholder="Primary Dataset", value=StatisticsState.desc_data1, on_change=StatisticsState.set_desc_data1, style=style.textarea_style),
                    rx.text_area(placeholder="Second Dataset (for Concordance)", value=StatisticsState.desc_data2, on_change=StatisticsState.set_desc_data2, style=style.textarea_style),
                    rx.button("Calculate", on_click=StatisticsState.get_descriptive_stats, style=style.button_style),
                    rx.heading("Results", size="md", margin_top="1em"),
                    rx.code_block(StatisticsState.desc_result, width="100%"),
                ), value="desc"
            ),
            # Predictive Statistics Tab
            rx.tabs.content(
                create_card(
                    rx.heading("Model Selection", size="md"),
                    rx.select(REGRESSION_MODELS, value=StatisticsState.pred_model, on_change=StatisticsState.set_pred_model),
                    rx.heading("Data Input", size="md", margin_top="1em"),
                    rx.text("X (Independent Vars): One observation per line. Use commas for multiple variables."),
                    rx.text_area(placeholder="X Data", value=StatisticsState.pred_x_data, on_change=StatisticsState.set_pred_x_data, height="150px", style=style.textarea_style),
                    rx.text("Y (Dependent Var): Comma-separated."),
                    rx.text_area(placeholder="Y Data", value=StatisticsState.pred_y_data, on_change=StatisticsState.set_pred_y_data, height="80px", style=style.textarea_style),
                    
                    rx.cond(StatisticsState.pred_model == "polynomial",
                        rx.input(placeholder="Polynomial Degree", value=StatisticsState.pred_poly_degree, on_change=StatisticsState.set_pred_poly_degree, style=style.input_style)
                    ),
                    rx.cond((StatisticsState.pred_model == "lasso") | (StatisticsState.pred_model == "ridge"),
                        rx.input(placeholder="Alpha", value=StatisticsState.pred_alpha, on_change=StatisticsState.set_pred_alpha, style=style.input_style)
                    ),
                    
                    rx.button("Run Regression", on_click=StatisticsState.run_regression, margin_top="1em", style=style.button_style),
                    rx.heading("Model Results", size="md", margin_top="1em"),
                    rx.code_block(StatisticsState.pred_result, width="100%"),
                ), value="pred"
            ),
            defaultValue="desc",
        ),
        rx.cond(
            StatisticsState.error_message,
            rx.callout.root(rx.callout.icon(rx.icon("alert-triangle")), rx.callout.text(StatisticsState.error_message), color_scheme="red", role="alert"),
        ),
    )
    return template(title="Statistics", content=content)
