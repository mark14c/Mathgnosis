import reflex as rx
from ..components.sidebar import sidebar, SidebarState
from .. import style
from ..components.page_layout import template
import httpx

class UnitConverterState(rx.State):
    # --- State Variables ---
    all_units: dict[str, list[str]] = {}
    selected_category: str = "Length"
    from_unit: str = "meter"
    to_unit: str = "foot"
    input_value: str = "1"
    result: str = ""
    error_message: str = ""

    # --- Computed Properties ---
    @rx.var
    def categories(self) -> list[str]:
        return list(self.all_units.keys())

    @rx.var
    def current_units(self) -> list[str]:
        return self.all_units.get(self.selected_category, [])

    # --- Event Handlers ---
    async def on_load(self):
        """Fetch the unit list when the page loads."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.get_api_url()}/api/unit_converter/units")
            if resp.status_code == 200:
                self.all_units = resp.json()
                # Set default units for the initial category
                self.on_category_change(self.selected_category)
            else:
                self.error_message = "Failed to load unit data."
        except Exception as e:
            self.error_message = f"Error loading units: {e}"

    def on_category_change(self, category: str):
        self.selected_category = category
        # Reset units to defaults for the new category
        units = self.current_units
        if units:
            self.from_unit = units[0]
            self.to_unit = units[1] if len(units) > 1 else units[0]
        self.result = "" # Clear result on category change

    # --- Live Conversion ---
    async def _get_conversion(self):
        async with self:
            if not self.input_value or not self.from_unit or not self.to_unit:
                return
            try:
                value = float(self.input_value)
                payload = {"value": value, "from_unit": self.from_unit, "to_unit": self.to_unit}
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.get_api_url()}/api/unit_converter/convert", json=payload)
                if resp.status_code == 200:
                    self.result = f"{resp.json()['result']:.6g}"
                    self.error_message = ""
                else:
                    self.error_message = resp.text
            except ValueError:
                self.error_message = "Invalid input value."
            except Exception as e:
                self.error_message = f"Conversion error: {e}"

    def get_conversion(self):
        return rx.background(self._get_conversion)

@rx.page(route="/unit_conversion", title="Unit Converter", on_load=UnitConverterState.on_load)
def unit_conversion_page() -> rx.Component:
    content = rx.card(
        rx.vstack(
            rx.heading("Select Category", size="5"),
            rx.select(UnitConverterState.categories, value=UnitConverterState.selected_category, on_change=UnitConverterState.on_category_change),
            rx.hstack(
                rx.vstack(
                    rx.text("From"),
                    rx.input(value=UnitConverterState.input_value, on_change=UnitConverterState.set_input_value, on_blur=UnitConverterState.get_conversion, style=style.input_style),
                    rx.select(UnitConverterState.current_units, value=UnitConverterState.from_unit, on_change=UnitConverterState.set_from_unit),
                    width="100%",
                ),
                rx.vstack(
                    rx.text("To"),
                    rx.heading(UnitConverterState.result, size="6"),
                    rx.select(UnitConverterState.current_units, value=UnitConverterState.to_unit, on_change=UnitConverterState.set_to_unit),
                    width="100%",
                    align_items="end",
                ),
                align_items="end",
                width="100%",
                spacing="6",
            ),
            rx.cond(
                UnitConverterState.error_message,
                rx.callout.root(rx.callout.icon(rx.icon("alert-triangle")), rx.callout.text(UnitConverterState.error_message), color_scheme="red"),
            ),
            width="100%",
            spacing="4",
        )
    )
    return template(title="Unit Converter", content=content)
