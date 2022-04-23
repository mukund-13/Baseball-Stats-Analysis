import pandas as pd
import requests
import sqlite3


#I have made the code into two parts
#The first part deals with fetching the data from an API and flattening it 
#to store it into a dataframe using pandas

#Part 1
# url = "https://baseballsavant.mlb.com/gf?game_pk=635886" # Adress for the API
def BaseballData(game_pk,path = "https://baseballsavant.mlb.com/gf?game_pk=635886"):
    jsonData = requests.get(path).json() # Get data from the api that is in JSON format

    #The following loop adds data from the api to an array. The data needed to be flattened as it was heavily nested
    pitchers = []
    for home_away in ['home', 'away']:
        for x in jsonData[f'{home_away}_pitchers'].values():
            pitchers += x
        
    pitchers_df = pd.DataFrame(pitchers) # Convert to dataframe

    #These are the column values that will be present in the table created
    cols = ['play_id','inning','ab_number','outs','stand','batter_name','p_throws',
            'pitcher_name','team_batting','team_fielding','result','strikes',
            'balls','pre_strikes','pre_balls','call_name','pitch_type','start_speed',
            'extension','zone','spin_rate','hit_speed','hit_distance','hit_angle',
            'is_barrel','is_bip_out','pitch_number','player_total_pitches',
            'game_pk']

    pitchers_df = pitchers_df[cols] #Add the columns to the dataframe

    #Part 2
    #The next lines would work with sqlite
    conn = sqlite3.connect('pitch.db') #Create a database called pitch
    pitchers_df.to_sql('pitch', conn, dtype={'play_id': ' PRIMARY KEY'}, if_exists='replace',  index=False)# Add the dataframe to our database 
    #with play_id as the primary key
    cursor = conn.cursor()

    #The following loop will prompt the user to enter a query
    #If an error is encountered, the user shall try again
    #The program will only terminate when the user inputs "stop"
    x = ""
    while x != "stop":
        try:
            x = input("Enter a query (type stop to stop executing): ") #Enter the query here
            if x == "stop":
                cursor.execute('''select count(pitch_number) from pitch ''') #execute and display the output
                print(cursor.fetchall())
                break
            cursor.execute(x) #execute and display the output
            print(cursor.fetchall())
        except:
            print("Error, try again")

    conn.close()

game_pk = input("Enter game_pk value: ")
# path = input("Give path: ")
BaseballData(game_pk, path = "https://baseballsavant.mlb.com/gf?game_pk=635886")
