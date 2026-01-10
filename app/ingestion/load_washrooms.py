import json
from pathlib import Path
from typing import Optional, Tuple
import pandas as pd


RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
WASHROOMS_FILE = RAW_DATA_DIR / "washrooms.geojson"


def load_geojson() -> dict:
    """
    Load raw GeoJSON file.
    """
    if not WASHROOMS_FILE.exists():
        raise FileNotFoundError(f"Washrooms file not found at {WASHROOMS_FILE}")

    with open(WASHROOMS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_coordinates(geometry: dict) -> Optional[Tuple[float, float]]:
    """
    Extract (latitude, longitude) from Point or single-coordinate MultiPoint.
    """
    geom_type = geometry.get("type")
    coords = geometry.get("coordinates")

    if geom_type == "Point" and len(coords) == 2:
        longitude, latitude = coords
        return latitude, longitude

    if geom_type == "MultiPoint" and isinstance(coords, list) and len(coords) == 1:
        point = coords[0]
        if len(point) == 2:
            longitude, latitude = point
            return latitude, longitude

    return None


def parse_features(geojson: dict) -> pd.DataFrame:
    """
    Parse GeoJSON features into a normalized DataFrame.
    """
    records = []

    for feature in geojson.get("features", []):
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})

        coords = extract_coordinates(geometry)
        if coords is None:
            continue

        latitude, longitude = coords

        name = (
            properties.get("location_name")
            or properties.get("name")
            or properties.get("alternative_name")
            or properties.get("location")
            or "Unknown"
        )

        records.append(
            {
                "name": name,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

    return pd.DataFrame.from_records(records)


def main():
    print("Loading washroom GeoJSON dataset...")

    geojson = load_geojson()
    df = parse_features(geojson)

    if df.empty:
        raise ValueError("No valid washroom records found")

    print(f"Loaded {len(df)} public washrooms")
    print("Columns:", ", ".join(df.columns))
    print(df.head())


if __name__ == "__main__":
    main()