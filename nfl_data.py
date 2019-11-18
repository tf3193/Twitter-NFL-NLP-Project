import rpy2.robjects as robj
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import pandas as pd
import matplotlib.pyplot as plt

pandas2ri.activate()
nfl_scrap_r = importr("nflscrapR")

def get_game_id(home_team, week, year=2019):
    sched_df = nfl_scrap_r.scrape_game_ids(year, weeks=week)
    return sched_df.loc[sched_df['home_team'] == home_team].iloc[0]['game_id']

def get_game_play_by_play(game_id):
    return nfl_scrap_r.scrape_json_play_by_play(game_id)

def get_win_percentage_df(game_id):
    df_wp = get_game_play_by_play(game_id)
    return df_wp[['game_seconds_remaining', 'home_wp', 'away_wp']]

def plot_wp(df_wp, team):
    if not (team in ['home', 'away']):
        return None

    y_val = f"{team}_wp"
    time = df_wp['game_seconds_remaining']
    wp = df_wp[y_val]

    plt.plot(time, wp, 'b')
    plt.title(f'{team} win percentage')
    plt.xlim(3600, 0)
    plt.ylim(0, 1)
    plt.show()



