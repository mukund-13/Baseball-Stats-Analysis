import pandas as pd
import requests
import sqlite3

url = "https://baseballsavant.mlb.com/gf?game_pk=635886"
jsonData = requests.get(url).json()

pitchers = []
for home_away in ['home', 'away']:
    for x in jsonData[f'{home_away}_pitchers'].values():
        pitchers += x
    
pitchers_df = pd.DataFrame(pitchers)
cols = ['play_id','inning','ab_number','outs','stand','batter_name','p_throws',
        'pitcher_name','team_batting','team_fielding','result','strikes',
        'balls','pre_strikes','pre_balls','call_name','pitch_type','start_speed',
        'extension','zone','spin_rate','hit_speed','hit_distance','hit_angle',
        'is_barrel','is_bip_out','pitch_number','player_total_pitches',
        'game_pk']
pitchers_df = pitchers_df[cols]

conn = sqlite3.connect('pitch.db')
pitchers_df.to_sql('pitch', conn, dtype={'play_id': ' PRIMARY KEY'}, if_exists='replace',  index=False)
cursor = conn.cursor()
x = ""
while x != "stop":
    try:
        x = input("Enter a query (type stop to stop executing): ")
        if x == "stop":
            break
        cursor.execute(x) 
        print(cursor.fetchall())
    except:
        print("Error, try again")

conn.close()