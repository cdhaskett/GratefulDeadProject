import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from collections import Counter
import ast
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Grateful Dead Tour Data")

STEALIE_URI = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj4KICA8Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI0OCIgZmlsbD0iIzIzMWYyMCIvPgogIDxjbGlwUGF0aCBpZD0iYyI+PGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgcj0iNDUiLz48L2NsaXBQYXRoPgogIDxnIGNsaXAtcGF0aD0idXJsKCNjKSI+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iNTAiIGhlaWdodD0iMTAwIiBmaWxsPSIjMjUzMTdiIi8+CiAgICA8cmVjdCB4PSI1MCIgeT0iMCIgd2lkdGg9IjUwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2VlMWIyYyIvPgogICAgPHBvbHlnb24gcG9pbnRzPSI1Nyw1IDQzLDQ3IDUzLDQ3IDQzLDk1IDY0LDQ1IDUzLDQ1IDYxLDUiIGZpbGw9IiNmZmZmZmYiLz4KICA8L2c+CiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgcj0iNDUiIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2ZmZmZmZiIgc3Ryb2tlLXdpZHRoPSIzIi8+Cjwvc3ZnPgo="

@st.cache_data
def load_data():
    df = pd.read_csv('GratefulDead_geocoded.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

def format_setlist(setlist_str):
    try:
        songs = ast.literal_eval(str(setlist_str))
        songs = [s.strip() for s in songs if s and s.strip().lower() != 'unknown']
    except (ValueError, SyntaxError):
        songs = []
    return songs

@st.cache_data
def get_song_counts(df):
    all_songs = []
    for setlist_str in df['Setlist']:
        all_songs.extend(format_setlist(setlist_str))
    return Counter([s.lower() for s in all_songs])

@st.cache_resource
def build_map(df):
    m = folium.Map(location=[39.5, -96], zoom_start=4, tiles="CartoDB dark_matter")
    cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            date_str = row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else 'Unknown'
            year_str = row['Date'].strftime('%Y') if pd.notna(row['Date']) else 'Unknown'
            songs = format_setlist(row['Setlist'])
            setlist_html = "<br>".join(f"{i}. {s}" for i, s in enumerate(songs, 1)) if songs else "<i>Setlist not available</i>"
            popup_html = (
                f"<div style='font-family:sans-serif;min-width:210px'>"
                f"<b>{row['Venue']}</b><br>{row['City']}, {row['State']}<br>"
                f"<span style='color:#888'>{date_str}</span><hr style='margin:6px 0'>"
                f"<b>Setlist</b><div style='max-height:150px;overflow-y:auto;font-size:12px'>{setlist_html}</div></div>"
            )
            folium.Marker(
                [row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{row['City']}, {row['State']} - {year_str}",
                icon=folium.CustomIcon(STEALIE_URI, icon_size=(24, 24))
            ).add_to(cluster)
    return m


def app():
    df = load_data()
    song_counts = get_song_counts(df)

    # --- Header ---
    st.markdown(
        f"<h1 style='margin-bottom:0'><img src='{STEALIE_URI}' width='56' "
        f"style='vertical-align:middle;margin-right:14px'/>Grateful Dead Tour Data Explorer</h1>",
        unsafe_allow_html=True
    )
    st.caption("Every documented show, 1965–1995 · click a stealie on the map or search a date below")

    # --- Stat bar ---
    years = df['Date'].dt.year.dropna()
    year_range = f"{int(years.min())}–{int(years.max())}" if not years.empty else "—"
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Shows", f"{len(df):,}")
    m2.metric("Venues", f"{df['Venue'].nunique():,}")
    m3.metric("States", df['State'].nunique())
    m4.metric("Unique Songs", f"{len(song_counts):,}")
    m5.metric("Years Active", year_range)

    st.divider()

    # --- Map + Setlist side by side ---
    map_col, side_col = st.columns([2, 1], gap="large")

    with map_col:
        st.subheader("Concert Locations")
        st_folium(build_map(df), use_container_width=True, height=560, returned_objects=[])

    with side_col:
        st.subheader("Explore a Show")
        df_sorted = df.sort_values('Date').reset_index(drop=True)

        def show_label(row):
            d = row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else 'Unknown date'
            return f"{d} — {row['Venue']}, {row['City']}"

        labels = [show_label(r) for _, r in df_sorted.iterrows()]
        choice = st.selectbox("Type a date or venue to search:", labels, key="show_selector")
        selected = df_sorted.iloc[labels.index(choice)]
        songs = format_setlist(selected['Setlist'])

        with st.container(height=430, border=True):
            d = selected['Date'].strftime('%B %d, %Y') if pd.notna(selected['Date']) else 'Unknown date'
            st.markdown(f"**{selected['Venue']}**  \n{selected['City']}, {selected['State']} · {d}")
            if songs:
                st.caption(f"{len(songs)} songs played")
                for i, s in enumerate(songs, 1):
                    st.write(f"{i}. {s.title()}")
            else:
                st.info("No setlist recorded for this show.")

    st.divider()

    # --- Tour stats in cards ---
    st.subheader("Tour Stats")
    s1, s2, s3 = st.columns(3, gap="medium")

    with s1:
        with st.container(border=True):
            st.markdown("**🎸 Most Played Songs**")
            for song, count in song_counts.most_common(8):
                st.write(f"{song.title()} — **{count}**")

    with s2:
        with st.container(border=True):
            st.markdown("**📍 Top Cities**")
            for city, count in df['City'].value_counts().nlargest(8).items():
                st.write(f"{city} — **{count}**")

    with s3:
        with st.container(border=True):
            st.markdown("**🗺️ Top States**")
            for state, count in df['State'].value_counts().nlargest(8).items():
                st.write(f"{state} — **{count}**")


if __name__ == '__main__':
    app()
