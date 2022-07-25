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
data_df = pd.read_csv('supermart.csv')


# Dash App
# ==============================================================================
app = dash.Dash()


app.layout = html.Div(children=[

    # Header -----------------------------------------------------------
    html.Div(children=[
        html.H1("SMART BUY", 
            style={'font-style':'Bold','color':'black', 'margin':'0px', 'padding':'1.5% 0% 0% 1.5%'}),
        html.H2("Sales Report", 
            style={'color':'black', 'font-size':'81%','margin':'0%', 'padding':'0% 0% 1% 1.5%'}),
    ], style={'width':'100%', 'height':'9%','margin':'0% 0% 0.6% 0%','border':'.5px solid gray','background':' #fff700','border-radius':'12px'}),


    html.Div(children=[
        # Dropdown - Selección de región -----------------------------------
        html.Div(children=[
            html.Div(children=[
                html.H2("Región", style={'margin':'0% 0% 0% 6%', 'padding':'0%', 'color':'black'}),
                dcc.Dropdown(id='region_dd',
                    options=[
                        {'label':'Todas ', 'value':False},
                        {'label':'Norte','value':'North'},
                        {'label':'Sur','value':'South'},
                        {'label':'Este', 'value':'East'},
                        {'label':'Oeste', 'value':'West'},
                        {'label':'Central', 'value':'Central'}],
                    style={'padding':'0px','width':'200px', 'margin':'0px 0px 0px 3px', 'display':'inline-block'})],
            style={'width':'210px', 'height':'60px', 'border':'1px solid gray', 'padding':'0px 9px 9px 3px',
            'border-radius':'6px','background':'#fff700','margin':'12px 0px 0px 12px'})
        ]),
    ], style={'width':'20%', 'height':'1080px','float':'left', 'background':'white'}),

    # Div de los gráficos ----------------------------------------------
    html.Div(children=[
        # Gráfico de ventas por subcategorías
        html.Div(children=[
            dcc.Graph(id='sales_cat')
            ],style={'width':'620px','height':'320px','background':'white','padding':'1%','border':'1px solid gray',
            'border-radius':'12px','margin':'6px 24px 24px 24px'}),

        # Gráfico de ventas por región
        html.Div(children=[
            dcc.Graph(id='sales_sub')
            ], style={'width':'620px','height':'320px','background':'white','padding':'1%','margin':'6px 24px 0px 24px','border':'1px solid gray','border-radius':'12px'})
    
    # cierre del div de los gráficos
    ], style={'display':'flex'})
    
# Cierre del div principal
], style={'background':'#f4f4ec'})


@app.callback(
    Output(component_id='sales_cat', component_property='figure'),
    Output(component_id='sales_sub', component_property='figure'),
    Input(component_id='region_dd', component_property='value')
)
def updatePlots(region):
    # Ensure the DataFrame is not overwritten
    data = data_df.copy(deep=True)
    # Create a conditional to filter the DataFrame if the input exists
    if region:
        data = data[data['Region']==region]
    
     # plot - ventas por categorias
    cat_sales = data.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    cat_sales_fig = px.bar(data_frame=cat_sales, title="Ventas por Categorías",
                 text_auto='.3s', width=600, height=300)
    cat_sales_fig.update_traces(marker_color='#fff700')
    cat_sales_fig.update_layout(xaxis_title=None,yaxis_title='Ventas',showlegend=False)
    
    # plot - ventas por subcategorias
    sub_sales = data.groupby('Sub Category')['Sales'].sum().sort_values(ascending=False)
    sub_sales_fig = px.bar(data_frame=sub_sales, title="Ventas por Subcategorías",
                 text_auto='.3s', width=600, height=300)
    sub_sales_fig.update_traces(marker_color='#fff700')
    sub_sales_fig.update_layout(xaxis_title=None,yaxis_title='Ventas',showlegend=False)
    
    return cat_sales_fig, sub_sales_fig


if __name__ == '__main__':
    app.run_server(debug=True, 
                   host=os.getenv('IP', '0.0.0.0'), 
                   port=int(os.getenv('PORT', 4444)))