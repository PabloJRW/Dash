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
yt_top = pd.read_csv('top_200_youtubers.csv')

# Dash App
# ==============================================================================
app = dash.Dash()


app.layout = html.Div(children=[

    # Header -----------------------------------------------------------
    html.Div(children=[
        html.H1("YouTube", 
            style={'font-style':'Bold','color':'#282828', 'margin':'0px', 'padding':'1.5% 0% 0% 1.5%'}),
        html.H2("Top 200 Youtubers", 
            style={'color':'black', 'font-size':'81%','margin':'0%', 'padding':'0% 0% 1% 1.5%'}),
    ], style={'width':'100vw', 'height':'9%','margin':'0% 0% 0.6% 0%','border':'.5px solid gray','background':'#FF0000','border-radius':'12px'}),


    html.Div(children=[
        # Dropdown - Selección de región -----------------------------------
        html.Div(children=[
            html.Div(children=[
                html.H2("Country", style={'margin':'0% 0% 0% 6%', 'padding':'0%', 'color':'black'}),
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
            'border-radius':'6px','background':'#FF0000','margin':'12px 0px 0px 12px'})
        ]),
    ], style={'width':'20%', 'height':'1080px','float':'left', 'background':'white'}),


    # 1ra fila - Div de los gráficos - -------------------------------------
    # ================================================
    html.Div(children=[

        # Gráfico de ventas por subcategorías
        html.Div(children=[
            dcc.Graph(id='mvcategory')
            ],style={'width':'620px','height':'320px','background':'white','padding':'1%','border':'1px solid gray',
            'border-radius':'12px','margin':'6px 24px 24px 24px'}),

        # Gráfico de ventas por región
        html.Div(children=[
            dcc.Graph(id='maintopics')
            ], style={'width':'620px','height':'320px','background':'white','padding':'1%','margin':'6px 24px 0px 24px','border':'1px solid gray',
                'border-radius':'12px'})

    # 1ra fila - cierre del div de los gráficos
    ], style={'display':'flex'}),
    

    # 2da fila - Div de los gráficos 
    # =========================================================
    html.Div(children=[

        # Line Plot: Order Date
        html.Div(children=[
            dcc.Graph(id="topfollowers")
        ], style={'width':'620px','height':'320px','background':'white','padding':'0','margin':'6px 24px 0px 24px','border':'1px solid gray',
            'border-radius':'12px'})

        # Plot: 


    # 2da fila: cierre del div
    ], style={'display':'flex'}),

# Div Principal - Layout Cierre
], style={'width':'100%','background':'#f4f4ec'})


@app.callback(
    Output(component_id='mvcategory', component_property='figure'),
    Output(component_id='maintopics', component_property='figure'),
    Output(component_id='topfollowers', component_property='figure'),
    Input(component_id='region_dd', component_property='value')
)
def updatePlots(region):
    # Ensure the DataFrame is not overwritten
    data = yt_top.copy(deep=True)
    # Create a conditional to filter the DataFrame if the input exists
    if region:
        data = data[data['Region']==region]
    
     # plot - ventas por categorias
    mv_category = yt_top.value_counts('Main Video Category')
    mv_category_fig = px.bar(mv_category, title="Top Categories", width=600, height=300)
    mv_category_fig.update_traces(marker_color='#FF0000')
    mv_category_fig.update_layout(xaxis_title=None,yaxis_title='Ventas',showlegend=False)
    
    # plot - ventas por subcategorias
    main_topics = yt_top.value_counts('Main topic')
    main_topics_fig = px.bar(main_topics, title="Top Topics", width=600, height=300)
    main_topics_fig.update_traces(marker_color='#FF0000')
    main_topics_fig.update_layout(xaxis_title=None,yaxis_title='Ventas',showlegend=False)
    
    #lineplot - order date
    top_followers_fig = px.bar(yt_top, x="Channel Name", y="followers")
    top_followers_fig.update_traces(marker_color='#FF0000')
    top_followers_fig.update_layout(xaxis_title=None,yaxis_title='Ventas',showlegend=False)
    
    return mv_category_fig, main_topics_fig, top_followers_fig


if __name__ == '__main__':
    app.run_server(debug=True, 
                   host=os.getenv('IP', '0.0.0.0'), 
                   port=int(os.getenv('PORT', 4444)))