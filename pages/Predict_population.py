import streamlit as st
from datetime import datetime
from app.configs import configs as cf
from app.logic.prediction import predict_population
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json


st.set_page_config(page_title='Прогноз численности начеления', layout='wide')
st.title('Прогноз численности населения')
st.info('### Здесь вы можете предсказать численность населения Республики Беларусь по различным субъектам.')


with open(cf.COUNTRY_SETTLEMENTS_PATH, encoding='utf-8') as file:
    country_settlements = json.load(file)


def change_district_select_options():
    if st.session_state.region_select is not None:
        st.session_state['district_select_options'] = \
            country_settlements['REGION_DISTRICTS'][st.session_state.region_select]
    else:
        st.session_state['district_select_options'] = []
    predict()


def predict():
    if st.session_state.district_select:
        subject = st.session_state.district_select
    elif st.session_state.region_select:
        subject = st.session_state.region_select
    else:
        subject = st.session_state.country_select
    years = list(range(datetime.now().year + 1, datetime.now().year + st.session_state.year_slider + 1))
    predicted_values = predict_population(subject, years)
    st.session_state.prediction_parameters = {
        'subject': subject,
        'years': years,
        'predicted_values': predicted_values
    }
    df = pd.DataFrame({'year': years,
                       'predicted_values': predicted_values
                       })
    placeholder.empty()
    with placeholder.container():
        st.write(f'## Прогноз населения для {subject}')
        st.dataframe(df, column_config={'year': 'Год', 'predicted_values': 'Прогнозируемое население'})
        with plt.style.context('ggplot'):
            fig = plt.figure(figsize=(10, 4))
            plt.xlabel('Год')
            plt.ylabel('Количество населения')
            plt.ticklabel_format(style='plain', axis='y')
            sns.lineplot(df, x='year', y='predicted_values', markers=True)
        st.pyplot(fig)


option_columns = st.columns(3)
with option_columns[0]:
    country_select = st.selectbox(
        key='country_select',
        label='Страна',
        placeholder='Выберите страну...',
        options=country_settlements['COUNTRY_REGIONS'].keys(),
        index=0,
        on_change=predict
    )
    year_slider = st.slider(
        key='year_slider',
        min_value=cf.MIN_PREDICTION_YEARS,
        max_value=cf.MAX_PREDICTION_YEARS,
        value=int((cf.MIN_PREDICTION_YEARS + cf.MAX_PREDICTION_YEARS) / 2),
        label='Количество прогнозируемых лет',
        step=1
    )
with option_columns[1]:
    region_select = st.selectbox(
        key='region_select',
        label='Область',
        placeholder='Выберите область...',
        options=list(*country_settlements['COUNTRY_REGIONS'].values()),
        index=None,
        on_change=change_district_select_options
    )

with option_columns[2]:
    district_select = st.selectbox(
        key='district_select',
        label='Район',
        placeholder='Выберите район...',
        options=st.session_state.get('district_select_options', list()),
        index=None,
        on_change=predict
    )
placeholder = st.empty()
st.session_state.chart_container = placeholder

# Make prediction on page load
predict()
