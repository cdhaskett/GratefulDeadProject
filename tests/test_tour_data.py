import pandas as pd
import pytest

from tour_data import format_setlist, get_song_counts, load_tour_data, validate_columns


def test_format_setlist_cleans_unknown_and_whitespace():
    raw = "['  Scarlet Begonias ', 'Unknown', 'Fire on the Mountain']"
    assert format_setlist(raw) == ["Scarlet Begonias", "Fire on the Mountain"]


def test_format_setlist_handles_bad_input():
    assert format_setlist("not a list") == []
    assert format_setlist("{'song': 'Truckin'}") == []


def test_get_song_counts_is_case_insensitive():
    df = pd.DataFrame(
        {
            "Setlist": [
                "['Truckin', 'Ripple']",
                "['truckin', 'Bertha']",
            ]
        }
    )
    counts = get_song_counts(df)
    assert counts["truckin"] == 2
    assert counts["ripple"] == 1
    assert counts["bertha"] == 1


def test_validate_columns_reports_missing_fields():
    df = pd.DataFrame({"Date": ["1977-05-08"], "Venue": ["Barton Hall"]})
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_columns(df)


def test_load_tour_data_parses_dates(tmp_path):
    path = tmp_path / "shows.csv"
    pd.DataFrame(
        {
            "Date": ["1977-05-08"],
            "Venue": ["Barton Hall"],
            "City": ["Ithaca"],
            "State": ["NY"],
            "Latitude": [42.449],
            "Longitude": [-76.480],
            "Setlist": ["['Scarlet Begonias', 'Fire on the Mountain']"],
        }
    ).to_csv(path, index=False)

    df = load_tour_data(path)
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])
    assert df.loc[0, "Venue"] == "Barton Hall"
