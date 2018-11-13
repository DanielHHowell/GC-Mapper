import dash
import dash_html_components as html
import dash_core_components as dcc
import analysis
from dash.dependencies import Input, Output


df = analysis.import_data()

app = dash.Dash('drug-discovery')
server = app.server

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium"]

for css in external_css:
    app.css.append_css({"external_url": css})



BACKGROUND = 'rgb(252, 252, 252)'



def scatter_plot_3d(
        x=df[1]['X'],
        y=df[1]['Y'],
        z=df[1]['Phase'],
        color=df[1]['Color'],
        xlabel='X',
        ylabel='Y',
        zlabel='Phase',
        plot_type='scatter3d', ):

    def axis_template_3d(title, type='linear'):
        return dict(
            showbackground=True,
            backgroundcolor=BACKGROUND,
            gridcolor='rgb(225, 225, 225)',
            title=title,
            type=type,
            zerolinecolor='rgb(252, 252, 252)'
        )

    def axis_template_2d(title):
        return dict(
            xgap = 10, ygap = 10,
            backgroundcolor = BACKGROUND,
            gridcolor = 'rgb(100, 100, 100)',
            dtick = 2,
            title = title,
            zerolinecolor = 'rgb(0, 0, 0)',
            color = '#444'
        )

    data = [dict(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            line=dict(color='#444'),
            reversescale=True,
            sizeref=45,
            sizemode='diameter',
            opacity=0.7,
            color=color,
        ),
        text=df[1]['Name'],
        type=plot_type,
    )]

    layout = dict(
        font=dict(family='Raleway'),
        hovermode='closest',
        showlegend=False,
        scene=dict(
            xaxis=axis_template_3d(xlabel),
            yaxis=axis_template_3d(ylabel),
            zaxis=axis_template_3d(zlabel),
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=0.08, y=2.2, z=0.08)
            )
        )
    )

    if plot_type == 'scatter':
        layout['xaxis'] = axis_template_2d(xlabel)
        layout['yaxis'] = axis_template_2d(ylabel)
        layout['plot_bgcolor'] = BACKGROUND
        layout['paper_bgcolor'] = BACKGROUND
        del layout['scene']
        del data[0]['z']

    # if trial != '1':
    #     layout['xaxis'] = axis_template_2d(xlabel)
    #     layout['yaxis'] = axis_template_2d(ylabel)
    #     layout['plot_bgcolor'] = BACKGROUND
    #     layout['paper_bgcolor'] = BACKGROUND
    #     del layout['scene']
    #     del data[0]['z']

    return dict(data=data, layout=layout)


FIGURE = scatter_plot_3d()

app.layout = html.Div([

    # Main body
    html.Div([

        html.Div([
            html.Div([

                html.P(
                    'Click and drag to rotate the graph in 3D, scroll to zoom.'),
            ], style={'text-align': 'center'}),

        ], className='jumbotron'),
    ], className='container'),

    # Graph
    html.Div([

        html.Div([

            # dcc.Dropdown(
            #     id='trial-input',
            #     options=[{'label': str(i+1), 'value': str(i+1)}
            #              for i in range(8)],
            #     value='1',
            #     multi=False
            # ),

            dcc.RadioItems(
                id = 'charts_radio',
                options=[
                    dict( label='3D Scatter', value='scatter3d' ),
                    dict( label='2D Scatter', value='scatter' ),
                ],
                labelStyle = dict(display='inline'),
                value='scatter3d'
            ),

            dcc.Graph(id='clickable-graph',
                      style=dict(height='1250px',width='1400px'),
                      hoverData=dict( points=[dict(pointNumber=0)] ),
                      figure=FIGURE ),

        ], className='nine columns', style=dict(textAlign='center')),

    ], className='row', style={'margin-left': '25%'}),
])

@app.callback(
    Output('clickable-graph', 'figure'),
    [Input('charts_radio', 'value'),
     #Input('trial-input', 'value')
    ])

def highlight_molecule(plot_type):
    return scatter_plot_3d(plot_type=plot_type)

if __name__ == '__main__':
    app.run_server()