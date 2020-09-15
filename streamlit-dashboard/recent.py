import streamlit as st
import pandas as pd

from datetime import datetime

def main(data):
    st.write("# Parameter Analysis")

    for rid in data['runid'].unique()[::-1]:
        rid_report(data, rid)

def rid_report(data, rid):
    events = data[data['runid'] == rid].sort_values('time')
    st.write(f'## Run ID: `{rid}` ({len(events)} events)')
    st.write(
        f"Started on {datetime.fromtimestamp(events['time'].min())} and "
        f"ended on {datetime.fromtimestamp(events['time'].max())}."
    )

    telemetryid_df = events.groupby('telemetryid')

    st.bar_chart(
        telemetryid_df[['eventid']].nunique()
    )

    st.write(events)

if __name__ == "__main__":
    main()