
from flask import Flask, render_template, request, redirect
import pandas as pd
import matplotlib.pyplot as plt
import os
from soccerplots.radar_chart import Radar

app = Flask(__name__)
leagues = ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"]
# Replace these file paths with the actual paths of your Excel files
file_paths = {
    "Premier League": "PL_FINAL.xlsx",
    "La Liga": "LALIGA_FINAL.xlsx",
    "Serie A": "SERIA_ALL.xlsx",
    "Bundesliga": "BUNDESLIGA_ALL.xlsx",
    "Ligue 1": "LIGUE1_ALL.xlsx"
}


def read_data(file_path, season, stat_type, league):
    data = pd.read_excel(file_path, sheet_name=stat_type, engine='openpyxl')
    
    filtered_data = data[(data['Season'] == season) & (data['League'] == league)]
    teams = filtered_data['Squad'].unique().tolist()
    players = filtered_data['Player'].unique().tolist()
    
    return teams, players 


@app.route('/', methods=['GET', 'POST'])
def home():
    # league = request.form.get('league')
    # season = request.form.get('season')
    # stat_type = request.form.get('stat_type')
    # player = request.form.get('player')
    # comparison = request.form.get('comparison')

    # teams, players = read_data(league, season, stat_type)
    if request.method=='POST':
        print("Check check check ")
        print("Check")
        league = request.form.get('league')
        season = request.form.get('season')
        stat_type = request.form.get('stat_type')
        player = request.form.get('player')
        comparison = request.form.get('comparison')

        teams, players = read_data(league, season, stat_type)
        print(teams, players)
        image_path=None
        if comparison == 'single':
            image_path = generate_single_player_radar(player, stat_type, league, season)
        elif comparison == 'compare':
            player2 = request.form.get('player2')
            league2 = request.form.get('league2')
            season2 = request.form.get('season2')
            image_path = generate_comparison_radar(player, player2, stat_type, league, league2, season, season2)

        # Save radar chart image
        # image_path = os.path.join('static', 'radar_chart.png')
        # fig.savefig(image_path)
        # plt.close(fig)

        # temp=generate_single_player_radar(player, stat_type, league, season)
        # print(temp)
        return render_template('main_interface.html', image_path=image_path, teams=teams, players=players)
    return render_template('main_interface.html')
    return "Hola! Welcome to FootAnalyzer!!"

@app.route('/generate_radar_chart', methods=['POST'])
def generate_radar_chart():

    if request.method=="POST":
        print("check")
        league = request.form.get('league')
        season = request.form.get('season')
        stat_type = request.form.get('stat_type')
        player = request.form.get('player')
        comparison = request.form.get('comparison')
        print(request.form)

        teams, players = read_data(league, season, stat_type)
        print(teams, players)

        
        if comparison == 'single':
            fig = generate_single_player_radar(player, stat_type, league, season)
        elif comparison == 'compare':
            player2 = request.form.get('player2')
            fig = generate_comparison_radar(player, player2, stat_type, league, season)
            player1, player2, stat_type, league1, league2, season1, season2 = player1, player2, stat_type, league1, league2, season1, season2

        image_path=fig
        # # Save radar chart image
        # image_path = os.path.join('static', 'radar_chart.png')
        # fig.savefig(image_path)
        # plt.close(fig)

        return render_template('main_interface.html', image_path=image_path, teams=teams, players=players)
        


def generate_single_player_radar(player, stat_type, league, season):
    # Determine which stat type function to call based on the selected stat_type
    print("check")
    
    if stat_type == "Keeper":
        file_path = file_paths[league]
        selected_league = league
        selected_stat_type = stat_type
        selected_player = player
        selected_season = season


        data1 = pd.read_excel(file_path, sheet_name=selected_stat_type, engine='openpyxl')

        player1_data = data1[(data1['Player'] == selected_player) & (data1['Season'] == selected_season)]

        # Extract unique team name for the selected player and season
        selected_team = data1[(data1['Player'] == selected_player) & (data1['Season'] == selected_season)]['Squad'].unique()[0]

        stats = player1_data[['90s', 'GA90', 'Save%', 'CS%', 'PKatt', 'PKSave%']]

        # Custom range values for each parameter
        ranges = [(3.4, 38), (0.48, 3.75), (26.7, 92), (0, 80), (0, 15), (0, 100)]

        # Parameter names
        params = stats.columns.tolist()
        # print(stats.iloc)

        # Parameter values as a list
        values = stats.iloc[0].tolist()

        # Title values
        title = dict(
            title_name=selected_player,
            title_color="#E3DDED",
            subtitle_name=f"{selected_team} - {selected_season}",
            subtitle_color="#FC2128",
            title_name_2="Radar Chart",
            title_color_2="#E3DDED",
            subtitle_name_2=selected_stat_type,
            subtitle_color_2='#FC2128',
            title_fontsize=18,
            subtitle_fontsize=15
        )

        # Endnote
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nKEEPER RADAR CHART\n90s = Minutes played divided by 90\nGA90 = Goals Against per 90 min\nSave% = Shots Save percentage\nCS% = Clean Sheet percentage\nPKatt = Penalty Kicks attempted\nPKSave% = Penalty Kick save percentage"
        # Instantiate object -- fontfamily
        radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#BFE9BF", range_color="#BFE9BF", range_fontsize=7.5, label_fontsize=13)

        # Plot radar with improved layout
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=['#0f4c75', '#e94560'], 
                                title=title, endnote=endnote, dpi=500)  


        # Save the radar plot to a file
        image_path = os.path.join('static', f'radar_plot_{selected_player}_{selected_stat_type}.png')
        fig.savefig(image_path)
        plt.close(fig)  # Close the plot to release resources

        return image_path

    

    elif stat_type == "Shooting":
        file_path = file_paths[league]
        selected_league = league
        selected_stat_type = stat_type
        selected_player = player  
        selected_season = season

        data1 = pd.read_excel(file_path, sheet_name=selected_stat_type, engine='openpyxl')

        player1_data = data1[(data1['Player'] == selected_player) & (data1['Season'] == selected_season)]

        # Extract unique team name for the selected player and season
        selected_team = data1[(data1['Player'] == selected_player) & (data1['Season'] == selected_season)]['Squad'].unique()[0]

        stats = player1_data[['90s', 'Gls', 'Sh/90', 'SoT%', 'xG', 'npxG', 'G-xG', 'PK']]

        # Custom range values for each parameter
        ranges = [(0, 38), (0, 41), (0, 45), (0, 100), (0, 33.2), (0, 29.3), (-8.7, 12.2), (0, 14)]

        # Parameter names
        params = stats.columns.tolist()

        # Parameter values as a list
        values = stats.iloc[0].tolist()

        # Title values
        title = dict(
            title_name=selected_player,
            title_color="#E3DDED",
            subtitle_name=f"{selected_team} - {selected_season}",
            subtitle_color="#FC2128",
            title_name_2="Radar Chart",
            title_color_2="#E3DDED",
            subtitle_name_2=selected_stat_type,
            subtitle_color_2='#FC2128',
            title_fontsize=18,
            subtitle_fontsize=15
        )

        # Endnote
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nSHOOTING RADAR CHART\n90s = Minutes played divided by 90\nGls = Goals Scored\nSh/90 = Total Shots per 90\nSoT% = Shots on Target %\nxG = Expected Goals\nnpxG = Non Penalty Expected Goals\nG-xG = Goals minus Expected Goals\nPK = Penalties Won or Made"

        # Instantiate object -- fontfamily
        radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#BFE9BF", range_color="#BFE9BF", range_fontsize=7.5, label_fontsize=13)

        # Plot radar with improved layout
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=['#0f4c75', '#e94560'], 
                                title=title, endnote=endnote, dpi=500)


        # Save the radar plot to a file
        image_path = os.path.join('static', f'radar_plot_{selected_player}_{selected_stat_type}.png')
        fig.savefig(image_path)
        plt.close(fig)  # Close the plot to release resources

        return image_path 



    elif stat_type == "Passing":
        file_path = file_paths[league]
        selected_league = league
        selected_stat_type = stat_type
        selected_player = player  
        selected_season = season

        data1 = pd.read_excel(file_path, sheet_name=selected_stat_type, engine='openpyxl')

        player1_data = data1[(data1['Player'] == selected_player) & (data1['Season'] == selected_season)]

        # Extract unique team name for the selected player and season
        selected_team = data1[(data1['Player'] == selected_player) & (data1['Season'] == selected_season)]['Squad'].unique()[0]

        stats = player1_data[['90s', 'Cmp', 'Cmp%', 'PrgDist', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'CrsPA', 'PrgP']]

        # Custom range values for each parameter
        ranges = [(0, 38), (0, 3000), (0, 100), (0, 38000), (0, 24), (0, 20), (0, 18), (-9, 9), (0, 140), (0, 380), (0, 60), (0, 380)]

        # Parameter names
        params = stats.columns.tolist()

        # Parameter values as a list
        values = stats.iloc[0].tolist()

        # Title values
        title = dict(
            title_name=selected_player,
            title_color="#E3DDED",
            subtitle_name=f"{selected_team} - {selected_season}",
            subtitle_color="#FC2128",
            title_name_2="Radar Chart",
            title_color_2="#E3DDED",
            subtitle_name_2=selected_stat_type,
            subtitle_color_2='#FC2128',
            title_fontsize=18,
            subtitle_fontsize=15
        )

        # Endnote
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nPASSING RADAR CHART\n90s = Minutes played divided by 90\nCmp = Passes Completed\nCmp% = Pass Completion %\nPrgDist = Progressive Passing Distance\nAst = Assist\nxAG = Expected Goals Assisted\nxA = Expected Assists\nA-xAG = Assists minus Expected Goals Assisted\nKP = Key Passes\n1/3 = Passes into Final 3rd\nCrsPA = Croses into Penalty Area\nPrgP = Progressive Passes"

        # Instantiate object -- fontfamily
        radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#BFE9BF", range_color="#BFE9BF", range_fontsize=7.5, label_fontsize=13)

        # Plot radar with improved layout
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=['#0f4c75', '#e94560'], 
                                title=title, endnote=endnote, dpi=500)


        # Save the radar plot to a file
        image_path = os.path.join('static', f'radar_plot_{selected_player}_{selected_stat_type}.png')
        fig.savefig(image_path)
        plt.close(fig)  # Close the plot to release resources

        return image_path 
    


    elif stat_type == "Defense":
        file_path = file_paths[league]
        selected_league = league
        selected_stat_type = stat_type
        selected_player = player  
        selected_season = season

        data1 = pd.read_excel(file_path, sheet_name=selected_stat_type, engine='openpyxl')

        player1_data = data1[(data1['Player'] == selected_player) & (data1['Season'] == selected_season)]

        # Extract unique team name for the selected player and season
        selected_team = data1[(data1['Player'] == selected_player) & (data1['Season'] == selected_season)]['Squad'].unique()[0]

        stats = player1_data[['90s', 'Tkl', 'Tkl%', 'DrTkl', 'DrTkl%', 'Blocks', 'Int', 'Clr', 'Err']]

        # Custom range values for each parameter
        ranges = [(0, 38), (0, 150), (0, 100), (0, 80), (0, 100), (0, 100), (0, 120), (0, 250), (0, 15)]

        # Parameter names
        params = stats.columns.tolist()

        # Parameter values as a list
        values = stats.iloc[0].tolist()

        # Title values
        title = dict(
            title_name=selected_player,
            title_color="#E3DDED",
            subtitle_name=f"{selected_team} - {selected_season}",
            subtitle_color="#FC2128",
            title_name_2="Radar Chart",
            title_color_2="#E3DDED",
            subtitle_name_2=selected_stat_type,
            subtitle_color_2='#FC2128',
            title_fontsize=18,
            subtitle_fontsize=15
        )

        # Endnote
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nDEFENDING RADAR CHART\n90s = Minutes played divided by 90\nTkl = Tackles made\nTkl% = Tackle Success %\nDrTkl = Dribblers Tackled\nDrTkl% = Dribblers Tackled Success %\nBlocks = No. of times Ball Blocked\nInt = Interceptions\nClr = Clearances\nErr = Errors"

        # Instantiate object -- fontfamily
        radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#BFE9BF", range_color="#BFE9BF", range_fontsize=7.5, label_fontsize=13)

        # Plot radar with improved layout
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=['#0f4c75', '#e94560'],
                                title=title, endnote=endnote, dpi=500)


        # Save the radar plot to a file
        image_path = os.path.join('static', f'radar_plot_{selected_player}_{selected_stat_type}.png')
        fig.savefig(image_path)
        plt.close(fig)  # Close the plot to release resources

        return image_path 
    

    else:
        # Handle unsupported stat type here
        image_path = None


    


def generate_comparison_radar(player1, player2, stat_type, league1, league2, season1, season2):
    # Determine which stat type function to call based on the selected stat_type
    if stat_type == "Keeper":
        file_path_player1 = file_paths[league1]
        file_path_player2 = file_paths[league2]

        selected_league1 = league1
        selected_league2 = league2
        selected_stat_type = stat_type
        selected_player1 = player1
        selected_player2 = player2
        selected_season1 = season1
        selected_season2 = season2

        data1 = pd.read_excel(file_path_player1, sheet_name=selected_stat_type, engine='openpyxl')
        data2 = pd.read_excel(file_path_player2, sheet_name=selected_stat_type, engine='openpyxl')


        player1_data = data1[(data1['Player'] == selected_player1) & (data1['Season'] == selected_season1)]
        player2_data = data2[(data2['Player'] == selected_player2) & (data2['Season'] == selected_season2)]

        # Extract unique team name for the selected player and season
        selected_team1 = data1[(data1['Player'] == selected_player1) & (data1['Season'] == selected_season1)]['Squad'].unique()[0]
        selected_team2 = data2[(data2['Player'] == selected_player2) & (data1['Season'] == selected_season2)]['Squad'].unique()[0]

        stats1 = player1_data[['90s', 'GA90', 'Save%', 'CS%', 'PKatt', 'PKSave%']]
        stats2 = player2_data[['90s', 'GA90', 'Save%', 'CS%', 'PKatt', 'PKSave%']]

        # Custom range values for each parameter
        ranges = [(3.4, 38), (0.48, 3.75), (26.7, 92), (0, 80), (0, 15), (0, 100)]


        # Parameter names
        params = stats1.columns.tolist()

        # Parameter values as a list
        values1 = stats1.iloc[0].tolist()
        values2 = stats2.iloc[0].tolist()

        values = [values1, values2]

        # Title values
        title = dict(
            title_name=selected_player1,
            title_color="#E3DDED",
            subtitle_name=f"{selected_team1} - {selected_season1}",
            subtitle_color="#FC2128",
            title_name_2=selected_player2,
            title_color_2="#E3DDED",
            subtitle_name_2=f"{selected_team2} - {selected_season2}",
            subtitle_color_2='#FC2128',
            title_fontsize=18,
            subtitle_fontsize=15
        )

        # Endnote
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nKEEPER RADAR CHART\n90s = Minutes played divided by 90\nGA90 = Goals Against per 90 min\nSave% = Shots Save percentage\nCS% = Clean Sheet percentage\nPKatt = Penalty Kicks attempted\nPKSave% = Penalty Kick save percentage"

        # Instantiate object
        radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#F0FFF0",
                range_color="#F0FFF0", range_fontsize=8, label_fontsize=12)
        
        # Plot radar with improved layout
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=[values1, values2], radar_color=['#f70029', '#0594f5'],
                    title=title, endnote=endnote, alphas=[0.5, 0.4], dpi=500, compare=True)

        # Save the radar plot to a file
        image_path = os.path.join('static', f'radar_plot_{selected_player1}_{selected_player2}_{selected_stat_type}.png')
        fig.savefig(image_path)
        plt.close(fig)  # Close the plot to release resources

        return image_path
    


    elif stat_type == "Shooting":
        file_path_player1 = file_paths[league1]
        file_path_player2 = file_paths[league2]

        selected_league1 = league1
        selected_league2 = league2
        selected_stat_type = stat_type
        selected_player1 = player1
        selected_player2 = player2
        selected_season1 = season1
        selected_season2 = season2

        data1 = pd.read_excel(file_path_player1, sheet_name=selected_stat_type, engine='openpyxl')
        data2 = pd.read_excel(file_path_player2, sheet_name=selected_stat_type, engine='openpyxl')


        player1_data = data1[(data1['Player'] == selected_player1) & (data1['Season'] == selected_season1)]
        player2_data = data2[(data2['Player'] == selected_player2) & (data2['Season'] == selected_season2)]

        # Extract unique team name for the selected player and season
        selected_team1 = data1[(data1['Player'] == selected_player1) & (data1['Season'] == selected_season1)]['Squad'].unique()[0]
        selected_team2 = data2[(data2['Player'] == selected_player2) & (data1['Season'] == selected_season2)]['Squad'].unique()[0]

        stats1 = player1_data[['90s', 'Gls', 'Sh/90', 'SoT%', 'xG', 'npxG', 'G-xG', 'PK']]
        stats2 = player2_data[['90s', 'Gls', 'Sh/90', 'SoT%', 'xG', 'npxG', 'G-xG', 'PK']]

        # Custom range values for each parameter
        ranges = [(0, 38), (0, 41), (0, 45), (0, 100), (0, 33.2), (0, 29.3), (-8.7, 12.2), (0, 14)]


        # Parameter names
        params = stats1.columns.tolist()

        # Parameter values as a list
        values1 = stats1.iloc[0].tolist()
        values2 = stats2.iloc[0].tolist()

        # Title values
        title = dict(
            title_name=selected_player1,
            title_color="#E3DDED",
            subtitle_name=f"{selected_team1} - {selected_season1}",
            subtitle_color="#FC2128",
            title_name_2=selected_player2,
            title_color_2="#E3DDED",
            subtitle_name_2=f"{selected_team2} - {selected_season2}",
            subtitle_color_2='#FC2128',
            title_fontsize=18,
            subtitle_fontsize=15
        )

        # Endnote
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nSHOOTING RADAR CHART\n90s = Minutes played divided by 90\nGls = Goals Scored\nSh/90 = Total Shots per 90\nSoT% = Shots on Target %\nxG = Expected Goals\nnpxG = Non Penalty Expected Goals\nG-xG = Goals minus Expected Goals\nPK = Penalties Won or Made"


        # Instantiate object
        radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#F0FFF0",
                range_color="#F0FFF0", range_fontsize=8, label_fontsize=12)
        
        # Plot radar with improved layout
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=[values1, values2], radar_color=['#f70029', '#0594f5'],
                    title=title, endnote=endnote, alphas=[0.5, 0.4], dpi=500, compare=True)

        # Save the radar plot to a file
        image_path = os.path.join('static', f'radar_plot_{selected_player1}_{selected_player2}_{selected_stat_type}.png')
        fig.savefig(image_path)
        plt.close(fig)  # Close the plot to release resources

        return image_path
    


    elif stat_type == "Passing":
        file_path_player1 = file_paths[league1]
        file_path_player2 = file_paths[league2]

        selected_league1 = league1
        selected_league2 = league2
        selected_stat_type = stat_type
        selected_player1 = player1
        selected_player2 = player2
        selected_season1 = season1
        selected_season2 = season2

        data1 = pd.read_excel(file_path_player1, sheet_name=selected_stat_type, engine='openpyxl')
        data2 = pd.read_excel(file_path_player2, sheet_name=selected_stat_type, engine='openpyxl')


        player1_data = data1[(data1['Player'] == selected_player1) & (data1['Season'] == selected_season1)]
        player2_data = data2[(data2['Player'] == selected_player2) & (data2['Season'] == selected_season2)]

        # Extract unique team name for the selected player and season
        selected_team1 = data1[(data1['Player'] == selected_player1) & (data1['Season'] == selected_season1)]['Squad'].unique()[0]
        selected_team2 = data2[(data2['Player'] == selected_player2) & (data1['Season'] == selected_season2)]['Squad'].unique()[0]

        stats1 = player1_data[['90s', 'Cmp', 'Cmp%', 'PrgDist', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'CrsPA', 'PrgP']]
        stats2 = player2_data[['90s', 'Cmp', 'Cmp%', 'PrgDist', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'CrsPA', 'PrgP']]

        # Custom range values for each parameter
        ranges = [(0, 38), (0, 3000), (0, 100), (0, 38000), (0, 24), (0, 20), (0, 18), (-9, 9), (0, 140), (0, 380), (0, 60), (0, 380)]


        # Parameter names
        params = stats1.columns.tolist()

        # Parameter values as a list
        values1 = stats1.iloc[0].tolist()
        values2 = stats2.iloc[0].tolist()

        # Title values
        title = dict(
            title_name=selected_player1,
            title_color="#E3DDED",
            subtitle_name=f"{selected_team1} - {selected_season1}",
            subtitle_color="#FC2128",
            title_name_2=selected_player2,
            title_color_2="#E3DDED",
            subtitle_name_2=f"{selected_team2} - {selected_season2}",
            subtitle_color_2='#FC2128',
            title_fontsize=18,
            subtitle_fontsize=15
        )

        # Endnote
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nPASSING RADAR CHART\n90s = Minutes played divided by 90\nCmp = Passes Completed\nCmp% = Pass Completion %\nPrgDist = Progressive Passing Distance\nAst = Assist\nxAG = Expected Goals Assisted\nxA = Expected Assists\nA-xAG = Assists minus Expected Goals Assisted\nKP = Key Passes\n1/3 = Passes into Final 3rd\nCrsPA = Croses into Penalty Area\nPrgP = Progressive Passes"

        # Instantiate object
        radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#F0FFF0",
                range_color="#F0FFF0", range_fontsize=8, label_fontsize=12)
        
        # Plot radar with improved layout
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=[values1, values2], radar_color=['#f70029', '#0594f5'],
                    title=title, endnote=endnote, alphas=[0.5, 0.4], dpi=500, compare=True)

        # Save the radar plot to a file
        image_path = os.path.join('static', f'radar_plot_{selected_player1}_{selected_player2}_{selected_stat_type}.png')
        fig.savefig(image_path)
        plt.close(fig)  # Close the plot to release resources

        return image_path
    


    elif stat_type == "Defense":
        file_path_player1 = file_paths[league1]
        file_path_player2 = file_paths[league2]

        selected_league1 = league1
        selected_league2 = league2
        selected_stat_type = stat_type
        selected_player1 = player1
        selected_player2 = player2
        selected_season1 = season1
        selected_season2 = season2

        data1 = pd.read_excel(file_path_player1, sheet_name=selected_stat_type, engine='openpyxl')
        data2 = pd.read_excel(file_path_player2, sheet_name=selected_stat_type, engine='openpyxl')


        player1_data = data1[(data1['Player'] == selected_player1) & (data1['Season'] == selected_season1)]
        player2_data = data2[(data2['Player'] == selected_player2) & (data2['Season'] == selected_season2)]

        # Extract unique team name for the selected player and season
        selected_team1 = data1[(data1['Player'] == selected_player1) & (data1['Season'] == selected_season1)]['Squad'].unique()[0]
        selected_team2 = data2[(data2['Player'] == selected_player2) & (data1['Season'] == selected_season2)]['Squad'].unique()[0]

        stats1 = player1_data[['90s', 'Tkl', 'Tkl%', 'DrTkl', 'DrTkl%', 'Blocks', 'Int', 'Clr', 'Err']]
        stats2 = player2_data[['90s', 'Tkl', 'Tkl%', 'DrTkl', 'DrTkl%', 'Blocks', 'Int', 'Clr', 'Err']]

        # Custom range values for each parameter
        ranges = [(0, 38), (0, 150), (0, 100), (0, 80), (0, 100), (0, 100), (0, 120), (0, 250), (0, 15)]


        # Parameter names
        params = stats1.columns.tolist()

        # Parameter values as a list
        values1 = stats1.iloc[0].tolist()
        values2 = stats2.iloc[0].tolist()

        # Title values
        title = dict(
            title_name=selected_player1,
            title_color="#E3DDED",
            subtitle_name=f"{selected_team1} - {selected_season1}",
            subtitle_color="#FC2128",
            title_name_2=selected_player2,
            title_color_2="#E3DDED",
            subtitle_name_2=f"{selected_team2} - {selected_season2}",
            subtitle_color_2='#FC2128',
            title_fontsize=18,
            subtitle_fontsize=15
        )

        # Endnote
        endnote = "Visualization made by: Aditya Khare (@AdityaK194)\nCredits: Anmol Durgapal (@slothfulwave612)\n\nDEFENDING RADAR CHART\n90s = Minutes played divided by 90\nTkl = Tackles made\nTkl% = Tackle Success %\nDrTkl = Dribblers Tackled\nDrTkl% = Dribblers Tackled Success %\nBlocks = No. of times Ball Blocked\nInt = Interceptions\nClr = Clearances\nErr = Errors"

        # Instantiate object
        radar = Radar(fontfamily="Franklin Gothic Medium", background_color="#121212", patch_color="#28252C", label_color="#F0FFF0",
                range_color="#F0FFF0", range_fontsize=8, label_fontsize=12)
        
        # Plot radar with improved layout
        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=[values1, values2], radar_color=['#f70029', '#0594f5'],
                    title=title, endnote=endnote, alphas=[0.5, 0.4], dpi=500, compare=True)

        # Save the radar plot to a file
        image_path = os.path.join('static', f'radar_plot_{selected_player1}_{selected_player2}_{selected_stat_type}.png')
        fig.savefig(image_path)
        plt.close(fig)  # Close the plot to release resources

        return image_path
    


    else:
        # Handle unsupported stat type here
        fig = None

    return fig
    # Code to generate radar chart for player comparison
    # Modify this code based on your requirements
    radar = Radar()
    # Generate the radar chart and return the figure

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input values from the form
        stat_type = request.form['stat_type']
        league = request.form['league']
        season = request.form['season']
        
        # Call read_data function to get teams and players
        file_path = "SERIA_ALL.xlsx"  # Update with your file path
        teams, players = read_data(file_path, season, stat_type, league)
        
        return render_template("main_interface.html", teams=teams, players=players, league=league)
    else:
        return render_template("main_interface.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
