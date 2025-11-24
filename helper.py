import pandas as pd 
import numpy as np


def fetch_medal_tally(df,year,country):

    medal_df = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])   
    
    temp_df = medal_df.copy()
    
    # filter by year if user select specific year
    if year != "Overall":
        temp_df = temp_df[temp_df["Year"] == int(year)]

    # filter by country if user selected specific country
    if country != "Overall":
        temp_df = temp_df[temp_df["region"] == country]

    # case 1: user select a specific country -> show year-wise medals
    if country != "Overall":
        group_col = "Year"
    else:
        # case 2: country = Overall -> group by country (region)
        group_col = "region"
        
    # group by country and sum medals 
    x = (temp_df.groupby(group_col)[["Gold", "Silver", "Bronze"]]
                  .sum()
                  .sort_values("Gold",ascending = False)        
                  .reset_index())

    x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]
    return x

def medal_tally(df):
    
    ## we drop duplicated row as medal distribute to all members ofv the team we simplay drop duplictes rows
    medal_tally = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])   
    medal_tally = medal_tally.groupby("region").sum()[["Gold","Silver","Bronze"]].sort_values("Gold",ascending=False).reset_index()

    medal_tally["total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]

    return medal_tally

def country_year_list(df):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0,"Overall")

    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0,"Overall")

    return years , country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(["Year",col])["Year"].value_counts().reset_index().sort_values("Year")
    nations_over_time.rename(columns={"Year" : "Edition" ,"count" : col },inplace=True)
    return nations_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    x = temp_df["Name"].value_counts().reset_index()
    x.columns = ["Name", "Medals"]
    
    y = x.head(15).merge(df, on="Name",how="left").drop_duplicates("Name")
    
    return y[["Name","Medals","Sport","region"]].reset_index(drop= True)

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"],inplace=True)
    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"]
    final_df = final_df.reset_index()
    final_df.columns = ["Year","Medal"]

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"],inplace=True)
    new_df = temp_df[temp_df["region"] == country]
    pt = new_df.pivot_table(index="Sport",columns= "Year",values="Medal",aggfunc="count").fillna(0)

    return pt

def most_successful_country(df,country):
    temp_df = df.dropna(subset=["Medal"])
    
    temp_df = temp_df[temp_df["region"] == country]

    x = temp_df["Name"].value_counts().reset_index()
    x.columns = ["Name", "Medals"]
    
    y = x.head(10).merge(df, on="Name",how="left").drop_duplicates("Name")
    
    return y[["Name","Medals","Sport"]].reset_index(drop=True)

def  weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=["Name","region"])
    athlete_df["Medal"].fillna("NO Medal", inplace=True)

    if sport != "Overall":
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        return temp_df
    else:
        return athlete_df
 
def  men_vs_womenv(df):
    athlete_df = df.drop_duplicates(subset=["Name","region"])

    men = athlete_df[athlete_df["Sex"] == "M"].groupby("Year").count()["Name"].reset_index()
    women = athlete_df[athlete_df["Sex"] == "F"].groupby("Year").count()["Name"].reset_index()
    final = men.merge(women,on="Year",how="left")
    final.rename(columns={"Name_x":"Male","Name_y":"Female"},inplace=True)
    final.fillna(0,inplace=True)

    return final