import folium
from streamlit_folium import st_folium

from folium.plugins import MarkerCluster


print("he;;p")
def render_map(df):
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=6)

    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Flight: {row['Flight']}<br>City: {row['City']}<br>Status: {row['Status']}",
            icon=folium.Icon(
                color="green" if row["Status"] == "Resolved" else "red",
                icon="plane",
                prefix="fa"
            )
        ).add_to(marker_cluster)

    st_folium(m, width=800, height=500)

