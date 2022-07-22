import os
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from turtle import color, title


# DATA
# ==============================================================================
data = pd.read_csv('supermart.csv')

# Data grouped by sub category
sales_by_subcategory = data.groupby('Sub Category')['Sales'].sum()
sales_by_subcategory.sort_values(ascending=False, inplace=True)

# Data grouped by region
sales_by_region = data.groupby('Region')['Sales'].sum()
sales_by_region.sort_values(ascending=False, inplace=True)


# Plots
# ==============================================================================
# Sales by subcategory plot
sales_by_subcategory_plot = px.bar(data_frame=sales_by_subcategory,
    color=sales_by_subcategory.index)
sales_by_subcategory_plot.update_layout(
    xaxis_title='Sub Categorías',
    yaxis_title='Ventas',
    showlegend=False)
sales_by_subcategory_plot.update_xaxes(tickangle=90)

# Sales by region plot
sales_by_region_plot = px.bar(data_frame=sales_by_region,
    color=sales_by_region.index)
sales_by_region_plot.update_layout(
    xaxis_title='Región',
    yaxis_title='Ventas',
    showlegend=False)


# Dash App
# ==============================================================================
app = dash.Dash()


app.layout = html.Div(children=[

    # Header
    html.Div(children=[
        html.H1("Retail Sales", style={'color':'white', 'margin':'0px', 'padding':'1.5% 0% 0% 1.5%'}),
        html.H2("Report", style={'color':'white', 'margin':'0%', 'padding':'0% 0% 1% 1.5%'}),
    ], style={'margin':'0% 0% .5% 0%','background':'#4e88f3'}),

    # Selección de región - dropdown
    html.Div(children=[
        html.Div(children=[
            html.H2("Región", style={'margin':'0%', 'padding':'0%', 'color':'#4e88f3'}),
            dcc.Dropdown(id='region_dd',
                options=[
                    {'label':'North','value':'Norte'},
                    {'label':'South','value':'Sur'},
                    {'label':'East', 'value':'Este'},
                    {'label':'West', 'value':'Oeste'},
                    {'label':'Central', 'value':'Central'}],
                style={'padding':'0px','width':'200px', 'margin':'0 auto', 'display':'inline-block'})],
                style={'width':'250px', 'height':'6 0px', 'display':'inline-block', 
           'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'})
    ]),
    
    # Div de los gráficos
    html.Div(children=[
        # Gráfico de ventas por subcategorías
        html.Div(children=[
            html.Br(),
            html.H3('Ventas por Sub-Categoría', 
                style={'color':'#4e88f3','border':'2px solid #4e88f3', 'width':'97%', 
                'margin':'0 auto', 'display':'inline-block'}),
            dcc.Graph(
                id='sales_by_subcategory_fig',
                figure=sales_by_subcategory_plot)
            ],style={'width':'49%'}),

        # Gráfico de ventas por región
        html.Div(children=[
            html.Br(),
            html.H3('Ventas por Región', 
            style={ 'color':'#4e88f3','border':'2px solid #4e88f3', 'width':'0 auto', 'margin':'0px'}),
            dcc.Graph(
                id='sales_by_region_fig',
                figure=sales_by_region_plot)
            ], style={'width':'49%'})

    ], style={'display':'flex'})
    

])


"""@app.callback(
    Output(component_id='sales_by_subcategory_fig', component_property='figure'),
    Input(component_id='region_dd', component_property='value')
)


def update_salesSubcategoryPlot(input_region):
    #Set a default value
    region_filter = 'North'
    # Ensure the DataFrame is not overwritten
    data_df = data.copy(deep=True)
    # Create a conditional to filter the DataFrame if the input exists
    if region_filter:
        region_filter = data[data['Region']==region_filter]
        data_df = data_df[data_df['Region']==region_filter]
    sales_by_subcategory_fig = px.bar(data_frame=sales_by_subcategory,
    color=sales_by_subcategory.index)
    sales_by_subcategory_fig.update_layout(
    xaxis_title='Sub Categorías',
    yaxis_title='Ventas',
    showlegend=False)
    sales_by_subcategory_fig.update_xaxes(tickangle=90)
    
    return sales_by_subcategory_fig
"""
if __name__ == '__main__':
    app.run_server(debug=True, 
                   host=os.getenv('IP', '0.0.0.0'), 
                   port=int(os.getenv('PORT', 4444)))