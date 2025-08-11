from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pint import UnitRegistry, UndefinedUnitError

router = APIRouter(
    prefix="/unit_converter",
    tags=["unit_converter"],
)

ureg = UnitRegistry()
# Add custom definitions for pint if needed, e.g., gallons
ureg.define('gallon = 3.78541 * liter = gal')
ureg.define('quart = gallon / 4 = qt')
ureg.define('pint = quart / 2 = pt')
ureg.define('foot_candle = lm / ft**2')


# --- Data & Models ---
UNITS_CATEGORIES = {
    "Length": ["meter", "kilometer", "centimeter", "millimeter", "micrometer", "nanometer", "angstrom", "inch", "foot", "yard", "mile", "astronomical_unit"],
    "Mass": ["kilogram", "gram", "milligram", "microgram", "nanogram", "tonne", "pound", "ounce", "atomic_mass_unit"],
    "Time": ["second", "millisecond", "microsecond", "nanosecond", "minute", "hour", "day"],
    "Area": ["square_meter", "square_centimeter", "square_millimeter", "square_kilometer", "hectare", "square_inch", "square_foot", "square_yard", "acre"],
    "Volume": ["cubic_meter", "cubic_decimeter", "cubic_centimeter", "cubic_millimeter", "liter", "milliliter", "microliter", "cubic_foot", "cubic_inch", "gallon", "quart", "pint"],
    "Temperature": ["kelvin", "celsius", "fahrenheit"],
    "Velocity": ["m/s", "km/h", "cm/s", "ft/s", "mph", "knot"],
    "Pressure": ["pascal", "kilopascal", "megapascal", "bar", "millibar", "atmosphere", "mmHg", "torr", "psi"],
    "Energy": ["joule", "kilojoule", "megajoule", "watt_hour", "kilowatt_hour", "electron_volt", "calorie", "kilocalorie", "BTU"],
    "Power": ["watt", "kilowatt", "megawatt", "horsepower"],
    "Frequency": ["hertz"],
    "Electric Charge": ["coulomb", "milliampere_hour", "ampere_hour"],
    "Electric Potential": ["volt", "millivolt", "kilovolt"],
    "Resistance": ["ohm", "kiloohm", "megaohm"],
    "Magnetic Flux Density": ["tesla", "gauss"],
    "Luminous Flux": ["lumen"],
    "Illuminance": ["lux", "foot_candle"],
}

class ConversionRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str

class GenericResponse(BaseModel):
    result: any

# --- API Endpoints ---
@router.get("/units", response_model=Dict[str, List[str]])
def get_all_units():
    return UNITS_CATEGORIES

@router.post("/convert", response_model=GenericResponse)
def convert_units(req: ConversionRequest):
    try:
        quantity = ureg.Quantity(req.value, req.from_unit)
        converted_quantity = quantity.to(req.to_unit)
        return {"result": converted_quantity.magnitude}
    except UndefinedUnitError as e:
        raise HTTPException(400, f"Invalid unit specified: {e}")
    except Exception as e:
        raise HTTPException(500, f"An error occurred during conversion: {e}")
