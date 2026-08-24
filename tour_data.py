"""Pure data helpers for the Grateful Dead Tour Data Explorer."""

import ast
from collections import Counter

import pandas as pd


REQUIRED_COLUMNS = {
    "Date",
    "Venue",
    "City",
    "State",
    "Latitude",
    "Longitude",
    "Setlist",
}


def validate_columns(df: pd.DataFrame) -> None:
    """Raise a clear error when the source file is missing required fields."""
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def load_tour_data(csv_path: str = "GratefulDead_geocoded.csv") -> pd.DataFrame:
    """Load the concert dataset and normalize the concert date."""
    df = pd.read_csv(csv_path)
    validate_columns(df)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def format_setlist(setlist_str) -> list[str]:
    """Convert a stored setlist representation into a clean list of songs."""
    try:
        songs = ast.literal_eval(str(setlist_str))
        if not isinstance(songs, (list, tuple)):
            return []
        return [
            str(song).strip()
            for song in songs
            if song and str(song).strip().lower() != "unknown"
        ]
    except (ValueError, SyntaxError):
        return []


def get_song_counts(df: pd.DataFrame) -> Counter:
    """Return case-normalized song frequencies across all recorded setlists."""
    all_songs = []
    for setlist_str in df["Setlist"]:
        all_songs.extend(format_setlist(setlist_str))
    return Counter(song.lower() for song in all_songs)
