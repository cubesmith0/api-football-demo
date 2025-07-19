import streamlit as st
import requests
import pandas as pd

st.title("⚽ Canlı API‑Football Demo – Son 10 Maç")

api_key = st.secrets["API_KEY"]

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}
params = {"league": "39", "season": "2023", "last": "10"}

response = requests.get(url, headers=headers, params=params)
data = response.json()

if response.status_code != 200 or "response" not in data:
    st.error("Veri alınamadı. API key veya limit kontrolü yap.")
else:
    matches = []
    for f in data["response"]:
        m = f["fixture"]
        t = f["teams"]
        g = f["goals"]
        matches.append({
            "date": m["date"][:10],
            "home": t["home"]["name"],
            "away": t["away"]["name"],
            "home_goals": g["home"],
            "away_goals": g["away"]
        })
    df = pd.DataFrame(matches)
    st.dataframe(df)
    df.to_csv("last10.csv", index=False)
    st.success("CSV 'last10.csv' dosyasına kaydedildi!")
