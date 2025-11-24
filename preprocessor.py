import pandas as pd

def preprocess(df, region_df):
        
    # filtering for summer olympics
    df = df[df["Season"] == "Summer"] 
    # merge with region_df
    df = df.merge(region_df,on="NOC",how="left")
    # dropping duplicates 
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = df.join(pd.get_dummies(df["Medal"]).astype(int))

    return df

