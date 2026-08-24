# Grateful Dead Tour Data Explorer

An interactive Streamlit application for exploring documented **Grateful Dead concerts from 1965–1995** through geography, venue history, setlists, and song-frequency analysis.

This project uses a music dataset to demonstrate the same analytical skills used in business work: **data cleaning, parsing semi-structured fields, geospatial visualization, aggregation, interactive filtering, and application design**.

## What the app does

### Interactive concert map

Shows geocoded concert locations across the United States using Folium and marker clustering. Each map point includes:

- venue
- city and state
- concert date
- available setlist

### Show explorer

Users can search by date or venue and inspect the recorded setlist for an individual show.

### Tour statistics

The app calculates and displays:

- total documented shows
- unique venues
- states visited
- unique songs
- active-year range
- most-played songs
- top cities by show count
- top states by show count

## Technical highlights

- **Geospatial visualization:** interactive Folium map with clustered concert markers
- **Semi-structured data parsing:** converts stored setlist strings into usable song lists
- **Reusable transformations:** helper functions standardize setlist parsing and frequency analysis
- **Cached processing:** Streamlit caching reduces repeated data work during interaction
- **Interactive search:** users can locate shows by date or venue
- **Custom UI:** includes a purpose-built visual theme and custom map markers

## Why this belongs in my portfolio

The subject matter is personal, but the workflow is broadly applicable. The project turns a large event-history dataset into an interface that lets a user answer questions quickly instead of manually searching rows.

The same pattern applies to operational data: **clean the source, create useful dimensions and measures, expose the right filters, and design the output around the user's question.**

## Repository structure

```text
GratefulDeadProject/
├── streamlit_app.py          # Interactive application
├── GratefulDead_geocoded.csv # Geocoded concert and setlist data
├── requirements.txt          # Runtime dependencies
├── .streamlit/               # Streamlit configuration
└── README.md
```

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Tools

**Python · pandas · Streamlit · Folium · streamlit-folium · Geospatial Analysis**

## Data note

The repository is intended as an analytical and visualization project. Concert and setlist information is historical source data; the application does not reproduce audio or other copyrighted media.
