import sys; sys.path.insert(0, '.')  # noqa
import time

import streamlit as st

from streamlit_.api import load_api_maybe

TEXT_SIZE = 80

with st.sidebar:
    config = st.file_uploader('Engine', type=['yaml', 'yml'])
    k = st.number_input('Top-k', value=5)
api = load_api_maybe(config)
if api is None:
    st.stop()

st.header('tinysearch🚀')

query = st.text_input('Query')
query = query.strip()
if not query:
    st.stop()

with st.spinner('Searching...'):
    start = time.perf_counter()
    scores = api.engine.search(query, k=k)
    runtime = time.perf_counter() - start
    runtime = round(runtime, 2)

scores = [s for s in scores if s.score > 0]
for i, score in enumerate(scores):
    text = api.corpus[score.id].text
    text_too_long = len(text) > TEXT_SIZE
    text = text[:TEXT_SIZE]
    text = text + '...' if text_too_long else text
    st.write(f'`{i+1}. {repr(text)} [{score.score:.2f}]`')
st.caption(f'time: {runtime:.4f} s.')
