from datetime import datetime


import streamlit as st
import pandas as pd
import numpy as np

def main(data):
    st.write("# Data Summary")
    st.write("""
    ## Total Frequency by `telemetryid`
    Raw number of times a `telemetry` event was triggered
    """)

    telemetryid_df = data.groupby('telemetryid')

    st.bar_chart(
        telemetryid_df[['eventid']].nunique()
    )

    st.write("""
    ## Average `telemetryid` calls per Run
    How many times each telemetry event 
    """)
    st.bar_chart(
        telemetryid_df['eventid'].nunique() / telemetryid_df['runid'].nunique()
    )

    st.write("## Average Runtime by `telemetryid`")
    st.bar_chart(
        telemetryid_df['runtime'].mean()
    )

    st.write("## Timeline")
    splitbytid = st.checkbox("Split by telemetryid", value=True)

    begin = data['time'].min()
    end = data['time'].max()
    time = np.linspace(begin, end, 2000)

    timeline_df = pd.DataFrame({'time': time})

    for tid in data['telemetryid'].unique():
        timeline_df[tid] = 0
        events = data[data['telemetryid'] == tid][['time', 'runtime']]
        events['endtime'] = events['time'] + events['runtime']
        for _, event in events.iterrows():
            query = (timeline_df['time'] >= event['time']) & (timeline_df['time'] < event['endtime'])
            timeline_df.loc[query, tid] += 1

    if not splitbytid:
        timeline_df['events'] = timeline_df[data['telemetryid'].unique()].sum(axis=1)
        timeline_df.drop(data['telemetryid'].unique(), axis=1, inplace=True)

    timeline_df['time'] = timeline_df['time'].apply(lambda v: datetime.fromtimestamp(v))

    st.bar_chart(
        timeline_df.set_index('time', drop=True),
    )


if __name__ == "__main__":
    main()