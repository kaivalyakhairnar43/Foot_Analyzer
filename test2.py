import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from soccerplots.radar_chart import Radar
import matplotlib.pyplot as plt
import os
import io
import base64



# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "FootAnalyzer"
app.config.suppress_callback_exceptions = True  # Suppress callback exceptions

# Define the layout of the app
app.layout = html.Div([
    html.Title("FootAnalyzer: Football Analytics Dashboard"),
    html.H1("FootAnalyzer"),
    html.H2("Football Analytics Dashboard for in-depth player profile statistics analysis"),
    dcc.RadioItems(
        id='chart-type-radio',
        options=[
            {'label': 'Individual Player', 'value': 'individual'},
            {'label': 'Comparison', 'value': 'comparison'}
        ],
        value='individual',
        labelStyle={'display': 'inline-block'}
    ),
    html.Br(),
    dcc.Dropdown(
        id='stat-type-dropdown',
        options=[
            {'label': 'Keeper', 'value': 'Keeper'},
            {'label': 'Shooting', 'value': 'Shooting'},
            {'label': 'Passing', 'value': 'Passing'},
            {'label': 'Defense', 'value': 'Defense'},
        ],
        placeholder="Select a Stat Type"
    ),
    html.Br(),
    html.Div(id='dropdown-container')
])

# Mapping for league names to file names
league_files = {
    'Premier League': 'PL_FINAL.xlsm',
    'Laliga': 'LALIGA_FINAL.xlsm',
    'Serie A': 'SERIA_ALL.xlsm',
    'Bundesliga': 'BUNDESLIGA_ALL.xlsm',
    'Ligue 1': 'LIGUE1_ALL.xlsm'
}

# Load data from Excel files
def load_data(league, stat_type):
    file_path = f'data/{league_files[league]}'
    sheet_name = stat_type
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

# Filter data based on season
def filter_data_by_season(df, season):
    return df[df['Season'] == season]

# Function to convert Matplotlib figure to Plotly figure
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return f"data:image/png;base64,{img_base64}"

# Function to generate radar chart for a single player
def generate_single_player_radar(player, stat_type, league, season):
    df = load_data(league, stat_type)
    df_filtered = filter_data_by_season(df, season)
    player_data = df_filtered[df_filtered['Player'] == player].iloc[0].to_dict()

    if stat_type == "Keeper":
        stats = [player_data[column] for column in ['90s', 'GA90', 'Save%', 'CS%', 'PKatt', 'PKSave%']]
        params = ['90s', 'GA90', 'Save%', 'CS%', 'PKatt', 'PKSave%']
        ranges = [(3.4, 38), (0.48, 3.75), (26.7, 92), (0, 80), (0, 15), (0, 100)]
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: @slothfulwave612\n\n90s = Minutes played divided by 90, GA90 = Goals Against per 90 min, Save% = Shots Save percentage, CS% = Clean Sheet percentage\nPKatt = Penalty Kicks attempted, PKSave% = Penalty Kick save percentage"
    elif stat_type == "Shooting":
        stats = [player_data[column] for column in ['90s', 'Gls', 'Sh/90', 'SoT%', 'xG', 'npxG', 'G-xG', 'PK']]
        params = ['90s', 'Gls', 'Sh/90', 'SoT%', 'xG', 'npxG', 'G-xG', 'PK']
        ranges = [(0, 38), (0, 41), (0, 45), (0, 100), (0, 33.2), (0, 29.3), (-8.7, 12.2), (0, 14)]
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\n90s = Minutes played divided by 90, Gls = Goals Scored, Sh/90 = Total Shots per 90, SoT% = Shots on Target %\nxG = Expected Goals, npxG = Non Penalty Expected Goals, G-xG = Goals minus Expected Goals, PK = Penalties Won or Made"
    elif stat_type == "Passing":
        stats = [player_data[column] for column in ['90s', 'Cmp', 'Cmp%', 'PrgDist', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'CrsPA', 'PrgP']]
        params = ['90s', 'Cmp', 'Cmp%', 'PrgDist', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'CrsPA', 'PrgP']
        ranges = [(0, 38), (0, 3000), (0, 100), (0, 38000), (0, 24), (0, 20), (0, 18), (-9, 9), (0, 140), (0, 380), (0, 60), (0, 380)]
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\n90s = Minutes played divided by 90, Gls = Goals Scored, Sh/90 = Total Shots per 90, xG = Expected Goals, npxG = Non Penalty Expected Goals\nG-xG = Goals minus Expected Goals, PrgDist = Progressive Passing Distance, Ast = Assist, xAG = Expected Goals Assisted, KP = Key Passes\n1/3 = Passes into Final 3rd, CrsPA = Croses into Penalty Area, PrgP = Progressive Passes"
    elif stat_type == "Defense":
        stats = [player_data[column] for column in ['90s', 'Tkl', 'Tkl%', 'DrTkl', 'DrTkl%', 'Blocks', 'Int', 'Clr', 'Err']]
        params = ['90s', 'Tkl', 'Tkl%', 'DrTkl', 'DrTkl%', 'Blocks', 'Int', 'Clr', 'Err']
        ranges = [(0, 38), (0, 150), (0, 100), (0, 80), (0, 100), (0, 100), (0, 120), (0, 250), (0, 15)]
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\n90s = Minutes played divided by 90, Tkl = Tackles made, Tkl% = Tackle Success %, DrTkl = Dribblers Tackled\nDrTkl% = Dribblers Tackled Success %, Blocks = No. of times Ball Blocked, Int = Interceptions, Clr = Clearances\nErr = Errors"
    else:
        return None
    
    title = {
        'title_name': player_data['Player'],
        'title_color': "#E3DDED",
        'subtitle_name': player_data['Squad'],
        'subtitle_color': "#FC2128",
        'title_name_2': stat_type,
        'title_color_2': "#E3DDED",
        'subtitle_name_2': season,
        'subtitle_color_2': '#FC2128',
        'title_fontsize': 18,
        'subtitle_fontsize': 15
    }


    radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#BFE9BF", range_color="#BFE9BF", range_fontsize=7.5, label_fontsize=13)

    fig, ax = radar.plot_radar(ranges=ranges, values=stats, params=params, radar_color=["#0f4c75", "#e94560"] , title=title, stat_type=stat_type, endnote=endnote, dpi=500, alphas=[0.3, 0.4])
    return fig_to_base64(fig)


# Function to generate radar chart for player comparison
def generate_comparison_radar(player1, player2, stat_type, league1, league2, season1, season2):
    df1 = load_data(league1, stat_type)
    df_filtered1 = filter_data_by_season(df1, season1)
    player_data1 = df_filtered1[df_filtered1['Player'] == player1].iloc[0].to_dict()

    df2 = load_data(league2, stat_type)
    df_filtered2 = filter_data_by_season(df2, season2)
    player_data2 = df_filtered2[df_filtered2['Player'] == player2].iloc[0].to_dict()

    if stat_type == "Keeper":
        stats1 = [player_data1[column] for column in ['90s', 'GA90', 'Save%', 'CS%', 'PKatt', 'PKSave%']]
        stats2 = [player_data2[column] for column in ['90s', 'GA90', 'Save%', 'CS%', 'PKatt', 'PKSave%']]
        params = ['90s', 'GA90', 'Save%', 'CS%', 'PKatt', 'PKSave%']
        ranges = [(3.4, 38), (0.48, 3.75), (26.7, 92), (0, 80), (0, 15), (0, 100)]
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: @slothfulwave612\n\nKEEPER RADAR CHART\n90s = Minutes played divided by 90, GA90 = Goals Against per 90 min, Save% = Shots Save percentage, CS% = Clean Sheet percentage\nPKatt = Penalty Kicks attempted, PKSave% = Penalty Kick save percentage"
    elif stat_type == "Shooting":
        stats1 = [player_data1[column] for column in ['90s', 'Gls', 'Sh/90', 'SoT%', 'xG', 'npxG', 'G-xG', 'PK']]
        stats2 = [player_data2[column] for column in ['90s', 'Gls', 'Sh/90', 'SoT%', 'xG', 'npxG', 'G-xG', 'PK']]
        params = ['90s', 'Gls', 'Sh/90', 'SoT%', 'xG', 'npxG', 'G-xG', 'PK']
        ranges = [(0, 38), (0, 41), (0, 45), (0, 100), (0, 33.2), (0, 29.3), (-8.7, 12.2), (0, 14)]
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nSHOOTING RADAR CHART\n90s = Minutes played divided by 90, Gls = Goals Scored, Sh/90 = Total Shots per 90, SoT% = Shots on Target %\nxG = Expected Goals, npxG = Non Penalty Expected Goals, G-xG = Goals minus Expected Goals, PK = Penalties Won or Made"
    elif stat_type == "Passing":
        stats1 = [player_data1[column] for column in ['90s', 'Cmp', 'Cmp%', 'PrgDist', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'CrsPA', 'PrgP']]
        stats2 = [player_data2[column] for column in ['90s', 'Cmp', 'Cmp%', 'PrgDist', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'CrsPA', 'PrgP']]
        params = ['90s', 'Cmp', 'Cmp%', 'PrgDist', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'CrsPA', 'PrgP']
        ranges = [(0, 38), (0, 3000), (0, 100), (0, 38000), (0, 24), (0, 20), (0, 18), (-9, 9), (0, 140), (0, 380), (0, 60), (0, 380)]
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nPASSING RADAR CHART\n90s = Minutes played divided by 90, Gls = Goals Scored, Sh/90 = Total Shots per 90, xG = Expected Goals, npxG = Non Penalty Expected Goals\nG-xG = Goals minus Expected Goals, PrgDist = Progressive Passing Distance, Ast = Assist, xAG = Expected Goals Assisted, KP = Key Passes\n1/3 = Passes into Final 3rd, CrsPA = Croses into Penalty Area, PrgP = Progressive Passes"
    elif stat_type == "Defense":
        stats1 = [player_data1[column] for column in ['90s', 'Tkl', 'Tkl%', 'DrTkl', 'DrTkl%', 'Blocks', 'Int', 'Clr', 'Err']]
        stats2 = [player_data2[column] for column in ['90s', 'Tkl', 'Tkl%', 'DrTkl', 'DrTkl%', 'Blocks', 'Int', 'Clr', 'Err']]
        params = ['90s', 'Tkl', 'Tkl%', 'DrTkl', 'DrTkl%', 'Blocks', 'Int', 'Clr', 'Err']
        ranges = [(0, 38), (0, 150), (0, 100), (0, 80), (0, 100), (0, 100), (0, 120), (0, 250), (0, 15)]
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nDEFENSE RADAR CHART\n90s = Minutes played divided by 90, Tkl = Tackles made, Tkl% = Tackle Success %, DrTkl = Dribblers Tackled\nDrTkl% = Dribblers Tackled Success %, Blocks = No. of times Ball Blocked, Int = Interceptions, Clr = Clearances\nErr = Errors"
    else:
        return None
    


    title = {
        'title_name': player_data1['Player'],
        'title_color': "#f70029",
        'subtitle_name': f"{player_data1['Squad']} - {season1}",
        'subtitle_color': "#ff526f",
        'title_name_2': player_data2['Player'],
        'title_color_2': "#0594f5",
        'subtitle_name_2': f"{player_data2['Squad']} - {season2}",
        'subtitle_color_2': "#69bffa",
        'title_fontsize': 18,
        'subtitle_fontsize': 15
    }

    radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#F0FFF0",
              range_color="#F0FFF0", range_fontsize=7.5, label_fontsize=13)
    
    fig, ax = radar.plot_radar(values=[stats1, stats2], params=params, radar_color=['#f70029', '#0594f5'], title=title, stat_type=stat_type, ranges=ranges, endnote=endnote, dpi=500, alphas=[0.5, 0.4], compare=True)
    return fig_to_base64(fig)


# Callback to update the layout based on the chart type selected
@app.callback(
    Output('dropdown-container', 'children'),
    [Input('chart-type-radio', 'value')]
)
def update_layout(chart_type):
    if chart_type == 'individual':
        return html.Div([
            dcc.Dropdown(
                id='league-dropdown',
                options=[
                    {'label': 'Laliga', 'value': 'Laliga'},
                    {'label': 'Premier League', 'value': 'Premier League'},
                    {'label': 'Serie A', 'value': 'Serie A'},
                    {'label': 'Bundesliga', 'value': 'Bundesliga'},
                    {'label': 'Ligue 1', 'value': 'Ligue 1'},
                ],
                placeholder="Select a League"
            ),
            dcc.Dropdown(
                id='season-dropdown',
                options=[
                    {'label': '18/19', 'value': '18/19'},
                    {'label': '19/20', 'value': '19/20'},
                    {'label': '20/21', 'value': '20/21'},
                    {'label': '21/22', 'value': '21/22'},
                    {'label': '22/23', 'value': '22/23'},
                ],
                placeholder="Select a Season"
            ),
            dcc.Dropdown(
                id='team-dropdown',
                placeholder="Select a Team"
            ),
            dcc.Dropdown(
                id='player-dropdown',
                placeholder="Select a Player"
            ),
            html.Img(id='radar-chart')
        ])
    elif chart_type == 'comparison':
        return html.Div([
            html.Div([
                html.H3("Player 1"),
                dcc.Dropdown(
                    id='league-dropdown-1',
                    options=[
                        {'label': 'Laliga', 'value': 'Laliga'},
                        {'label': 'Premier League', 'value': 'Premier League'},
                        {'label': 'Serie A', 'value': 'Serie A'},
                        {'label': 'Bundesliga', 'value': 'Bundesliga'},
                        {'label': 'Ligue 1', 'value': 'Ligue 1'},
                    ],
                    placeholder="Select a League"
                ),
                dcc.Dropdown(
                    id='season-dropdown-1',
                    options=[
                        {'label': '18/19', 'value': '18/19'},
                        {'label': '19/20', 'value': '19/20'},
                        {'label': '20/21', 'value': '20/21'},
                        {'label': '21/22', 'value': '21/22'},
                        {'label': '22/23', 'value': '22/23'},
                    ],
                    placeholder="Select a Season"
                ),
                dcc.Dropdown(
                    id='team-dropdown-1',
                    placeholder="Select a Team"
                ),
                dcc.Dropdown(
                    id='player-dropdown-1',
                    placeholder="Select a Player"
                ),
            ], style={'width': '45%', 'display': 'inline-block'}),
            html.Div([
                html.H3("Player 2"),
                dcc.Dropdown(
                    id='league-dropdown-2',
                    options=[
                        {'label': 'Laliga', 'value': 'Laliga'},
                        {'label': 'Premier League', 'value': 'Premier League'},
                        {'label': 'Serie A', 'value': 'Serie A'},
                        {'label': 'Bundesliga', 'value': 'Bundesliga'},
                        {'label': 'Ligue 1', 'value': 'Ligue 1'},
                    ],
                    placeholder="Select a League"
                ),
                dcc.Dropdown(
                    id='season-dropdown-2',
                    options=[
                        {'label': '18/19', 'value': '18/19'},
                        {'label': '19/20', 'value': '19/20'},
                        {'label': '20/21', 'value': '20/21'},
                        {'label': '21/22', 'value': '21/22'},
                        {'label': '22/23', 'value': '22/23'},
                    ],
                    placeholder="Select a Season"
                ),
                dcc.Dropdown(
                    id='team-dropdown-2',
                    placeholder="Select a Team"
                ),
                dcc.Dropdown(
                    id='player-dropdown-2',
                    placeholder="Select a Player"
                ),
            ], style={'width': '45%', 'display': 'inline-block'}),
            html.Img(id='radar-chart-comparison')
        ])

# Callback to update team dropdown based on league and season for individual player
@app.callback(
    Output('team-dropdown', 'options'),
    [Input('league-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('stat-type-dropdown', 'value')]
)
def update_team_dropdown(league, season, stat_type):
    if league and season and stat_type:
        df = load_data(league, stat_type)
        df_filtered = filter_data_by_season(df, season)
        teams = df_filtered['Squad'].unique().tolist()
        return [{'label': team, 'value': team} for team in teams]
    return []

# Callback to update player dropdown based on team for individual player
@app.callback(
    Output('player-dropdown', 'options'),
    [Input('team-dropdown', 'value'),
     Input('league-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('stat-type-dropdown', 'value')]
)
def update_player_dropdown(team, league, season, stat_type):
    if team and league and season and stat_type:
        df = load_data(league, stat_type)
        df_filtered = filter_data_by_season(df, season)
        players = df_filtered[df_filtered['Squad'] == team]['Player'].tolist()
        return [{'label': player, 'value': player} for player in players]
    return []

# Callback to update the radar chart for individual player
@app.callback(
    Output('radar-chart', 'src'),
    [Input('player-dropdown', 'value'),
     Input('league-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('stat-type-dropdown', 'value')]
)
def update_radar_chart(player, league, season, stat_type):
    if player and league and season and stat_type:
        img_base64 = generate_single_player_radar(player, stat_type, league, season)
        return img_base64
    return ""


# Callback to update team dropdowns for comparison
@app.callback(
    [Output('team-dropdown-1', 'options'),
     Output('team-dropdown-2', 'options')],
    [Input('league-dropdown-1', 'value'),
     Input('season-dropdown-1', 'value'),
     Input('league-dropdown-2', 'value'),
     Input('season-dropdown-2', 'value'),
     Input('stat-type-dropdown', 'value')]
)
def update_team_dropdown_comparison(league1, season1, league2, season2, stat_type):
    options1 = []
    options2 = []
    if league1 and season1 and stat_type:
        df1 = load_data(league1, stat_type)
        df_filtered1 = filter_data_by_season(df1, season1)
        teams1 = df_filtered1['Squad'].unique().tolist()
        options1 = [{'label': team, 'value': team} for team in teams1]

    if league2 and season2 and stat_type:
        df2 = load_data(league2, stat_type)
        df_filtered2 = filter_data_by_season(df2, season2)
        teams2 = df_filtered2['Squad'].unique().tolist()
        options2 = [{'label': team, 'value': team} for team in teams2]

    return options1, options2

# Callback to update player dropdowns for comparison
@app.callback(
    [Output('player-dropdown-1', 'options'),
     Output('player-dropdown-2', 'options')],
    [Input('team-dropdown-1', 'value'),
     Input('league-dropdown-1', 'value'),
     Input('season-dropdown-1', 'value'),
     Input('team-dropdown-2', 'value'),
     Input('league-dropdown-2', 'value'),
     Input('season-dropdown-2', 'value'),
     Input('stat-type-dropdown', 'value')]
)
def update_player_dropdown_comparison(team1, league1, season1, team2, league2, season2, stat_type):
    options1 = []
    options2 = []
    if team1 and league1 and season1 and stat_type:
        df1 = load_data(league1, stat_type)
        df_filtered1 = filter_data_by_season(df1, season1)
        players1 = df_filtered1[df_filtered1['Squad'] == team1]['Player'].tolist()
        options1 = [{'label': player, 'value': player} for player in players1]

    if team2 and league2 and season2 and stat_type:
        df2 = load_data(league2, stat_type)
        df_filtered2 = filter_data_by_season(df2, season2)
        players2 = df_filtered2[df_filtered2['Squad'] == team2]['Player'].tolist()
        options2 = [{'label': player, 'value': player} for player in players2]

    return options1, options2

# Callback to update the radar chart for player comparison
@app.callback(
    Output('radar-chart-comparison', 'src'),
    [Input('player-dropdown-1', 'value'),
     Input('league-dropdown-1', 'value'),
     Input('season-dropdown-1', 'value'),
     Input('player-dropdown-2', 'value'),
     Input('league-dropdown-2', 'value'),
     Input('season-dropdown-2', 'value'),
     Input('stat-type-dropdown', 'value')]
)
def update_radar_chart_comparison(player1, league1, season1, player2, league2, season2, stat_type):
    if player1 and league1 and season1 and player2 and league2 and season2 and stat_type:
        img_base64 = generate_comparison_radar(player1, player2, stat_type, league1, league2, season1, season2)
        return img_base64
    return ""

if __name__ == '__main__':
    print("Starting the Dash app...")
    app.run_server(debug=True, port=8050)
