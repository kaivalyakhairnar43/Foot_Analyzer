from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def read_data(file_path):
    try:
        # Read data from the CSV file into a pandas DataFrame
        data = pd.read_csv(file_path)
        return data['Squad'].unique().tolist(), data['Player'].unique().tolist()
    except FileNotFoundError:
        return [], []

@app.route('/')
def index():
    # File path for the provided CSV file
    file_path = "SERIA_ALL.xlsx"  # Ensure this CSV file is properly formatted

    # Call the function to read data from the CSV file
    teams, players = read_data(file_path)

    return render_template('main_interface.html', teams=teams, players=players)

if __name__ == '__main__':
    app.run(debug=True)