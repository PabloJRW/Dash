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
yt_top = pd.read_csv('yt_top.csv')

# Dash App
# ==============================================================================
app = dash.Dash()

 
app.layout = html.Div(children=[

    # Header -----------------------------------------------------------
    html.Div(children=[
        html.H1("YouTube", 
            style={'font-size':'42px','font-style':'Youtube Sans Bold','color':'black','margin':'0px', 'padding':'1.5% 0% 0% 1.5%'}),
        html.H2("Top 200 Youtubers", 
            style={'color':'white', 'font-size':'81%','margin':'0%', 'padding':'0% 0% 1% 1.5%'}),
    ], style={'width':'100vw', 'height':'9%','margin':'0% 0% 0.6% 0%','border':'.5px solid gray','background':'#FF0000','border-radius':'12px'}),


    html.Div(children=[
        # Dropdown - Selección de país -----------------------------------
        html.Div(children=[
            html.Div(children=[
                html.H2("Country", style={'margin':'0% 0% 0% 6%', 'padding':'0%', 'color':'white'}),
                dcc.Dropdown(yt_top.Country.unique(), id='country_dd')
            ],
            style={'width':'210px', 'height':'60px', 'border':'1px solid gray', 'padding':'0px 9px 9px 3px',
            'border-radius':'6px','background':'#FF0000','margin':'12px 0px 0px 12px'})
        ]),

        # Dropdown - Selección de país -----------------------------------
        html.Div(children=[
            html.Div(children=[
                html.H2("Category", style={'margin':'0% 0% 0% 6%', 'padding':'0%', 'color':'white'}),
                dcc.Dropdown(yt_top.Category.unique(), id='category_dd')
            ],
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
            'border-radius':'12px','margin':'6px 12px 24px 24px'}),

        # Gráfico de ventas por región
        html.Div(children=[
            dcc.Graph(id='maintopics')
            ], style={'width':'620px','height':'320px','background':'white','padding':'1%','margin':'6px 24px 0px 12px','border':'1px solid gray',
                'border-radius':'12px'})

    # 1ra fila - cierre del div de los gráficos
    ], style={'display':'flex'}),
    

    # 2da fila - Div de los gráficos 
    # =========================================================
    html.Div(children=[

        # Line Plot: Order Date
        html.Div(children=[
            dcc.Graph(id="topfollowers")
        ], style={'width':'620px','height':'320px','background':'white','padding':'1%','margin':'6px 12px 0px 24px','border':'1px solid gray',
            'border-radius':'12px'}),

        # Plot: 
        # Line Plot: Order Date
        html.Div(children=[
            dcc.Graph(id="likes")
        ], style={'width':'620px','height':'320px','background':'white','padding':'1%','margin':'6px 24px 0px 12px','border':'1px solid gray',
            'border-radius':'12px'})

    # 2da fila: cierre del div
    ], style={'display':'flex'}),

# Div Principal - Layout Cierre
], style={'width':'100%','background':'#f4f4ec'})


@app.callback(
    Output(component_id='mvcategory', component_property='figure'),
    Output(component_id='maintopics', component_property='figure'),
    Output(component_id='topfollowers', component_property='figure'),
    Output(component_id='likes', component_property='figure'),
    Input(component_id='country_dd', component_property='value'),
    Input(component_id='category_dd', component_property='value')
)
def updatePlots(country=None, category=None):
    # Ensure the DataFrame is not overwritten
    data = yt_top.copy(deep=True)

    # Create a conditional to filter the DataFrame if the input exists
    if country and category:
        data = data[(data['Country']==country) & (data['Category']==category)]
    elif country:
        data = data[data['Country']==country] 
    elif category:
        data = data[data['Category']==category]
 
     # plot - ventas por categorias
    mv_category = data['Main Video Category'].value_counts().head(5)
    mv_category_fig = px.bar(mv_category, title="Top Categories", width=600, height=300)
    mv_category_fig.update_traces(marker_color='#FF0000')
    mv_category_fig.update_layout(xaxis_title=None,yaxis_title='Number of Channels',showlegend=False)
    
    # plot - ventas por subcategorias
    main_topics = data['Main topic'].value_counts().head(5)
    main_topics_fig = px.bar(main_topics, title="Top Topics", width=600, height=300)
    main_topics_fig.update_traces(marker_color='#FF0000')
    main_topics_fig.update_layout(xaxis_title=None,yaxis_title='number of Channels',showlegend=False)
    
    #lineplot - order date
    top_followers = data[['Channel Name','followers']].sort_values('followers', ascending=False).head()
    top_followers_fig = px.bar(top_followers, x="Channel Name", y="followers", title="Top Followers",
        text_auto='.2s', width=600, height=300)
    top_followers_fig.update_traces(marker_color='#FF0000')
    top_followers_fig.update_layout(xaxis_title=None,yaxis_title='Number of Followers',showlegend=False)
    
    #
    top_likes = data[['Channel Name','Likes']].sort_values('Likes', ascending=False).head(5)
    top_likes_fig = px.bar(top_likes, x="Channel Name", y="Likes", width=600, height=300)
    top_likes_fig.update_traces(marker_color='#FF0000')
    top_likes_fig.update_layout(xaxis_title=None,yaxis_title='Number of Likes',showlegend=False)
    
    return mv_category_fig, main_topics_fig, top_followers_fig, top_likes_fig


if __name__ == '__main__':
    app.run_server(debug=True, 
                   host=os.getenv('IP', '0.0.0.0'), 
                   port=int(os.getenv('PORT', 4444)))


                   