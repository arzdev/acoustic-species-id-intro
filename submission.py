# Acoustic Species Identification Intro
# Ali Zaidi
# Date 4/19/2021

import pandas as pd

# input: csv path, new stratified file name
# output: true/false if stratified csv file was successful
def stratified_random_sampler(original_path, new_stratified_name):
    try:
        csv_df = pd.read_csv(original_path)

        # Remove any short Durations (minute long clips)
        csv_df.drop(csv_df[~(csv_df.Duration > 60)].index, inplace=True)

        # create a temporary col for Hour Time
        csv_df.loc[:, 'Temp-Hour'] = csv_df['Comment'].str.split(" ").str[2] # ex: Recorded at 14:56:49 16/06/2019 ... -> 14:56:49
        # remove min
        csv_df.loc[:, 'Temp-Hour']= csv_df['Temp-Hour'].str.split(':').str[0] # ex: 14:56:49 -> 14

        grouped = csv_df.groupby(["AudioMothCode", "Temp-Hour"])  # group for second strata layer 

        indices = [] # random indices for each hour (0-23) for an AudioMothCode
        for row in grouped:
            indices.append(int(row[1].sample().index.values)) # pick one random hour

        csv_df = csv_df.loc[indices]  # keep only random hours
        csv_df.drop('Temp-Hour', axis=1, inplace=True)
        # Remove any Audiomoth device without enough clips (less than 24)
        csv_df = csv_df.groupby('AudioMothCode').filter(lambda x: len(x) == 24)

        # save stratified data
        csv_df.to_csv(str(new_stratified_name), index=False)
        
        return True
    
    except BaseException as e:
        print('An exception occurred: {}'.format(e))
        return False


stratified_random_sampler("", "stratified_data.csv")  # add csv path file


