import dash_html_components as html
import dash_bootstrap_components as dbc
from layout_styles import CONTENT_STYLE

header = html.H4("Thanks for trying out our app!")
subheader = html.H6("It's really just the beginning for community data exploration.")
feedback_link = dbc.CardLink("http://go.nhsa.org/feedback", href="http://go.nhsa.org/feedback")
feedback_request = html.P("If you would like to give some feedback on how to make this tool better, please go to:")
kidscount_text = html.P("Another great resource for county data is Kids Count. Check it out here:")
kidscount_link = dbc.CardLink("https://datacenter.kidscount.org/", href="https://datacenter.kidscount.org/")
resources_text = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    header,
                                    subheader,
                                    feedback_request,
                                    feedback_link,
                                    kidscount_text,
                                    kidscount_link
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=6
                )
            ], justify="center", align="center"
        )

layout = html.Div([resources_text], style=CONTENT_STYLE)