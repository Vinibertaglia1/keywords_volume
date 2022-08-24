from itertools import count
import pandas as pd 
import streamlit as st 
import scipy.stats as stats
import numpy as np

df = pd.read_csv('googleVolumeSearch.csv')

st.markdown('<h1 style = "border-radius: 50px; color: #FFFFFF;text-align:center;text-transform: uppercase; background:-webkit-linear-gradient(#1088ff,#0bd6d4);"> Keyword Analysis </h1>',unsafe_allow_html=True)
country = df['country'].unique().tolist()
country.insert(0,"")
countries = st.selectbox("Choose a country",country)
if countries != '':
    df_filtrado = df[df['country'] == countries]

    df_filtrado['absolute'] = df_filtrado['absolute'].fillna(0)
    z_scores = stats.zscore(df_filtrado['absolute'])
    df_filtrado['volume_zscore'] = z_scores
    q20, q50, q70, q95 = np.percentile(df_filtrado['volume_zscore'],[20,50,70,95])
    
    def get_percentile_by_value(value, q20 = q20, q50=q50,q70=q70, q95=q95):
        label = ''
        if value < q20:
            label = 'Very Low'
        elif (value >= q20) and (value < q50):
            label = 'Low'
        elif (value >= q50) and (value < q70):
            label = 'Medium'
        elif (value >= q70) and (value < q95):
            label = 'High'
        else:
            label = 'Very High'
        return label 

    df_filtrado['volume_label'] = df_filtrado['volume_zscore'].apply(get_percentile_by_value)
    textos =  df_filtrado['keyword'].unique().tolist()
    textos.insert(0,'')

    feature = st.selectbox("Choose a Feature", ['','Keywords Database','Enter your Keyword'])
    
    def get_percentage_of_total(value, df=df_filtrado):
        max =  df['volume_zscore'].max()
        calculate = (100 * value) / max
        round_percentage = np.abs(round(calculate,2))
        
        return round_percentage
    
    df_filtrado['volume_percentage'] = df_filtrado['volume_zscore'].apply(get_percentage_of_total)
    
    if feature == 'Keywords Database':
        saida = st.selectbox('Choose and press enter to add keywords',textos)
        df_text = df_filtrado[df_filtrado['keyword'] == saida]
        if df_text['absolute'].iloc[-1] == 0:
            df_text['volume_percentage'] = 0
        col1, col2, col3 = st.columns(3)
        if saida != "":
            with col1:
                st.markdown("<h1>  Volume </h1>", unsafe_allow_html=True)
                volume_absolute = df_text['absolute'].iloc[-1]
                st.markdown(f"<h3> {volume_absolute}</h3>",unsafe_allow_html=True)
            with col2:
                st.markdown("<h1>  Volume Percentage </h1>", unsafe_allow_html=True)
                volume_percentage = df_text['volume_percentage'].iloc[-1]
                
                st.markdown(f"<h3> {volume_percentage} % </h3>", unsafe_allow_html=True)

            with col3:
                st.markdown("<h1> Search Volume </h1>", unsafe_allow_html=True)
                volume_label = df_text['volume_label'].iloc[-1]
                st.markdown(f"<h3> {volume_label}</h3>", unsafe_allow_html=True)
    elif feature == 'Enter your Keyword':
        volume_input = st.number_input('Input the Volume from Tool')
        new_volume = df_filtrado[df_filtrado['absolute'] == int(volume_input)]
        col2, col3 = st.columns(2)
        with col2:
            st.markdown("<h1>  Volume </h1>", unsafe_allow_html=True)
            volume_absolute = volume_input
            st.markdown(f"<h3> {volume_input}</h3>",unsafe_allow_html=True)

        with col3:
            st.markdown("<h1> Search Volume </h1>", unsafe_allow_html=True)
            volume_label = new_volume['volume_label'].iloc[-1]
            st.markdown(f"<h3> {volume_label}</h3>", unsafe_allow_html=True)
            