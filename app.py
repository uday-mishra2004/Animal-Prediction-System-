"""Streamlit interface. Training stays in the command-line pipeline."""
import json
import pandas as pd
import joblib
import streamlit as st
from src.core import ROOT, validate, predict
st.set_page_config(page_title='Wildlife Insights',page_icon='🌿',layout='wide')
st.title('Wildlife Insights & Detection Demo')
st.caption('Survey analytics • reproducible machine learning • transparent limitations')
metrics_path=ROOT/'reports/metrics.json'
if not metrics_path.exists():
    st.info('Run python -m src.train in the project terminal first.');st.stop()
meta=json.loads(metrics_path.read_text())
if meta['source']=='synthetic_demo':
    st.warning('SYNTHETIC DEMO: records, locations and outcomes are invented. Metrics demonstrate the pipeline, not ecological validity.')
else:
    st.warning('User-supplied data: provenance and label validity require independent review.')
@st.cache_resource
def load_model(modified):
    return joblib.load(ROOT/'models/pipeline.joblib')
@st.cache_data
def load_data(path,modified):
    return validate(pd.read_csv(path))
data_path=ROOT/('data/raw/synthetic_surveys.csv' if meta['source']=='synthetic_demo' else 'data/processed_surveys.csv')
try:
    df=load_data(str(data_path),data_path.stat().st_mtime)
except (OSError,ValueError) as exc:
    st.error(str(exc));st.stop()
page=st.sidebar.radio('Explore',['Overview','Species analytics','Geography','Prediction','Model performance','Methodology'])
chosen=st.sidebar.multiselect('Species',sorted(df.species.unique()),default=sorted(df.species.unique()))
filtered=df[df.species.isin(chosen)]
if page=='Overview':
    a,b,c=st.columns(3);a.metric('Survey records',len(filtered));b.metric('Represented species',filtered.species.nunique());c.metric('Survey sites',filtered.site_id.nunique())
    if len(filtered):st.caption(f'Date coverage: {filtered.survey_date.min().date()} to {filtered.survey_date.max().date()}')
    st.subheader('Recorded survey outcomes');st.bar_chart(filtered.detected.value_counts().rename(index={0:'Not detected',1:'Detected'}))
    st.dataframe(filtered.head(100),hide_index=True)
elif page=='Species analytics':
    st.subheader('Survey counts by species');st.bar_chart(filtered.species.value_counts())
    st.subheader('Monthly survey records');st.line_chart(filtered.groupby('month').size())
    st.subheader('Detection rate within recorded surveys');st.bar_chart(filtered.groupby('species').detected.mean())
    st.caption('Counts and rates reflect sampling and survey effort; they are not population abundance.')
elif page=='Geography':
    if {'latitude','longitude'}<=set(filtered.columns):st.map(filtered[['latitude','longitude']])
    else:st.info('No valid coordinate fields available.')
elif page=='Prediction':
    st.write('Estimate recorded detection for a specified species and survey. This does not estimate true presence or absence.')
    with st.form('predict'):
        values={c:st.selectbox(c.replace('_',' ').title(),meta['categories'][c]) for c in ['species','habitat']}
        for c,(lo,hi) in meta['ranges'].items():
            values[c]=st.number_input(c.replace('_',' ').title(),min_value=float(lo),max_value=float(hi),value=float((lo+hi)/2))
        go=st.form_submit_button('Estimate detection')
    if go:
        try:
            pipe=load_model((ROOT/'models/pipeline.joblib').stat().st_mtime)
            probability=predict(pipe,meta,values)
            st.metric('Model score for recorded detection',f'{probability:.1%}')
            st.caption('Uncalibrated model output; not validated for conservation decisions.')
        except (OSError,ValueError) as exc:st.error(str(exc))
elif page=='Model performance':
    st.write('Selected model:',meta['selected_model']);st.caption(meta['split'])
    st.dataframe(pd.DataFrame(meta['comparison']).T)
    st.json({k:v for k,v in meta['test'].items() if k!='classification_report'})
    st.dataframe(pd.DataFrame(meta['test']['classification_report']).T)
    st.caption('Confusion matrix order: [not detected, detected]. Selection used training-site cross-validation; holdout used only for final evaluation.')
else:
    st.markdown((ROOT/'docs/model_card.md').read_text())
    st.caption('MySQL is optional. The dashboard reads validated CSV files and saved model outputs, so it runs without a database server.')
