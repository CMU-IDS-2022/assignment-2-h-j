import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Autonomous Vehicle Data 🚗📊.")

@st.cache  # add caching so we load the data only once
def load_data_nine():
    # Load the penguin data from https://github.com/allisonhorst/palmerpenguins.
    # TODO: Change this to load https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2017_AV_data.csv 
    # and https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2019_AV_data.csv
    penguins_url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/v0.1.0/inst/extdata/penguins.csv"
    seven_url = "https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2017_AV_data.csv"
    nine_url = "https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2019_AV_data.csv"
 #   return pd.read_csv(seven_url)
    return pd.read_csv(nine_url)

def load_data_seven():
    seven_url = "https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-h-j/master/2017_AV_data.csv"
    return pd.read_csv(seven_url)

df_nine = load_data_nine()

df_seven = load_data_seven()

st.write("Let's look at raw data for 2019 in the Pandas Data Frame.")

st.write(df_nine)

st.write("Now, let's look at raw data for 2017 in the Pandas Data Frame.")

st.write(df_seven)

st.write("Hmm 🤔, is there some correlation between familiarity with autonomous vehicles and approval of Pittsburgh as a proving ground for them? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find out.")

chart = alt.Chart(df_nine).mark_point().encode(
    x=alt.X("FamiliarityTech", scale=alt.Scale(zero=False)),
    y=alt.Y("SafeAv", scale=alt.Scale(zero=False)),
    color=alt.Y("ProvingGround")
).properties(
    width=600, height=400
).interactive()

st.write(chart)

st.write("Is there a difference between 2017 and 2019 for the approval of Pittsburgh as a proving gound for AV testing? Let's compare bar charts with [Altair](https://altair-viz.github.io/) to find out.")

hist_2019 = alt.Chart(df_nine).mark_bar(
    tooltip=True
).encode(
    # alt.X("ProvingGround", type="nominal"),
    # alt.Y(aggregate="count", type="quantitative")
    alt.X("ProvingGround", type="nominal", axis = alt.Axis(title="Proving Ground Approval, 2019")),
    y='count()',
    #alt.Color("Species", scale=alt.Scale(domain=["Adelie", "Chinstrap", "Gentoo"], range=["orangered", "purple", "seagreen"]))
).properties(
	width=300, height=400
)

hist_2017 = alt.Chart(df_seven).mark_bar(
    tooltip=True
).encode(
    # alt.X("ProvingGround", type="nominal"),
    # alt.Y(aggregate="count", type="quantitative")
    alt.X("FeelingsProvingGround", type="nominal", axis = alt.Axis(title="Proving Ground Approval, 2017")),
    y='count()',
    #alt.Color("Species", scale=alt.Scale(domain=["Adelie", "Chinstrap", "Gentoo"], range=["orangered", "purple", "seagreen"]))
).properties(
	width=300, height=400
)

pg_compare = alt.hconcat(hist_2017, hist_2019)
st.write(pg_compare)

st.markdown("This project was created by Healy Dwyer and Jacqueline Liao for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
