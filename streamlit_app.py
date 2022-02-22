import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Autonomous Vehicle Data 🚗📊.")

@st.cache  # add caching so we load the data only once
def load_data():
    # Load the penguin data from https://github.com/allisonhorst/palmerpenguins.
    # TODO: Change this to load https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2017_AV_data.csv 
    # and https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2019_AV_data.csv
    penguins_url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/v0.1.0/inst/extdata/penguins.csv"
    seven_url = "https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2017_AV_data.csv"
    nine_url = "https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2019_AV_data.csv"
 #   return pd.read_csv(seven_url)
    return pd.read_csv(nine_url)

df = load_data()

st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df)

st.write("Hmm 🤔, is there some correlation between familiarity with autonomous vehicles and approval of Pittsburgh as a proving ground for them? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")

chart = alt.Chart(df).mark_point().encode(
    x=alt.X("FamiliarityTech", scale=alt.Scale(zero=False)),
    y=alt.Y("SafeAv", scale=alt.Scale(zero=False)),
    color=alt.Y("ProvingGround")
).properties(
    width=600, height=400
).interactive()

st.write(chart)

st.markdown("This project was created by Healy Dwyer and Jacqueline Liao for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
