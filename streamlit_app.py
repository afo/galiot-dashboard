import altair as alt
import streamlit as st

import pandas as pd
import numpy as np

from SessionState import get
st.set_page_config(layout="wide")
session_state = get(password='')


def main():

    c1, c2 = st.beta_columns(2)
    with c2:
        st.title('Data Analysis')
    with c1:
        st.markdown(
            f"""
        <div class="container">
            <img class="logo-img" width=300px src="https://uploads-ssl.webflow.com/601427c1623985e99b150892/60452e5cf669e57bed3bf771_lgoogbalck.svg">
        </div>
        """,
            unsafe_allow_html=True
        )

    st.markdown('## Hotspots in Sweden')  # see *

    st.markdown('All hotspots in Sweden')

    df = pd.read_csv('swe_hotspots-april2-2021.csv')
    df[['timestamp_added', 'owner', 'name', 'short_street',
        'short_state']]  # <-- Draw the dataframe

    st.markdown('## Top 10 owners in Sweden')

    col1, col2 = st.beta_columns(2)

    df2 = pd.read_csv('reward_per_owner.csv', index_col=0)

    st.write(df2)

    numbers2 = list((df['owner'][::-1] ==
                     '14Rqw67Er4T4mDitRR5hkvDbefXUhVQGiaVV4yzgSF3sVtu6PfU').cumsum())

    numbers = list(range(1, len(df['timestamp_added'])+1))

    df3 = pd.DataFrame({'Total': numbers, 'Galiot': numbers2}, index=pd.to_datetime(
        list(df['timestamp_added'][::-1])))

    df4 = df3['Galiot']/df3['Total']
    df4 = pd.DataFrame(df4, columns=['Galiot Percentage'])
    df4 = df4.round(3)*100

    st.markdown('## Galiot Percentage of Hotspots in Sweden over Time')
    st.altair_chart(alt.Chart(pd.melt(df4.reset_index(), id_vars=["index"]), width=1600, height=350).mark_area(
        color="lightblue",
        interpolate='step-after',
        line=True
    ).encode(
        alt.X("index", title=""),
        alt.Y("value", title="", stack=None),
        alt.Color("variable", title="", type="nominal"),
        opacity={"value": 0.4},
        tooltip=["index", "value", "variable"]
    ).interactive()
    )
    st.markdown('## Galiot Hotspots vs Total HS in Sweden')
    st.altair_chart(
        alt.Chart(pd.melt(df3.reset_index(), id_vars=["index"]), width=1600, height=350).mark_area().encode(
            alt.X("index", title="", scale=alt.Scale(type="utc")),
            alt.Y("value", title="", scale=alt.Scale(type="utc"), stack=None),
            alt.Color("variable", title="", type="nominal"),
            opacity={"value": 0.8},
            tooltip=["index", "value", "variable"]
        ).interactive()
    )
    # st.area_chart(df3)

    #st.latex(r''' e^{i\pi} + 1 = 0 ''')


if session_state.password != 'helium':
    pwd = st.text_input(
        "Password for Internal Galiot Dashboard:", value="", type="password")
    session_state.password = pwd
    if session_state.password == 'helium':
        main()
    elif:
        st.error("the password you entered is incorrect")
else:
    main()
