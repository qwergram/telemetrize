import streamlit as st

def main(data):
    st.write("""
    # Raw Data
    Below is the data available.
    """)
    st.write(data)

if __name__ == "__main__":
    main()