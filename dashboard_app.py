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
    color=sales_by_subcategory.index, title="Ventas por Subcategoría", text_auto='.3s',width=600,height=300)
sales_by_subcategory_plot.update_traces(marker_color='#fff700')
sales_by_subcategory_plot.update_layout(
    xaxis_title=None,
    yaxis_title='Ventas',
    showlegend=False)
sales_by_subcategory_plot.update_xaxes(tickangle=90)

# Sales by region plot
sales_by_region_plot = px.bar(data_frame=sales_by_region,
    color=sales_by_region.index, title="Ventas por Región",text_auto='.3s',width=600,height=300)
sales_by_region_plot.update_traces(marker_color='#fff700')
sales_by_region_plot.update_layout(
    xaxis_title=None,
    yaxis_title='Ventas',
    showlegend=False)


# Dash App
# ==============================================================================
app = dash.Dash()


app.layout = html.Div(children=[

    # Header -----------------------------------------------------------
    html.Div(children=[
        html.H1("SMART BUY", style={'font-style':'Bold','color':'black', 'margin':'0px', 'padding':'1.5% 0% 0% 1.5%'}),
        html.H2("Sales Report", style={'color':'black', 'font-size':'15px','margin':'0%', 'padding':'0% 0% 1% 1.5%'}),
    ], style={'margin':'0px 0px 5px 0px','background':' #fff700','border-radius':'12px'}),

    # Dropdown - Selección de región -----------------------------------
    html.Div(children=[
        html.Div(children=[
            html.H2("Región", style={'margin':'0% 0px 0px 3px', 'padding':'0%', 'color':'black'}),
            dcc.Dropdown(id='region_dd',
                options=[
                    {'label':'North','value':'Norte'},
                    {'label':'South','value':'Sur'},
                    {'label':'East', 'value':'Este'},
                    {'label':'West', 'value':'Oeste'},
                    {'label':'Central', 'value':'Central'}],
                style={'padding':'0px','width':'200px', 'margin':'0px 0px 0px 3px', 'display':'inline-block'})],
        style={'width':'210px', 'height':'60px', 'border':'2px solid black', 'padding':'0px 9px 9px 3px',
        'border-radius':'6px','background':'#fff700','margin':'0px'})
    ]),
    
    # Div de los gráficos ----------------------------------------------
    html.Div(children=[
        # Gráfico de ventas por subcategorías
        html.Div(children=[
            #html.Br(),
            #html.H3('Ventas por Sub-Categoría', style={
          #      'color':'black','background':'#fff700','margin':'0px', 
          #      'border-radius':'6px', 'padding':'0px 0px 0px 30px'}),
            dcc.Graph(
                id='sales_by_subcategory_fig',
                figure=sales_by_subcategory_plot)
            ],style={'width':'600px','height':'300px','background':'white','padding':'0px','border':'2px solid black',
            'border-radius':'12px','margin':'6px 24px 24px 24px'}),

        # Gráfico de ventas por región
        html.Div(children=[
            #html.Br(),
            #html.H3('Ventas por Región', style={ 
            #    'color':'black','background':'#fff700','margin':'0px',
            #    'border-radius':'6px','padding':'0px 0px 0px 30px'}),
            dcc.Graph(
                id='sales_by_region_fig',
                figure=sales_by_region_plot)
            ], style={'width':'600px','height':'300px','background':'white','padding':'0px','margin':'6px 24px 0px 24px','border':'2px solid black','border-radius':'12px'})
    #
    # cierre del div de los gráficos
    ], style={'display':'flex'})
    
# Cierre del div principal
], style={'background':'#f4f4ec'})


@app.callback(
    Output(component_id='sales_by_subcategory_figg', component_property='figure'),
    Input(component_id='region_dd', component_property='value')
)

@app.callback()
def update_salesSubcategoryPlot(input_region=None):
    #Set a default value
    region_filter = input_region
    # Ensure the DataFrame is not overwritten
    data_df = sales_by_subcategory.copy(deep=True)
    # Create a conditional to filter the DataFrame if the input exists
    if region_filter:
        data_df = data_df[data_df['Region']==region_filter]
    
    sales_by_subcategory_figg = px.bar(data_frame=data_df,
    color=sales_by_subcategory.index)
    
    return sales_by_subcategory_figg


if __name__ == '__main__':
    app.run_server(debug=True, 
                   host=os.getenv('IP', '0.0.0.0'), 
                   port=int(os.getenv('PORT', 4444)))