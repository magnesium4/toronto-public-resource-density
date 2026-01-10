import json
from pathlib import Path
import pandas as pd
from shapely.geometry import Point, shape

from load_washrooms import load_geojson, parse_features


RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
NEIGHBOURHOODS_FILE = RAW_DATA_DIR / "neighbourhoods.geojson"


def load_neighbourhoods() -> list[dict]:
    if not NEIGHBOURHOODS_FILE.exists():
        raise FileNotFoundError(f"Neighbourhood file not found at {NEIGHBOURHOODS_FILE}")

    with open(NEIGHBOURHOODS_FILE, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    return geojson.get("features", [])


def map_resources_to_neighbourhoods(
    resources: pd.DataFrame,
    neighbourhoods: list[dict],
) -> pd.DataFrame:
    records = []

    for _, row in resources.iterrows():
        point = Point(row["longitude"], row["latitude"])
        neighbourhood_name = None

        for feature in neighbourhoods:
            polygon = shape(feature["geometry"])
            if polygon.contains(point):
                neighbourhood_name = feature["properties"].get(
                    "AREA_NAME", "Unknown"
                )
                break

        records.append(
            {
                "name": row["name"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "neighbourhood": neighbourhood_name,
            }
        )

    return pd.DataFrame(records)


def main():
    print("Loading washrooms...")
    washrooms_geojson = load_geojson()
    washrooms_df = parse_features(washrooms_geojson)

    print("Loading neighbourhood boundaries...")
    neighbourhoods = load_neighbourhoods()

    print("Mapping washrooms to neighbourhoods...")
    mapped_df = map_resources_to_neighbourhoods(washrooms_df, neighbourhoods)

    counts = (
        mapped_df.groupby("neighbourhood")
        .size()
        .sort_values(ascending=False)
    )

    print("\nWashrooms per neighbourhood:")
    print(counts.head(10))


if __name__ == "__main__":
    main()
