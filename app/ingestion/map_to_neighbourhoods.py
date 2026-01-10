from shapely.geometry import Point
import pandas as pd

from neighbourhoods import load_neighbourhoods_with_area
from load_washrooms import load_geojson, parse_features


def map_resources_to_neighbourhoods(resources, neighbourhoods_gdf):
    records = []

    for _, row in resources.iterrows():
        point = Point(row["longitude"], row["latitude"])
        matched = neighbourhoods_gdf[neighbourhoods_gdf.contains(point)]

        if not matched.empty:
            neighbourhood = matched.iloc[0]
            name = neighbourhood["AREA_NAME"]
            area_km2 = neighbourhood["area_km2"]
        else:
            name = "Unknown"
            area_km2 = None

        records.append(
            {
                "name": row["name"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "neighbourhood": name,
                "area_km2": area_km2,
            }
        )

    return pd.DataFrame(records)


def main():
    washrooms_df = parse_features(load_geojson())
    neighbourhoods_gdf = load_neighbourhoods_with_area()
    print(neighbourhoods_gdf.head())

    mapped_df = map_resources_to_neighbourhoods(
        washrooms_df, neighbourhoods_gdf
    )

    print(mapped_df.head())

    density = (
        mapped_df.groupby("neighbourhood")
        .agg(
            resource_count=("name", "count"),
            area_km2=("area_km2", "first"),
        )
        .assign(density=lambda df: df.resource_count / df.area_km2)
        .sort_values("density", ascending=False)
    )

    print(density.head(10))


if __name__ == "__main__":
    main()
