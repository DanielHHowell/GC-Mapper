import dash
import dash_html_components as html
import dash_core_components as dcc
import analysis

df = analysis.import_data(1)

app = dash.Dash('drug-discovery')
server = app.server

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/bootswatch/3.3.7/paper/bootstrap.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css",
                "https://raw.githubusercontent.com/DanielHHowell/ChromaTune/master/static/css/style.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium"]

for css in external_css:
    app.css.append_css({"external_url": css})



BACKGROUND = 'rgb(252, 252, 252)'


def scatter_plot_3d(
        x=df['X'],
        y=df['Y'],
        z=df['Phase'],
        color=df['Color'],
        xlabel='X',
        ylabel='Y',
        zlabel='Phase',
        plot_type='scatter3d',
):
    def axis_template_3d(title, type='linear'):
        return dict(
            showbackground=True,
            backgroundcolor=BACKGROUND,
            gridcolor='rgb(225, 225, 225)',
            title=title,
            type=type,
            zerolinecolor='rgb(252, 252, 252)'
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
        text=df['Name'],
        type=plot_type,
    )]

    layout = dict(
        font=dict(family='Raleway'),
        hovermode='closest',
        showlegend=False,
        # scene=dict(
        #     xaxis=axis_template_3d(xlabel),
        #     yaxis=axis_template_3d(ylabel),
        #     zaxis=axis_template_3d(zlabel),
        # )
    )

    return dict(data=data, layout=layout)


FIGURE = scatter_plot_3d()

app.layout = html.Div([
    html.Div([
        html.Nav([
            html.Div([

                # Left header
                html.A([
                    html.Div([
                        html.Img(
                            src='https://i.imgur.com/UEH2EBT.png',
                            style={'width': 220, 'margin-top': '12%'},
                        ),
                        html.Img(
                            src='https://i.imgur.com/V5stVH0.png',
                            style={'width': 40, 'margin-top': '12%', 'position': 'center'},
                        ),
                    ], className='navbar-header')
                ], href='http://127.0.0.1:5000'),

                # Right header
                html.Div([
                    html.Ul([
                        html.Li([
                            html.Div([
                                html.A([

                                    html.Div([
                                        html.Img(src='https://i.imgur.com/pmuOmIv.png',
                                                 style={'width': 55, 'margin-top': '30%', 'margin-right': 30,
                                                        'position': 'center'})
                                    ], className='row'),

                                ], href='http://127.0.0.1:5000/profile')
                            ], className='icon-container container')
                        ])
                    ], className='nav navbar-nav navbar-right')
                ], className='navbar-collapse collapse')

            ], className='container-fluid'),
        ], className='navbar navbar-default'),
    ], id='header'),

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

            dcc.Graph(id='clickable-graph',
                      style=dict(height='1600px', width='1750px'),
                      hoverData=dict(points=[dict(pointNumber=0)]),
                      figure=FIGURE),

        ]),

    ], className='row', style={'margin-left': '15%'}),

    html.Footer([
        html.Div([
            html.A('by Daniel Howell',
                   href='mailto:danielhhowell@aol.com')
        ], className='container')
    ], className='footer', style={'position': 'bottom',
                                  'bottom': 0, 'width': '100%',
                                  'height': 60, 'line-height': 60,
                                  'background-color': '#f5f5f5'})
])

if __name__ == '__main__':
    app.run_server()