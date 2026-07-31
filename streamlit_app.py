import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from collections import Counter
import ast
from streamlit_folium import folium_static

st.set_page_config(layout="wide", page_title="Grateful Dead Tour Data")

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
    avg_lat = df['Latitude'].mean()
    avg_lon = df['Longitude'].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=4, tiles="CartoDB dark_matter")
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in df.iterrows():
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            date_str = row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else 'Unknown'
            year_str = row['Date'].strftime('%Y') if pd.notna(row['Date']) else 'Unknown'

            songs = format_setlist(row['Setlist'])
            if songs:
                setlist_html = "<br>".join(f"{i}. {s}" for i, s in enumerate(songs, 1))
            else:
                setlist_html = "<i>Setlist not available</i>"

            popup_html = (
                f"<div style='font-family:sans-serif;min-width:210px'>"
                f"<b>{row['Venue']}</b><br>{row['City']}, {row['State']}<br>"
                f"<span style='color:#666'>{date_str}</span><hr style='margin:6px 0'>"
                f"<b>Setlist</b>"
                f"<div style='max-height:160px;overflow-y:auto;font-size:12px'>{setlist_html}</div>"
                f"</div>"
            )
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{row['City']}, {row['State']} - {year_str}"
            ).add_to(marker_cluster)
    return m


def app():
    st.title("Grateful Dead Tour Data Explorer")

    df_geocoded = load_data()

    st.header("Concert Locations Map")
    st.caption("Click any marker to see the venue, date, and full setlist for that show.")
    if not df_geocoded.empty:
        folium_static(build_map(df_geocoded), width=800, height=500)
    else:
        st.warning("No geocoded data available to display on the map.")

    st.header("🎵 Explore a Show's Setlist")
    df_sorted = df_geocoded.sort_values('Date').reset_index(drop=True)

    def show_label(row):
        d = row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else 'Unknown date'
        return f"{d} — {row['Venue']}, {row['City']}, {row['State']}"

    labels = [show_label(r) for _, r in df_sorted.iterrows()]
    choice = st.selectbox("Search by typing a date or venue, then pick a show:", labels, key="show_selector")
    selected = df_sorted.iloc[labels.index(choice)]

    songs = format_setlist(selected['Setlist'])
    if songs:
        st.write(f"**{len(songs)} songs played:**")
        for i, s in enumerate(songs, 1):
            st.write(f"{i}. {s}")
    else:
        st.info("No setlist recorded for this show.")

    col1, col2, col3 = st.columns(3)
    song_counts = get_song_counts(df_geocoded)
    if song_counts:
        with col1:
            st.subheader("Top 5 Most Played Songs")
            for song, count in song_counts.most_common(5):
                st.write(f"- {song.title()}: {count} times")
        with col2:
            st.subheader("5 Least Played Songs (Played Once)")
            played_once = [s for s, c in song_counts.items() if c == 1]
            if played_once:
                for song in played_once[:5]:
                    st.write(f"- {song.title()}")
            else:
                st.write("No songs found that were played only once.")
    else:
        with col1:
            st.warning("No song data to display.")
        with col2:
            st.warning("No song data to display.")

    with col3:
        st.subheader("Top 5 Cities & States")
        st.write("**Cities:**")
        for city, count in df_geocoded['City'].value_counts().nlargest(5).items():
            st.write(f"- {city}: {count} performances")
        st.write("**States:**")
        for state, count in df_geocoded['State'].value_counts().nlargest(5).items():
            st.write(f"- {state}: {count} performances")


if __name__ == '__main__':
    app()
