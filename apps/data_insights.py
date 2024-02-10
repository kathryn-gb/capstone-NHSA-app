import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from layout_styles import CONTENT_STYLE, CARD_TEXT_STYLE
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from app import app

# The structure of the home content is dependent on the variable categories the user selected from the sidebar,
# housed in the index file. Therefore, the content returned to index must be able to vary in both size and substance.
# As such, the presence of every category is checked for with an if statement. If it is present, content is created
# for it. Otherwise, content objects are assigned as None. All content objects != None are returned to app layout.

# first, functions are defined for commonly used charts
# Function for bar chart
def bar_chart(df_x, variable_name_x, county_name, data_type="Whole"):
    # Remove 'Percent of' or 'Number of' from the variable name if exist
    if ('Percent of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Percent of ")[1]
    elif ('Number of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Number of ")[1]
    else:
        pass

    # Generate visual

    # Title & axis varies for the visual based on type of data
    if data_type == 'Whole':
        fig = px.bar(df_x, x='Year', y='County', labels={"Year": "Year", 'County': 'Count'})
        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(height=400,
                          title={'text':'Number of ' + variable_name_x + '<br>' + ' in the last 5 years in ' + county_name,
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
    elif data_type == 'Percentage':
        fig = px.bar(df_x, x='Year', y='County', labels={"Year": "Year", 'County': 'Percent'})
        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(height=400,
                          title={'text':'Percentage of ' + variable_name_x + '<br>' + ' in the last 5 years in ' + county_name,
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
    else:
        fig = px.bar(df_x, x='Year', y='County', labels={"Year": "Year", 'County': variable_name_x})
        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(height=400, title={'text':variable_name_x + '<br>' + ' in the last 5 years in ' + county_name,
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})

    return fig

# Function for stacked bar chart
def stacked_bar_chart(df_x, variable_name_x, county_name, data_type="Whole"):
    # Remove 'Percent of' or 'Number of' from the variable name if exist
    if ('Percent of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Percent of ")[1]
    elif ('Number of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Number of ")[1]
    else:
        pass

    # Generate visual

    # Title & axis varies for the visual based on type of data
    if data_type == 'Whole':
        fig = px.bar(df_x, x='Year', y='County', color="Variable", \
                     labels={"Year": "Year", 'County': 'Count'})
        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(height=400, title={'text':'Number of ' + variable_name_x + \
                                                 '<br>' + ' in the last 5 years in ' + county_name,
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})

    elif data_type == 'Percentage':
        fig = px.bar(df_x, x='Year', y='County', color="Variable", \
                     labels={"Year": "Year", 'County': 'Percent'})
        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(height=400, title={'text':'Percentage of ' + variable_name_x + \
                                                 '<br>' + ' in the last 5 years in ' + county_name,
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
    else:
        fig = px.bar(df_x, x='Year', y='County', color="Variable", \
                     labels={"Year": "Year", 'County': "Count"})
        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(height=400, title={'text':variable_name_x + \
                                                 '<br>' + ' in the last 5 years in ' + county_name,
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
    return fig


# Function for line_chart
def line_chart(df_line, variable_name_x, county_name, data_type='Whole'):
    # Remove 'Percent of' or 'Number of' from the variable name if exist
    if ('Percent of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Percent of ")[1]
    elif ('Number of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Number of ")[1]
    else:
        pass

    # Generate visual

    # Title & axis varies for the visual based on type of data
    if data_type == 'Whole':
        # Generate visual for state vs county trend comparison
        if len(df_line.columns) == 3:
            fig = px.line(df_line, x="Year", y="value", color="variable", hover_name="variable", \
                          labels={"Year": "Year", 'value': 'Count'})
            fig.update_layout(height=400, title={'text':'Change in # of ' + variable_name_x + ' for ' + \
                                                     '<br>' + county_name + ' in the last 5 years',
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))

        # Generate visual for county trend
        elif len(df_line.columns) == 2:
            fig = px.line(df_line, x="Year", y="County", hover_name="Year", \
                          labels={"Year": "Year", 'County': 'Count'})
            fig.update_layout(height=400, title={'text':'Change in # of ' + variable_name_x + ' for ' + \
                                                     '<br>' + county_name + ' in the last 5 years',
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
    elif data_type == 'Percentage':
        # Generate visual for state vs county trend comparison
        if len(df_line.columns) == 3:
            fig = px.line(df_line, x="Year", y="value", color="variable", hover_name="variable", \
                          labels={"Year": "Year", 'value': 'Percent'})
            fig.update_layout(height=400, title={'text':'Change in % of ' + variable_name_x + ' for ' + \
                                                     '<br>' + county_name + ' in the last 5 years',
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
        # Generate visual for county trend
        elif len(df_line.columns) == 2:
            fig = px.line(df_line, x="Year", y="County", hover_name="Year", \
                          labels={"Year": "Year", 'County': 'Percent'})
            fig.update_layout(height=400, title={'text':'Change in % of ' + variable_name_x + ' for ' + \
                                                     '<br>' + county_name + ' in the last 5 years',
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
    elif data_type == 'Whole_no_num':
        # Generate visual for state vs county trend comparison
        if len(df_line.columns) == 3:
            fig = px.line(df_line, x="Year", y="value", color="variable", hover_name="variable", \
                          labels={"Year": "Year", 'value': "Count"})
            fig.update_layout(height=800, title={'text':'Change in ' + variable_name_x + ' for ' + \
                                                     '<br>' + county_name + ' in the last 5 years',
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))

        # Generate visual for county trend
        elif len(df_line.columns) == 2:
            fig = px.line(df_line, x="Year", y="County", hover_name="Year", \
                          labels={"Year": "Year", 'County': "Count"})
            fig.update_layout(height=800, title={'text':'Change in ' + variable_name_x + ' for ' + \
                                                     '<br>' + county_name + ' in the last 5 years',
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
    else:
        # Generate visual for state vs county trend comparison
        if len(df_line.columns) == 3:
            fig = px.line(df_line, x="Year", y="value", color="variable", hover_name="variable", \
                          labels={"Year": "Year", 'value': variable_name_x})
            fig.update_layout(height=400, title={'text':variable_name_x + ' for ' + \
                                                     '<br>' + county_name + ' in the last 5 years',
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
        # Generate visual for county trend
        elif len(df_line.columns) == 2:
            fig = px.line(df_line, x="Year", y="County", hover_name="Year", \
                          labels={"Year": "Year", 'County': variable_name_x})
            fig.update_layout(height=400, title={'text':variable_name_x + ' for ' + \
                                                     '<br>' + county_name + ' in the last 5 years',
                                                 'x': 0.5,
                                                 'xanchor': 'center',
                                                 'font':{'size':13}})
            fig.update_yaxes(rangemode="tozero")
            fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
    return fig

# Function to create dataframe with percentage data for state and county data for line chart
def line_df_comparison(df_x, year_list):
    # Create percentage comparison dataframe universe Vs one comparison
    county_percent_list = []
    state_percent_list = []
    for j in range(2):
        i = 0
        while i in range(df_x.shape[0]):
            percent_value = round((df_x.iloc[i + 1, j] / df_x.iloc[i, j]) * 100, 2)
            if j == 0:
                county_percent_list.append(percent_value)
            else:
                state_percent_list.append(percent_value)
            i = i + 2

    percent_df_x = pd.DataFrame(
        {'Year': year_list,
         'County': county_percent_list,
         'State': state_percent_list
         })

    # Convert dataframe into a format that is readable by the line chart function
    df_x_line = pd.melt(percent_df_x, id_vars=['Year'], value_vars=['County', 'State'])

    return (df_x_line)

# Function to create insight for line chart with state and county comparison
def line_chart_insights(df_line, variable_name_x, year_list, county_name, data_type='Whole', comparison_type = "county_comparison"):
    # Remove 'Percent of' or 'Number of' from the variable name if exist
    if ('Percent of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Percent of ")[1]
    elif ('Number of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Number of ")[1]
    else:
        pass
    # Insight for County Vs State trend comparison. If dataframe has 3 columns, the if statement executes
    if (len(df_line.columns) == 3) & (comparison_type == "county_comparison"):

        # Calculate start year and end year difference between county and state data
        start_yr_difference = round(((df_line[df_line.Year == year_list[0]].iloc[1][2]) - \
                                     (df_line[df_line.Year == year_list[0]].iloc[0][2])), 2)
        end_yr_difference = round(((df_line[df_line.Year == year_list[-1]].iloc[1][2]) - \
                                   (df_line[df_line.Year == year_list[-1]].iloc[0][2])), 2)

        if start_yr_difference < 0:
            start_diff = "greater"
        else:
            start_diff = "lesser"

        if end_yr_difference < 0:
            end_diff = "greater"
        else:
            end_diff = "lesser"
        if data_type == "Whole":
            return(("In " + year_list[0].astype(str) + "," + " the " + variable_name_x + " in " + county_name + " is " + \
                  start_diff + " than " + "state figures by " + abs(start_yr_difference).astype(str) + "."), ("In " + year_list[-1].astype(str) + "," + " the " + variable_name_x + " in " + county_name + " is " + \
                  end_diff + " than " + "state figures by " + abs(end_yr_difference).astype(str) + "."))
        else:
            return(("In " + year_list[0].astype(str) + "," + " the " + variable_name_x + " in " + county_name + " is " + \
                  start_diff + " than " + "state figures by " + abs(start_yr_difference).astype(
                str) + " percentage points."), ("In " + year_list[-1].astype(str) + "," + " the " + variable_name_x + " in " + county_name + " is " + \
                  end_diff + " than " + "state figures by " + abs(end_yr_difference).astype(
                str) + " percentage points."))

    # Insights for County trend.
    elif (len(df_line.columns) == 2) & (comparison_type == "county_comparison"):
        start_vs_end_yr_difference = round(((df_line[df_line.Year == year_list[0]].iloc[0][0]) - \
                                            (df_line[df_line.Year == year_list[-1]].iloc[0][0])), 2)

        if start_vs_end_yr_difference < 0:
            diff = "increased"
        else:
            diff = "reduced"

        if data_type == "Whole":
            return(("In the last " + str(len(year_list)) + " years, " + " the number of " + variable_name_x + \
                  " in " + county_name), (" " + diff + " by " + (abs(start_vs_end_yr_difference)).astype(str) + "."))
        else:
            return(("In the last " + str(len(year_list)) + " years, " + " the " + variable_name_x + " in " + \
                  county_name), (" " + diff + " by " + (abs(start_vs_end_yr_difference)).astype(str) + " percentage points."))
    # Insights for variable comparison trend.
    elif (len(df_line.columns) == 3) & (comparison_type == "variable_comparison"):
        variable_list = df_line.variable.unique().tolist()
        insights_list = []
        for var in variable_list:
            df_line_n = df_line[df_line['variable'] == var]
            start_vs_end_yr_difference = round(((df_line_n[df_line_n.Year == year_list[0]].iloc[0][2]) - \
                                                (df_line_n[df_line_n.Year == year_list[-1]].iloc[0][2])), 2)
            if start_vs_end_yr_difference < 0:
                diff = "increased"
            else:
                diff = "reduced"

            if data_type == "Whole":
                insights_list.append("In the last " + str(len(year_list)) + " years, " + "the number of " + var + \
                      " in " + county_name + " " + diff + " by " + (abs(start_vs_end_yr_difference)).astype(int).astype(
                    str) + ".")
            else:
                insights_list.append("In the last " + str(len(year_list)) + " years, " + "the " + var + " in " + \
                      county_name + " " + diff + " by " + (abs(start_vs_end_yr_difference)).astype(int).astype(
                    str) + " percentage points.")
        return insights_list

# Function to create insight for bar chart with county data
def bar_chart_insights(df_x, variable_name_x, year_list, county_name, data_type="Whole"):
    # Remove 'Percent of' or 'Number of' from the variable name if exist
    if ('Percent of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Percent of ")[1]
    elif ('Number of ' in variable_name_x):
        variable_name_x = variable_name_x.split("Number of ")[1]
    else:
        pass

    # Calculate start year and end year difference between county and state data

    start_vs_end_yr_difference = round(((df_x[df_x.Year == year_list[0]].iloc[0][0]) - \
                                        (df_x[df_x.Year == year_list[-1]].iloc[0][0])), 2)

    if start_vs_end_yr_difference < 0:
        diff = "increased"
    else:
        diff = "reduced"
    if data_type == "Whole":
        return("In the last " + str(len(year_list)) + " years, " + " the number of " + variable_name_x + \
              " in " + county_name + " " + diff + " by " + (abs(start_vs_end_yr_difference)).astype(str) + ".")
    else:
        return("In the last " + str(len(year_list)) + " years, " + " the " + variable_name_x + " in " + \
              county_name + " " + diff + " by " + (abs(start_vs_end_yr_difference)).astype(str) + " percentage points.")

# Now, the layout content is generated. Collapse categories to get a high level view.
def return_insights(fulldf):
    column_list = fulldf.columns
    category_list = fulldf.Category.unique()
    county_name = column_list[0]
    year_list = fulldf.Year.unique()
    truecontentlist = []
    if 'Race and Ethnicity' in category_list:
        headerRE = html.H4('Race and Ethnicity')
        REfulldf = fulldf[fulldf.Category=='Race and Ethnicity']
        REfulldf.reset_index(drop=True, inplace=True)
        REdf = REfulldf.drop(REfulldf[(REfulldf.Year != max(year_list)) | (REfulldf.Variable == "Universe: Total Population") | (REfulldf.Variable == "Not Hispanic or Latino Total") | (REfulldf.Variable == "Hispanic or Latino Total")].index)
        ethnicityvals = []
        racevals = []
        for var in REdf["Variable"]:
            ethnicityvals.append(var.split('_')[0])
            racevals.append(var.split('_')[1])
        REdf["Total Population"] = "Total Population"  # in order to have a single root node
        REdf["Ethnicity"] = ethnicityvals
        REdf["Race"] = racevals
        totalpop = sum(REdf[county_name])
        REdf["Percent of population"] = (REdf[county_name] / totalpop) * 100
        percenteth = REdf.groupby('Ethnicity').sum()
        percentnot = percenteth[percenteth.index=='Not Hispanic or Latino']['Percent of population'].iloc[0].round(2)
        percentyes = percenteth[percenteth.index=='Hispanic or Latino']['Percent of population'].iloc[0].round(2)
        figRE = px.treemap(REdf, path=['Total Population', 'Ethnicity', 'Race'], values=county_name,
                          color='Race')
        figRE.update_traces(marker_colors=["#00adf2",  # asian hispan
                                          "#fcce7e",  # some other not hispan
                                          "#00adf2",  # asian not hispan
                                          "lightblue",  # 2+ hispan
                                          "#cfa8ed",  # american indian not hispan
                                          "#fcce7e",  # some other hispan
                                          "pink",  # black hispan
                                          "lightblue",  # 2+ not hispan
                                          "pink",  # black not hispan
                                          "#a0e8b4",  # hispan white
                                          "magenta",  # hispan native hawaiian
                                          "#a0e8b4",  # white not hispan
                                          "#cfa8ed",  # american indian hispan
                                          "magenta",  # native hawaiian not hispan
                                          "darkblue",  # hispan total
                                          "blue",  # not hispan total
                                          "lightgray"])  # total population
        figRE.data[0].textinfo = 'label+text+value+percent parent'
        content_RE_row = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=figRE), md=12
                )
            ]
        )
        content_RE_textbox = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.H4(children=[county_name + ' Ethnicity'], className='card-title',
                                            style=CARD_TEXT_STYLE),
                                    html.P(children=[str(
                                        percentnot) + '% of residents do not identify as Hispanic or Latino, and ' + str(
                                        percentyes) + '% do identify as Hispanic or Latino'], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerRE)
        truecontentlist.append(content_RE_row)
        truecontentlist.append(content_RE_textbox)
    if 'Children in Foster Care' in category_list:
        headerCF = html.H4('Children in Foster Care')
        df_1 = fulldf[fulldf.Category == 'Children in Foster Care']

        # Extract variable names and county names
        category_name_1 = df_1['Category'].iloc[0]
        variable_name_1 = df_1['Variable'].iloc[0]
        df_1.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for line chart with state comparison
        df_1_line = pd.melt(df_1, id_vars=['Year'], value_vars=['County', 'State'])

        # return bar chart
        figCF_bar = bar_chart(df_1, variable_name_1, county_name, "Percentage")
        # return bar chart insights
        CFbarsights = bar_chart_insights(df_1, variable_name_1, year_list, county_name, "Percentage")

        # return line chart with state comparison and insights
        figCF_line = line_chart(df_1_line, variable_name_1, county_name, "Percentage")
        CFlinesights, CFsecond = line_chart_insights(df_1_line, variable_name_1, year_list, county_name, "Percentage")
        content_CF_row1 = dbc.Row(
            [
                dbc.Col(
                        dcc.Graph(figure=figCF_bar), md=12
                )
            ]
        )
        content_CF_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=figCF_line), md=12
                )
            ]
        )
        content_CF_textbox1 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    #html.H4(children=['Insight'], className='card-title', style=CARD_TEXT_STYLE),
                                    html.P(children=[CFbarsights], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        content_CF_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    # html.H4(children=['Insight'], className='card-title', style=CARD_TEXT_STYLE),
                                    html.P(children=[CFlinesights + CFsecond], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        if np.isnan(figCF_bar.data[0]['y']).all():
            content_CF_row1 = dbc.Row([dbc.Col(html.P("Data unavailable for this county"))])
            content_CF_textbox1 = ''
        truecontentlist.append(headerCF)
        truecontentlist.append(content_CF_row1)
        truecontentlist.append(content_CF_textbox1)
        truecontentlist.append(content_CF_row2)
        truecontentlist.append(content_CF_textbox2)
    if 'SSI, Cash Public Assistance, Food Stamps' in category_list:
        headerSSI = html.H4('SSI, Cash Public Assistance, Food Stamps')
        df_2 = fulldf[fulldf.Category == 'SSI, Cash Public Assistance, Food Stamps'].reset_index(drop=True)
        variables_list_2 = df_2.Variable.unique()
        category_name_2 = df_2['Category'].iloc[0]
        variable_name_2 = df_2['Variable'].iloc[1]  # iloc[0] is for universe variable
        df_2.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for bar chart with single variable
        df_2_bar = df_2[~df_2['Variable'].str.contains('Universe')]

        # Data frame for line chart with percent conversion & comparison with state
        df_2_line = line_df_comparison(df_2, year_list)

        # return visuals

        # return bar chart
        SSIbar_figure = bar_chart(df_2_bar, variable_name_2, county_name, "Whole")

        # return bar chart insights
        SSIBARSIGHTS = bar_chart_insights(df_2_bar, variable_name_2, year_list, county_name, "Whole")

        # return line chart with state comparison
        SSIline_figure = line_chart(df_2_line, variable_name_2, county_name, "Percentage")

        # return line chart with state comparison insights
        SSILINESIGHTS, SSIsecond = line_chart_insights(df_2_line, variable_name_2, year_list, county_name, "Percentage")
        content_SSI_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=SSIbar_figure), md=12
                )
            ]
        )
        content_SSI_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=SSIline_figure), md=12
                )
            ]
        )
        content_SSI_textbox1 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    #html.H4(children=[], className='card-title', style=CARD_TEXT_STYLE),
                                    html.P(children=[SSIBARSIGHTS], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        content_SSI_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    #html.H4(children=[], className='card-title',style=CARD_TEXT_STYLE),
                                    html.P(children=[SSILINESIGHTS + SSIsecond], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerSSI)
        truecontentlist.append(content_SSI_row1)
        truecontentlist.append(content_SSI_textbox1)
        truecontentlist.append(content_SSI_row2)
        truecontentlist.append(content_SSI_textbox2)
    if 'Unemployment Rate' in category_list:
        headerUN = html.H4('Unemployment Rate')
        df_3 = fulldf[fulldf.Category == 'Unemployment Rate']

        # Extract variable names and county names
        category_name_3 = df_3['Category'].iloc[0]
        variable_name_3 = df_3['Variable'].iloc[0]
        df_3.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for line chart with state comparison
        df_3_line = pd.melt(df_3, id_vars=['Year'], value_vars=['County', 'State'])

        # return bar chart
        UNbar_figure = bar_chart(df_3, variable_name_3, county_name, "Rate")

        # return bar chart insights
        UNBARSIGHTS = bar_chart_insights(df_3, variable_name_3, year_list, county_name, "Rate")

        # return line chart with state comparison
        UNline_figure = line_chart(df_3_line, variable_name_3, county_name, "Rate")

        # return line chart with state comparison insights
        UNLINESIGHTS, UNsecond = line_chart_insights(df_3_line, variable_name_3, year_list, county_name, "Rate")
        content_UN_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=UNbar_figure), md=12
                )
            ]
        )
        content_UN_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=UNline_figure), md=12
                )
            ]
        )
        content_UN_textbox1 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    #html.H4(children=[], className='card-title', style=CARD_TEXT_STYLE),
                                    html.P(children=[UNBARSIGHTS], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        content_UN_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    # html.H4(children=[], className='card-title', style=CARD_TEXT_STYLE),
                                    html.P(children=[UNLINESIGHTS + UNsecond], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerUN)
        truecontentlist.append(content_UN_row1)
        truecontentlist.append(content_UN_textbox1)
        truecontentlist.append(content_UN_row2)
        truecontentlist.append(content_UN_textbox2)
    if 'Teen mothers' in category_list:
        headerTM = html.H4('Teen mothers')
        # Dataframe for a single selection of state, county and category by user
        df_4 = fulldf[fulldf.Category == 'Teen mothers']

        # Extract variable names and county names
        category_name_4 = df_4['Category'].iloc[0]
        variable_name_4 = df_4['Variable'].iloc[0]
        df_4.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for line chart with state comparison
        df_4_line = pd.melt(df_4, id_vars=['Year'], value_vars=['County', 'State'])

        # return bar chart
        TMbar_figure = bar_chart(df_4, variable_name_4, county_name, "Whole")

        # return bar chart insights
        TMINSB = bar_chart_insights(df_4, variable_name_4, year_list, county_name, "Whole")

        # return line chart with state comparison
        TMline_figure = line_chart(df_4_line, variable_name_4, county_name)

        # return line chart with state comparison insights
        TMINSL, TMsecond = line_chart_insights(df_4_line, variable_name_4, year_list, county_name, "Whole")
        content_TM_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=TMbar_figure), md=12
                )
            ]
        )
        content_TM_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=TMline_figure), md=12
                )
            ]
        )
        content_TM_textbox1 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    #html.H4(children=[county_name + ' Ethnicity'], className='card-title', style=CARD_TEXT_STYLE),
                                    html.P(children=[TMINSB], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        content_TM_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=[TMINSL + TMsecond], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerTM)
        truecontentlist.append(content_TM_row1)
        truecontentlist.append(content_TM_textbox1)
        truecontentlist.append(content_TM_row2)
        truecontentlist.append(content_TM_textbox2)
    if 'Child Poverty' in category_list:
        headerCP = html.H4('Child Poverty')
        # Dataframe for a single selection of state, county and category by user
        df_5 = fulldf[fulldf.Category == 'Child Poverty']

        # Extract variable names and county names
        category_name_5 = df_5['Category'].iloc[0]
        variable_name_5 = df_5['Variable'].iloc[1]

        # Filter data for a single variable
        df_5 = df_5[df_5.Variable == variable_name_5]

        df_5.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for line chart
        df_5_line = df_5[['County', 'Year']]

        # return bar chart
        CPbar_figure = bar_chart(df_5, variable_name_5, county_name, "Whole")

        # return bar chart insights
        CPINSB = bar_chart_insights(df_5, variable_name_5, year_list, county_name, "Whole")

        # return line chart with state comparison
        CPline_figure = line_chart(df_5_line, variable_name_5, county_name)

        # return line chart with state comparison insights
        CPINSL, CPsecond = line_chart_insights(df_5_line, variable_name_5, year_list, county_name, "Whole")
        content_CP_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=CPbar_figure), md=12
                )
            ], justify="center", align="center"
        )
        content_CP_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=CPline_figure), md=12
                )
            ]
        )
        content_CP_textbox1 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=[CPINSB], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        content_CP_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=[CPINSL + CPsecond], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerCP)
        truecontentlist.append(content_CP_row1)
        truecontentlist.append(content_CP_textbox1)
        truecontentlist.append(content_CP_row2)
        truecontentlist.append(content_CP_textbox2)
    if 'Health Insurance Coverage' in category_list:
        headerHI = html.H4('Health Insurance Coverage')
        df_6 = fulldf[fulldf.Category == 'Health Insurance Coverage'].reset_index(drop=True)
        variables_list_6 = df_6.Variable.unique()
        category_name_6 = df_6['Category'].iloc[0]
        variable_name_6 = df_6['Variable'].iloc[1]  # iloc[0] is for universe variable
        df_6.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for bar chart with single variable
        df_6_bar = df_6[~df_6['Variable'].str.contains('Universe')]

        # Data frame for line chart with percent conversion & comparison with state
        df_6_line = line_df_comparison(df_6, year_list)

        # return bar chart
        HIbar_figure = bar_chart(df_6_bar, variable_name_6, county_name, "Whole")

        # return bar chart insights
        HIINSB = bar_chart_insights(df_6_bar, variable_name_6, year_list, county_name, "Whole")

        # return line chart with state comparison
        HIline_figure = line_chart(df_6_line, variable_name_6, county_name, "Percentage")

        # return line chart with state comparison insights
        HIINSL, HIsecond = line_chart_insights(df_6_line, variable_name_6, year_list, county_name, "Percentage")
        content_HI_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=HIbar_figure), md=12
                )
            ]
        )
        content_HI_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=HIline_figure), md=12
                )
            ]
        )
        content_HI_textbox1 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=[HIINSB], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        content_HI_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=[HIINSL + HIsecond], style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerHI)
        truecontentlist.append(content_HI_row1)
        truecontentlist.append(content_HI_textbox1)
        truecontentlist.append(content_HI_row2)
        truecontentlist.append(content_HI_textbox2)
    if 'Household Composition (children under 6)' in category_list:
        headerHC = html.H4('Household Composition (Children under 6)')
        df_7 = fulldf[fulldf.Category == 'Household Composition (children under 6)'].reset_index(drop=True)
        variables_list_7 = df_7.Variable.unique()[1:4]
        category_name_7 = df_7['Category'].iloc[0]
        variable_name_7 = df_7['Variable'].iloc[0]
        variable_name_7 = variable_name_7.split(": ")[1]
        df_7.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for bar chart with single variable
        df_7_bar = df_7[df_7['Variable'].isin(variables_list_7)]

        # Data frame for line chart with percent conversion & comparison with state
        df_7_line = df_7_bar.drop(df_7_bar.columns[[1, 4]], axis = 1)
        df_7_line = df_7_line[['Year', 'Variable', 'County']]
        df_7_line.columns = ['Year', 'variable', 'value']

        # return bar chart
        HCbar_figure = stacked_bar_chart(df_7_bar, variable_name_7, county_name, "Whole")

        # return line chart with state comparison
        HCline_figure = line_chart(df_7_line, variable_name_7,county_name,"Whole")

        # return line chart with state comparison insights
        HCINSL= line_chart_insights(df_7_line,variable_name_7, year_list, county_name, "Whole","variable_comparison")
        content_HC_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=HCbar_figure), md=12
                )
            ]
        )
        content_HC_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=HCline_figure), md=12
                )
            ]
        )
        content_HC_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=HCINSL, style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerHC)
        truecontentlist.append(content_HC_row1)
        truecontentlist.append(content_HC_row2)
        truecontentlist.append(content_HC_textbox2)
    if 'Population Living With Disabilities' in category_list:
        headerDB = html.H4('Population Living With Disabilities')
        df_8 = fulldf[fulldf.Category == 'Population Living With Disabilities'].reset_index(drop=True)
        variables_list_8 = df_8.Variable.unique()[1:4]
        category_name_8 = df_8['Category'].iloc[0]
        variable_name_8 = df_8['Variable'].iloc[0]
        variable_name_8 = variable_name_8.split(": ")[1] + " with hearing & vision disabilities"
        df_8.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for bar chart with single variable
        df_8_bar = df_8[df_8['Variable'].isin(variables_list_8)]

        # Print line chart comparing vision and sight disabilities
        df_8_line = df_8_bar.drop(df_8_bar.columns[[1, 4]], axis=1)
        df_8_line = df_8_line[['Year', 'Variable', 'County']]
        df_8_line.columns = ['Year', 'variable', 'value']

        # return bar chart
        DBbar_figure = stacked_bar_chart(df_8_bar, variable_name_8, county_name, "Whole")

        # return line chart with state comparison
        DBline_figure = line_chart(df_8_line, variable_name_8,county_name,"Whole")

        # return line chart with state comparison insights
        DBINSL = line_chart_insights(df_8_line,variable_name_8,year_list, county_name, "Whole","variable_comparison")
        content_DB_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=DBbar_figure), md=12
                )
            ]
        )
        content_DB_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=DBline_figure), md=12
                )
            ]
        )
        content_DB_textbox1 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=DBINSL, style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerDB)
        truecontentlist.append(content_DB_row1)
        truecontentlist.append(content_DB_row2)
        truecontentlist.append(content_DB_textbox1)
    if 'School Enrollment' in category_list:
        headerSE= html.H4('School Enrollment')
        df_9 = fulldf[fulldf.Category == 'School Enrollment'].reset_index(drop=True)
        variables_list_9 = df_9.Variable.unique()
        category_name_9 = df_9['Category'].iloc[0]
        variable_name_9 = "Number of children enrolled in kindergarten, nursery school or preschool"
        df_9.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        df_9_bar = df_9[df_9['Variable'].isin(variables_list_9)]

        df_9_line = df_9_bar.drop(df_9_bar.columns[[1, 4]], axis=1)
        df_9_line = df_9_line[['Year', 'Variable', 'County']]
        df_9_line.columns = ['Year', 'variable', 'value']

        # return bar chart
        SEbar_figure = stacked_bar_chart(df_9_bar, variable_name_9, county_name, "Whole")

        # return line chart with state comparison
        SEline_figure = line_chart(df_9_line, variable_name_9,county_name,"Whole")

        # return line chart with state comparison insights
        SEINSL = line_chart_insights(df_9_line,variable_name_9, year_list, county_name, "Whole","variable_comparison")
        content_SE_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=SEbar_figure), md=12
                )
            ]
        )
        content_SE_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=SEline_figure), md=12
                )
            ]
        )
        content_SE_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=SEINSL, style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerSE)
        truecontentlist.append(content_SE_row1)
        truecontentlist.append(content_SE_row2)
        truecontentlist.append(content_SE_textbox2)
    if 'Educational Attainment' in category_list:
        headerEA = html.H4('Educational Attainment')
        df_10 = fulldf[fulldf.Category == 'Educational Attainment'].reset_index(drop=True)
        variables_list_10 = df_10.Variable.unique()[1:7]
        category_name_10 = df_10['Category'].iloc[0]
        variable_name_10 = "Educational attainment of Population 25 years and over"
        df_10.columns = ['County', 'State', 'Year', 'Variable', 'Category']

        # Data frame for bar chart with single variable
        df_10_bar = df_10[df_10['Variable'].isin(variables_list_10)]

        # Data frame for line chart with percent conversion & comparison with state
        df_10_line = df_10_bar.drop(df_10_bar.columns[[1, 4]], axis=1)
        df_10_line = df_10_line[['Year', 'Variable', 'County']]
        df_10_line.columns = ['Year', 'variable', 'value']

        # return bar chart
        EAbar_figure = stacked_bar_chart(df_10_bar, variable_name_10, county_name, "Whole_no_num")

        # return line chart with state comparison
        EAline_figure = line_chart(df_10_line, variable_name_10,county_name,"Whole_no_num")

        # return line chart with state comparison insights
        EAINSL = line_chart_insights(df_10_line,variable_name_10, year_list, county_name, "Whole","variable_comparison")
        content_EA_row1 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=EAbar_figure), md=12
                )
            ]
        )
        content_EA_row2 = dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=EAline_figure), md=12
                )
            ]
        )
        content_EA_textbox2 = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [

                            dbc.CardBody(
                                [
                                    html.P(children=EAINSL, style=CARD_TEXT_STYLE),
                                ]
                            )
                        ], color='#a9dad6'
                    ),
                    md=12
                )
            ]
        )
        truecontentlist.append(headerEA)
        truecontentlist.append(content_EA_row1)
        truecontentlist.append(content_EA_row2)
        truecontentlist.append(content_EA_textbox2)

    return html.Div(truecontentlist, style=CONTENT_STYLE)

