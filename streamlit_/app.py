import sys; sys.path.insert(0, '.')  # noqa
import time

import streamlit as st

from streamlit_.api import get_or_load_api

TEXT_SIZE = 80

with st.sidebar:
    config = st.file_uploader('Engine', type=['yaml', 'yml'])
    k = st.number_input('Top-k', value=5)
api = get_or_load_api(config)
if api is None:
    st.stop()

st.header('tinysearch🚀')

query = st.text_input('Query')
query = query.strip()
if not query:
    st.stop()

with st.spinner('Searching...'):
    start = time.perf_counter()
    scores = api.search(query, k=k)
    runtime = time.perf_counter() - start
    runtime = round(runtime, 2)

scores = [s for s in scores if s.score > 0]
for i, score in enumerate(scores):
    doc = api.get_document_by_id(score.id)
    text = doc.text
    text_too_long = len(text) > TEXT_SIZE
    text = text[:TEXT_SIZE]
    text = text + '...' if text_too_long else text
    st.code(f'{i+1}. {repr(text)} [{score.score:.2f}]', language=None)
st.caption(f'time: {runtime:.4f} s.')
