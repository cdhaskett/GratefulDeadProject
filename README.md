# Grateful Dead Tour Data Explorer

![Tests](https://github.com/cdhaskett/GratefulDeadProject/actions/workflows/tests.yml/badge.svg)

An interactive Streamlit project for exploring documented **Grateful Dead concerts from 1965–1995** through geography, venue history, setlists, and song-frequency analysis.

This one is personal on purpose. I wanted a portfolio project built around something I would actually enjoy digging into, while still demonstrating the same workflow I use with business data: **clean the source, structure messy fields, find the useful patterns, and build the output around the questions a person actually wants to answer.**

## The question behind the project

What does thirty years of touring look like when you stop treating it like a list of concerts and start treating it like a dataset?

The app makes it easy to explore questions such as:

- Where did the band play most often?
- Which cities and states show up again and again?
- What were the most frequently played songs?
- What was played at a particular show?
- How did a 30-year touring history spread geographically across the United States?

## What the app does

### Interactive concert map

A geocoded Folium map displays concert locations with marker clustering. Each map point includes the venue, city/state, concert date, and available setlist.

### Show explorer

Users can search by date or venue and inspect the recorded setlist for an individual concert instead of digging through rows of source data.

### Tour statistics

The app summarizes:

- documented shows
- unique venues
- states visited
- unique songs
- active-year range
- most-played songs
- top cities by show count
- top states by show count

## What this project demonstrates

- **Geospatial analysis:** maps geocoded event history with Folium and clustered markers
- **Semi-structured data parsing:** turns stored setlist strings into clean, reusable song lists
- **Data validation:** checks that required source fields exist before the app runs
- **Reusable analytics logic:** separates data preparation and aggregation from the Streamlit interface
- **Interactive application design:** lets users answer specific questions through search, maps, and summary metrics
- **Performance-minded development:** uses Streamlit caching to avoid unnecessary repeat processing
- **Automated testing:** validates setlist parsing, song counts, required columns, and date handling with pytest and GitHub Actions

## Why it belongs in my portfolio

The subject matter is music, but the analytical pattern is broadly applicable.

A large event-history file is not especially useful by itself. The value comes from cleaning it, creating reusable transformations, choosing useful dimensions and measures, and building an interface that lets somebody get to an answer quickly.

That is the same basic problem I enjoy solving with operational and business data — this version just has better songs.

## Project structure

```text
GratefulDeadProject/
├── streamlit_app.py           # Interactive Streamlit application
├── tour_data.py               # Reusable loading, validation, parsing, and aggregation logic
├── GratefulDead_geocoded.csv  # Geocoded concert and setlist data
├── tests/
│   └── test_tour_data.py      # Unit tests for core data logic
├── .github/workflows/
│   └── tests.yml              # Automated pytest workflow
├── requirements.txt           # Runtime dependencies
├── requirements-dev.txt       # Test dependencies
├── .streamlit/                # Streamlit configuration
└── README.md
```

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

To run the tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Tools

**Python · pandas · Streamlit · Folium · streamlit-folium · pytest · GitHub Actions · Geospatial Analysis**

## Data note

The repository is an analytical and visualization project using historical concert and setlist information. The application does not reproduce audio or other copyrighted media.
