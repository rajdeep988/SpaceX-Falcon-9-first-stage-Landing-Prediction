# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="Select Site",
                                                searchable=True
                                                ),
                                html.Br()
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                # marks={0: '0', 100: '1000'},
                                                value=[min_payload, max_payload]),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
               Output(component_id='success-payload-scatter-chart', component_property='figure')],
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])

def get_pie_chart(entered_site, payload_mass):
    filtered_df = spacex_df[['Launch Site', 'class', 'Payload Mass (kg)', 'Booster Version Category']]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='Launch Site',
        title='Total Success Launch by all Sites')
        # payload_df = filtered_df[filtered_df['Payload Mass (kg)'] <= payload_mass]
        payload_df= filtered_df[filtered_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1], inclusive=True)]
        fig2 = px.scatter(payload_df, y="class", x="Payload Mass (kg)", color="Booster Version Category",
                          title=f'Correlation Between Payload Mass and Success of all Sites')

        return fig, fig2
    else:
        df = filtered_df[filtered_df['Launch Site']==entered_site]
        count_df = pd.DataFrame({'class': [0, 1],
                            'count': [df['class'].value_counts(sort=False)[0], df['class'].value_counts(sort=False)[1]]})
        fig = px.pie(count_df, values='count',
        names='class',
        title=f'Total Success Launch by {entered_site} Site',
        color = 'class'
        )
        payload_df = df[df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1], inclusive=True)]
        fig2 = px.scatter(payload_df, y="class", x="Payload Mass (kg)",
                          color="Booster Version Category",
                          title=f'Correlation Between Payload Mass and Success of {entered_site} Site')
        return fig, fig2
        # return the outcomes piechart for a selected site


# Run the app
if __name__ == '__main__':
    app.run_server()


