
import streamlit as st 
import numpy as np 
import pandas as pd 
import os 
import plotly.express as px
from PIL import Image
from streamlit_echarts import st_echarts
import json 



######################################### title and logo ##########################################

st.set_page_config(layout="wide")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


image = Image.open('Logo-Amazon.jpg')

col1, col2 = st.columns([0.1,0.9])

with col1: 
    st.image(image, width=200)

###################      title setings         ###########################################################

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">dashboard interactivo de ventas de Amazon</h1></center>"""

with col2:
    st.markdown(html_title, unsafe_allow_html=True)
    
#### read the data file  and font 

amazon_dta = pd.read_excel('Amazon.xlsx')
fuente  = 'Gravitas Pro'

##############    resumen of the profit, sales and sales      ########################################### 


resumen = amazon_dta.groupby('Category').agg({'Profit': 'sum', 'Sales': 'sum' , 'Quantity':'sum'})


###################### products by categorys sales #####################################################


products = amazon_dta.groupby(['Category', 'Product Name']).agg({'Profit': 'sum', 'Sales': 'sum' , 'Quantity':'sum'})

products.reset_index(inplace=True)


###########################       time series      ############################################################

time_series = amazon_dta.groupby('Order Date').agg({'Profit': 'sum', 'Sales': 'sum' , 'Quantity':'sum'})
pd.to_datetime(time_series.index)



###########################         regions         #################################################################

amazon_dta["Geography"] = amazon_dta["Geography"].str.split(",").str[-1]
countrys = amazon_dta.groupby('Geography').agg({'Sales': 'sum'})

################################### waterfall dta ######################################################################


time_frequency = amazon_dta.copy() 
time_frequency['year'] = amazon_dta['Order Date'].dt.year
time_frequency['quarter'] = amazon_dta['Order Date'].dt.quarter
waterfall_dta = time_frequency.groupby(['year', 'quarter']).agg({'Profit':'sum'})
waterfall_dta.reset_index(inplace=True)



waterfall_dta['diference']= waterfall_dta['Profit'].diff()
waterfall_dta.diference[0] = waterfall_dta.Profit[0]

map = {1:'q1',2:'q2',3:'q3',4:'q4'}

def aplly_map(number): 
    if number in map:
        return map[number]
    else: 
        return number
    
waterfall_dta['quarter'] = waterfall_dta['quarter'].apply(aplly_map)


###################################  js chart data  and chart #############################################################


option ={
    'tooltip': {'tiger': 
                'item'},
    'legend': {'top':'5%',
               'left':'center'},
    'series': [{'name': 'purchases',
                'type': 'pie',
                'radius':['40%', '70%'],
                'avoidLabelOverlap':'true',
                'label':{'show':'true', 
                         'position':'center'},

                'emphasis':{
                    'label':{'show':'true',            
                             'fontSize':'39',
                             'fontWeight':'bold'}
                },
                
                'labelLine':{'show':'false'},
                'itemStyle':{'borderColor':'#fff'},         
                'data': [
                    {'value':'809', 'name':'2 o menos'},
                    {'value':'433', 'name':'3 a 6'},
                    {'value':'30', 'name':'7 o mas'}
                    ]

    
}]
}



###############        Barplot for profit     ##################################################################


fig = px.bar(resumen, x=resumen.index, y='Profit')
fig.update_xaxes(tickfont=dict(family=fuente, size=14))
fig.update_yaxes(tickfont=dict(family=fuente, size=14))

fig.update_traces(marker_color='rgb(166,216,84)')

################       barplot for Sales         ###############################################################

fig2 = px.bar(resumen, x=resumen.index, y='Sales')
fig2.update_xaxes(tickfont=dict(family=fuente, size=14))
fig2.update_yaxes(tickfont=dict(family=fuente, size=14))

fig2.update_traces(marker_color='rgb(55,126,184)')

######################### Barplot for quantity #################################################################


fig3 = px.bar(resumen, x=resumen.index, y='Quantity',)
fig3.update_xaxes(tickfont=dict(family=fuente, size=14))
fig3.update_yaxes(tickfont=dict(family=fuente, size=14))

fig3.update_traces(marker_color='#FECB52')


###################################     map chart     #########################################################

fig4 = px.choropleth(
    locations=['AZ', 'CA', 'CO', 'ID', 'MT', 'NV', 'NM', 'OR', 'UT', 'WA','WY'], 
    locationmode="USA-states", 
    color=countrys['Sales'], 
    scope="usa", 
    labels={'locations':'regions', 'color':'Sales'},
    color_continuous_scale='aggrnyl')


##################################################        heatmap        #################################################


fig5 = px.treemap(products, path=[px.Constant("producto"), 'Category', 'Product Name'], values='Sales', color='Sales',
                 color_continuous_scale='aggrnyl')
fig5.update_layout(width=1400)


################################################ waterfall charts   #######################################################

import plotly.graph_objects as go

fig6 = go.Figure(go.Waterfall(
    x=[waterfall_dta['year'], waterfall_dta['quarter']],
    measure=['absolute', 'relative', 'relative', 'relative', 'relative', 'relative', 'relative',
             'relative', 'relative', 'relative', 'relative', 'relative', 'relative', 'relative','relative', 'relative'],
    y=waterfall_dta['diference'],

    decreasing={"marker": {"color": "Maroon", "line": {"color": "red", "width": 2}}},
    increasing={"marker": {"color": "Teal"}},
    totals={"marker": {"color": "deep sky blue", "line": {"color": "blue", "width": 3}}}
))

fig6.update_layout(title="varianza de la utilidad", waterfallgap=0.3, width=1350, height=500)



###################################### waterfall javascript chart ########################################################

option2 = {
    "title": {"text": "benefio acumulado grafica de cascada"},
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"},
        "formatter":  "{b}<br/>{a}: {c}"         #####solution for the problem with js chats 
    },
    "legend": {"data": ['up', 'low']},
    "grid": {"left": '3%', "right": '4%', "bottom": '3%', "containLabel": True},
    "xAxis": {
        "type": 'category',
        "data": ['2011 Q1', '2011 Q2', '2011 Q3', '2011 Q4', 
                 '2012 Q1', '2012 Q2', '2012 Q3', '2012 Q4', 
                 '2013 Q1', '2013 Q2', '2013 Q3', '2013 Q4', 
                 '2014 Q1', '2014 Q2', '2014 Q3', '2014 Q4']
    },
    "yAxis": {"type": 'value'},
    "series": [
        {
            "name": 'Placeholder',
            "type": 'bar',
            "stack": 'Total',
            "silent": 'True',
            "itemStyle": {"borderColor": 'transparent', "color": 'transparent'},
            "emphasis": {"itemStyle": {"borderColor": 'transparent', "color": 'transparent'}},
            "data": [0, 1784.0288, 4274.8337, 6423.7188, 5277.8446, 4008.2922, 3714.4375, 3714.4375, 
                     2242.8620, 2242.8620, 4116.5159, 8504.7807, 9095.7788, 3559.6872, 3559.6872, 11032.2515,11032.2515]
        },
        {
            "name": 'up',
            "type": 'bar',
            "stack": 'Total',
            "label": {"show": 'True', "position": 'top'},
            "itemStyle": {"color": 'green'},
            "data": [1784.0288, 2490.8049, 3308.2762, '-', '-', '-', '-', 3777.1829, '-', 
                     1873.6539, 4388.2648, 590.9981, 4959.4798, '-', 11693.2515, '-']
        },
        {
            "name": 'low',
            "type": 'bar',
            "stack": 'Total',
            "label": {"show": 'True', "position": 'bottom'},
            "itemStyle":{"color":'red'},
            "data": ['-', '-', '-', 1159.3911, 1145.8742, 1269.5524, 293.8547, '-', 
                     5248.7584, '-', '-', '-', '-', 10495.5714, '-', 4220.1976]
        }
    ]
}




##########################           tabs and cols  for dashboard          ########################################################

col3, col4 = st.columns([0.4, 0.35])



with col3:

    tab1, tab2, tab3 = st.tabs(['Utilidad', 'Ventas', 'Cantidad'])

    with tab1:
        st.header("utilidad")
        st.plotly_chart(fig)

    with tab2:
        st.header("Ventas")
        st.plotly_chart(fig2)

    with tab3:
        st.header("Cantidad")
        st.plotly_chart(fig3)

with col4:

    tab4, tab5 = st.tabs(['frecuencia', 'Estados'])

    with tab4: 
        st.header("productos por compra") 
        st_echarts(option, width=500, height=500)   
        
    with tab5: 
        st.header("ventas por estado")
        st.plotly_chart(fig4)
        
############################        heatmap        #############################################################################

st.header('ingesos por producto y categoria')
st.plotly_chart(fig5)

############################        Time series chart                ###########################################################

st.header('Series de tiempo')

col5, col6 = st.columns([0.1, 0.8])

with col5: 
    time_series_options = time_series.columns.to_list()
    selected_series = st.radio("select",
             key='line_visibility',
             options=time_series_options)

with col6:
    filtered_time_series = time_series[[selected_series]]
    st.line_chart(filtered_time_series, color='#ffaa00')

############################################## waterfall charts #######################################################

st.header("Utilidad a travez del tiempo analisis de varianza")

tab6, tab7 = st.tabs(['js grafica', 'plotly grafica'])

with tab6:
    st_echarts(options=option2,width=1350, height=500)

with tab7:
    st.plotly_chart(fig6)







