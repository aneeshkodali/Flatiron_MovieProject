import pandas as pd


def cleanMovieTitles(dataframe, column, patternList):
    '''
    Args
        - dataframe
        - column
        - patternList = list of text patterns
    
    Performs text cleaning on a movie title column
    '''

    for pattern in patternList:
        # If colon in list
        if pattern==':':
            dataframe[column] = dataframe[column].str.split(':').str[0]
        else:
            dataframe[column] = dataframe[column].str.replace(pattern, '').str.rstrip()

    return dataframe



def findDuplicateMovies(dataframe, duplicateColumnList, duplicateMovieValue):
    '''
    Args
        - dataframe
        - duplicateColumn = list of columns on which duplicate data can be found
        - duplicateValue = value that is duplicated
    Finds duplicate rows and adds information'''

    # Initialize dataframe
    dupeDF = pd.DataFrame()
    # Iterate through each column
    for column in duplicateColumnList:
        # Filter dataframe
        df = dataframe.loc[dataframe[column]==duplicateMovieValue]
        # Concatenate dataframe
        dupeDF = pd.concat([dupeDF, df])
    
    # Remove duplicate rows
    dupeDF.drop_duplicates(inplace=True)
    return dupeDF


def dropDuplicateMovieRows(dupeDataframe, columnList):
    '''
    Args
        - dupeDataFrame = dataframe of duplicate data
        - column list = list of columns for which information is preserved
    Returns
        dataframe with duplicates removed, 
        but copies of columns are created that contain 
        list of unique values from duplicate data
    '''
    
    # Iterate through columns
    for column in columnList:

        # Special case for 'genre' column
        if column=='genres':
            
            # Get list of unique genres, filtering out na values
            uniqueGenres = list(dupeDataframe['genres'])
            uniqueGenres = [x for x in uniqueGenres if str(x) != 'nan']
            uniqueGenres = [x.split(',') for x in uniqueGenres]
            uniqueGenres = list(set([y for x in uniqueGenres for y in x]))
            dupeDataframe['genresOthers'] = dupeDataframe['genres'].apply(lambda x: uniqueGenres)
        
        else:
            uniqueValues = list(set(dupeDataframe[column]))
            uniqueValues = [x for x in uniqueValues if str(x)!='nan']
            dupeDataframe[column+'Others'] = dupeDataframe[column].apply(lambda x: uniqueValues)

    
    # Drop duplicate rows
    dupeDataframe = pd.DataFrame(dupeDataframe.iloc[0]).T
    return dupeDataframe
    