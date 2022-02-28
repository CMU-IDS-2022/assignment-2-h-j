import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some data about autonomous vehicles, collected from Pittsburgh residents 🚗📊.")

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

st.write("We're interested in seeing how opinions about AVs and using Pittsburgh as a testing 'Proving Ground' for AVs have changed from 2017 to 2019.")

st.write("First, Let's look at raw data for 2017 in the Pandas Data Frame.")

st.write(df_seven)

st.write("Now, let's look at raw data for 2019 in the Pandas Data Frame.")

st.write(df_nine)

st.write("Hmm 🤔, is there a difference between 2017 and 2019 for the approval of Pittsburgh as a proving gound for AV testing? Let's compare bar charts with [Altair](https://altair-viz.github.io/) to find out.")

hist_2019 = alt.Chart(df_nine).mark_bar(
    tooltip=True
).encode(
    # alt.X("ProvingGround", type="nominal"),
    # alt.Y(aggregate="count", type="quantitative")
    alt.X("ProvingGround", type="nominal", axis = alt.Axis(title="Proving Ground Approval, 2019"), sort=[
        'Approve',
        'Somewhat Approve',
        'Neutral',
        'Somewhat Disapprove',
        'Disapprove',
        'nan']),
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
    alt.X("FeelingsProvingGround", type="nominal", axis = alt.Axis(title="Proving Ground Approval, 2017"), sort=[
        'Approve',
        'Somewhat Approve',
        'Neutral',
        'Somewhat Disapprove',
        'Disapprove',
        'nan']),
    y='count()',
    #alt.Color("Species", scale=alt.Scale(domain=["Adelie", "Chinstrap", "Gentoo"], range=["orangered", "purple", "seagreen"]))
).properties(
	width=300, height=400
)

pg_compare = alt.hconcat(hist_2017, hist_2019)
st.write(pg_compare)

st.write("There doesn't seem to be much of a difference between 2017 and 2019 based on the charts above. Let's try another way of investigating our question by looking at the interaction between **approval of Pittsburgh as a proving ground in 2019** and **impact of the 2018 Arizona Uber crash** from the 2019 data.")

pg_brush = alt.selection_multi(fields=['ProvingGround'])
arizona_brush = alt.selection_multi(fields=['ArizonaCrash'])
pg_2019_chart = alt.Chart(df_nine, title='Proving Ground Approval, 2019').transform_filter(arizona_brush).mark_bar().encode(
    x='count()',
    y= alt.Y('ProvingGround', type="nominal", sort=[
        'Approve',
        'Somewhat Approve',
        'Neutral',
        'Somewhat Disapprove',
        'Disapprove',
        'nan']),
    color=alt.condition(pg_brush, alt.value('steelblue'), alt.value('lightgray'))
).add_selection(pg_brush).interactive()
arizona_chart = alt.Chart(df_nine, title='Impact of 2018 Arizona Uber Crash on AV Opinion').transform_filter(pg_brush).mark_bar().encode(
    x='count()',
    y=alt.Y('ArizonaCrash', sort=[
        'Significantly more negative opinion',
        'Somewhat more negative opinion',
        'No change',
        'Somewhat more positive opinion',
        'Significantly more positive opinion',
        'nan']),
    color=alt.condition(arizona_brush, alt.value('salmon'), alt.value('lightgray'))
).add_selection(arizona_brush).interactive()

st.altair_chart(pg_2019_chart & arizona_chart)

st.write("From the charts above, it appears that for the majority of survey responders, the 2018 crash did not impact their opnions on AVs, and most Pittsburghers still approve of Pittsburgh as a testing groundfor AVs. Unsurprisingly, however, residents who responded **Significantly more negative opinion** to the Arizona Crash question mostly disapproved of using Pittsburgh as a proving ground.")

st.write("Lastly, we're interested in finding out if people feel safer sharing the road with human drivers vs AVs. Do people trust their fellow humans or robots more? Let's look at the 2019 data to see.")

hist_humans = alt.Chart(df_nine).mark_bar(size=20,
    tooltip=True
).encode(
     x=alt.X('SafeHuman', sort='-y', axis = alt.Axis(title="Safety Sharing Road with Human Drivers. (0 = Very Unsafe, 5 = Very Safe)", tickMinStep=1)),
     y='count()',
).properties(
	width=300, height=400
).interactive()

selection = alt.selection_multi(fields=['SafeAv'], bind='legend')

hist_avs = alt.Chart(df_nine).mark_bar(size=20,
    tooltip=True
).encode(
     x=alt.X('SafeAv', sort='-y', axis = alt.Axis(title="Safety Sharing Road with AVs. (0 = Very Unsafe, 5 = Very Safe)", tickMinStep=1)),
     y='count()',
).properties(
	width=300, height=400
).interactive().add_selection(
    selection
)

human_av_compare = alt.hconcat(hist_humans, hist_avs)
st.write(human_av_compare)

st.write("Interestingly enough, it appears that people feel more safe overall sharing the road with AVs than with human drivers. What are your theories as to why this is?")

st.markdown("This project was created by Healy Dwyer and Jacqueline Liao for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
