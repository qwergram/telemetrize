import streamlit as st
import pandas as pd

def main(data):
    st.write("# Parameter Analysis")

    for tid in data['telemetryid'].unique():
        tid_report(data, tid)

def tid_report(data, tid):
    st.write(f'## Telemetry ID: `{tid}`')
    events = data[data['telemetryid'] == tid]
    st.write(events[['args', 'kwargs', 'runtime', 'error', 'runid']])

if __name__ == "__main__":

    main()