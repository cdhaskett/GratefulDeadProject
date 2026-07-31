
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from collections import Counter
import ast
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Grateful Dead Tour Data")

@st.cache_data
def load_data():
    df = pd.read_csv('GratefulDead_geocoded.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

@st.cache_data
def get_song_counts(df):
    all_songs = []
    for setlist_str in df['Setlist']:
        try:
            setlist = ast.literal_eval(str(setlist_str))
            all_songs.extend(setlist)
        except (ValueError, SyntaxError):
            pass
    filtered_songs = [song.strip().lower() for song in all_songs if song and song.strip().lower() != 'unknown']
    return Counter(filtered_songs)


def app():
    st.title("Grateful Dead Tour Data Explorer")

    df_geocoded = load_data()

    # --- Map of all shows ---
    st.header("Concert Locations Map")
    if not df_geocoded.empty:
        avg_lat = df_geocoded['Latitude'].mean()
        avg_lon = df_geocoded['Longitude'].mean()
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=4)

        marker_cluster = MarkerCluster().add_to(m)

        for idx, row in df_geocoded.iterrows():
            if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                # Guard against dates that failed to parse
                date_str = row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else 'Unknown'
                year_str = row['Date'].strftime('%Y') if pd.notna(row['Date']) else 'Unknown'

                popup_text = f"<b>Date:</b> {date_str}<br>"
                popup_text += f"<b>Venue:</b> {row['Venue']}<br>"
                popup_text += f"<b>City:</b> {row['City']}, {row['State']}"
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=popup_text,
                    tooltip=f"{row['City']}, {row['State']} - {year_str}"
                ).add_to(marker_cluster)

        st_folium(m, width=800, height=500)
    else:
        st.warning("No geocoded data available to display on the map.")

    # --- Stats Section ---
    col1, col2, col3 = st.columns(3)

    song_counts = get_song_counts(df_geocoded)
    if song_counts:
        most_common_songs = song_counts.most_common(5)
        with col1:
            st.subheader("Top 5 Most Played Songs")
            for song, count in most_common_songs:
                st.write(f"- {song.title()}: {count} times")

        with col2:
            st.subheader("5 Least Played Songs (Played Once)")
            least_common_songs_played_once = [song for song, count in song_counts.items() if count == 1]
            if least_common_songs_played_once:
                for song in least_common_songs_played_once[:5]:
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
        top_cities = df_geocoded['City'].value_counts().nlargest(5)
        st.write("**Cities:**")
        for city, count in top_cities.items():
            st.write(f"- {city}: {count} performances")

        st.write("**States:**")
        top_states = df_geocoded['State'].value_counts().nlargest(5)
        for state, count in top_states.items():
            st.write(f"- {state}: {count} performances")


if __name__ == '__main__':
    app()
