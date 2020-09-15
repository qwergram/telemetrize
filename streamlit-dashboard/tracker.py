from datetime import datetime

import streamlit as st
import pandas as pd

def load_data():
    return pd.read_csv("telemetry.csv")    

def main(data):
    st.sidebar.title("Telemetry Data Output")
    st.sidebar.write("_built by @qwergram_")

    python_versions = data['pyver'].unique()
    listed_python_versions = "\n".join(
        f"    {'    ' * bool(i)}- {v}" for i, v in enumerate(python_versions)
    )

    st.sidebar.write(f"""
    ### Data Overview

    - {len(data)} datapoints recorded
    - {data['telemetryid'].nunique()} unique events recorded
    - {data['runid'].nunique()} unique runs recorded
    - {len(python_versions)} python versions recorded
    {listed_python_versions}
    - {data['executable'].nunique()} unique executables recorded
    - {data['user'].nunique()} unique users recorded
    - {data['host'].nunique()} unique hosts recorded
    - {data['error'].nunique() - 1} unique errors recorded
    - {data['codever'].nunique() - ('unknown' in data['codever'])} versions of code recorded
    - Data ranges from
        - From {datetime.fromtimestamp(data['time'].min())}
        - To {datetime.fromtimestamp(data['time'].max())}
        - Ranging {datetime.fromtimestamp(data['time'].max()) - datetime.fromtimestamp(data['time'].min())}
    """)

def home(data):
    st.write("""
    # Telemetry Library Analysis

    **Motivation**: The original concept of this library was written to better 
    understand the inner workings of open source libraries, such as django.
    This dashboard was then created as an analysis tool for internal nvidia 
    tools.

    This dashboard requires the `write_to_csv` operation to be set.

    Open an issue for any other questions. Below is an FAQ.

    # How do I add pages?

    Use the following template:
    ```py
    import streamlit as st
    import pandas as pd

    def main(data):
        pass

    if __name__ == "__main__":
        main(pd.read_csv('some_file_path.csv'))

    ```
    and then update the `PAGES` constant in `tracker.py` near the end.
    """)

if __name__ == "__main__":
    import summary
    import rawdisplay
    import arguments
    import recent

    PAGES = {
        'Home': home,
        'Data Summary': summary.main,
        'Parameter Analysis': arguments.main,
        'Run Reports': recent.main,


        'Raw Data': rawdisplay.main,
    }

    DATA = pd.read_csv('telemetry.csv')

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection](DATA)
    main(DATA)