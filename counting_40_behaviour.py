import pandas as pd
import numpy as np

def count_40_in_status(age, status):
    '''
    The function reads: 1) Storks data according to the specific age and status.
                        2) Time boundaries of each stroke in which we look for behaviour 40

    Per each stroke the function counts rows inside the time boundaries and where the behavior is 40 as well.
    All counting amount normalized to percentages (of all strokes) is saved as csv file in 40Percentages dir.


    :param age: 'adult'/'juvenile'
    :param status: 'migration_to_africa'/'migration_to_europe'/'nesting'/'wintering'
    :return: None
    '''

    # Reading the raw data and creating timestamps as the dataframe index
    data = pd.read_csv('RawData/' + age + '.csv')
    data['Timestamp'] = pd.to_datetime(data['date'].astype(str) + ' ' + data['time'].astype(str))
    data.set_index('Timestamp', inplace=True)

    # Reading the time boundaries of all storks in which we look for behaviour 40
    all_from_to = pd.read_csv('TimeBoundaries/' + age + '/' + status + '.csv')

    all_id = np.unique(data['research_ID'].values) # All storks id number
    all_40_percent = [] # All birds counting of behaviour 40 in the specific status
    for id in all_id: # for each stork id
        id_data = data[data['research_ID']==id] # All of the data of the id

        # Specific status boundaries time of the id. It might be more than a single row! That's why we loop it in the
        # following rows
        id_from_to = all_from_to[all_from_to['research_ID'] == id]

        total_count_40 = 0 # Amount of behaviour 40 inside the time boundaries
        total_count_behviour = 0 # Amount of all data inside the time boundaries

        # For each row in the specific status boundaries time of the id - (most of the time it's only one iteration)
        for index, row in id_from_to.iterrows():
            # Getting the boundaries of the times
            from_ = pd.to_datetime(row['date from'] + ' ' + row['hour from'], dayfirst=True)
            to_ = pd.to_datetime(row['date to'] + ' ' + row['hour to'], dayfirst=True)

            # Counting the number of time with behaviour2 = 40
            is_40 = id_data['behaviour2'][from_:to_] == 40
            count_40 = is_40.sum()
            total_count_40 += count_40

            total_count_behviour += len(id_data['behaviour2'][from_:to_])

        # Normalizing to percentages
        if total_count_behviour != 0:
            all_40_percent.append(100 * total_count_40 / total_count_behviour)
        else:
            all_40_percent.append(np.nan)

    pd.DataFrame(all_40_percent, index=all_id).to_csv('40Percentages/' + age + '/' + status + '.csv')

# Calling the function for each age and status
for age in ['Adults','Juveniles']:
    for status in ['migration_to_africa','migration_to_europe','nesting','wintering']:
        count_40_in_status(age, status)