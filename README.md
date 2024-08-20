FootAnalyzer Overview FootAnalyzer is an interactive football analytics dashboard built using Dash. This application allows users to analyze in-depth player profile statistics from various football leagues and seasons. Users can generate radar charts for individual players or compare two players based on their performance in different statistical categories.

Features Individual Player Analysis: Generate radar charts for individual players based on their performance in specific stat categories. Player Comparison: Compare two players from different leagues and seasons with side-by-side radar charts. Statistical Categories: Analyze players based on categories such as Shooting, Passing, Defense, and Goalkeeping. Interactive Filters: Select leagues, seasons, teams, and players through dropdown menus for a customized analysis experience. Installation

Clone the repository:
[git clone https://github.com/yourusername/Foot_Analyzer.git] [cd Foot_Analyzer]

Create and activate a virtual environment:
[python -m venv env] [source env/bin/activate] # On Windows, use env\Scripts\activate

Install the required packages:
[pip install -r requirements.txt]

Run the app:
[python app.py]

Access the app:
Open your web browser and go to http://127.0.0.1:8050/

Directory Structure

FootAnalyzer/ ├── data/ │ ├── PL_FINAL.xlsm │ ├── LALIGA_FINAL.xlsm │ ├── SERIA_ALL.xlsm │ ├── BUNDESLIGA_ALL.xlsm │ └── LIGUE1_ALL.xlsm ├── app.py ├── requirements.txt ├── README.md └── assets/ └── custom.css Usage Individual Player Analysis

Select 'Individual Player' from the chart type radio buttons.
Select a Stat Type from the dropdown menu (e.g., Shooting, Passing).
Select a League.
Select a Season.
Select a Team.
Select a Player.
The radar chart for the selected player will be displayed.
Player Comparison

Select 'Comparison' from the chart type radio buttons.
For both players: Select a League. Select a Season. Select a Team. Select a Player.
The radar charts for both players will be displayed side-by-side for comparison.
Data Sources The application uses data from Excel files stored in the data directory. Each Excel file contains sheets corresponding to different statistical categories.

Customization The radar charts are generated using the soccerplots library. You can customize the appearance of the charts by modifying the parameters in the generate_single_player_radar and generate_comparison_radar functions in app.py.

Contributing Feel free to fork this repository, make improvements, and submit pull requests. For major changes, please open an issue to discuss what you would like to change.

License This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments: Anmol Durgapal (@slothfulwave612) for the soccerplots library.
