import pandas as pd

def main():
    ##Getting input for season to get ELO for
    kValue = 55
    season = input("Enter Season: ")
    fileName = lambda x: "{}_SEASON_NRL_DATA_v1.1".format(x)

    ##Reading appropriate text files into pandas dataframe
    dfOne = pd.read_csv(fileName(int(season) - 2))
    dfTwo = pd.read_csv(fileName(int(season) - 1))
    dfThree = pd.read_csv(fileName(season))

    ##initialising an elo dictionary
    eloDict = getNewEloDict()
    eloDictOne, accuracy = processSeasonData(dfOne, kValue, eloDict)
    eloDictTwo, accuracy = processSeasonData(dfTwo, kValue, eloDictOne)

    ##getting new dataframe and exporting
    toExport = updateDataframe(dfThree, kValue, eloDictTwo)
    toExport.to_csv('{}_SEASON_NRL_DATA_v1.2'.format(season))




##Function that returns new dictionary with default values
def getNewEloDict():
    eloDict = {
    "Sea Eagles" : 1000,
    "Titans" : 1000,
    "Dolphins" : 1000, ##not in the comp yet for the data that i'm analysing but i'll put it here anyway
    "Rabbitohs" : 1000,
    "Warriors" : 1000,
    "Storm" : 1000,
    "Broncos" : 1000,
    "Cowboys" : 1000,
    "Dragons" : 1000,
    "Raiders" : 1000,
    "Panthers" : 1000,
    "Eels" : 1000,
    "Knights" : 1000,
    "Sharks" : 1000,
    "Roosters" : 1000,
    "Wests Tigers" : 1000,
    "Bulldogs" : 1000
    }
    return eloDict


##This function processes the seasons data, updating elo values and recording the percentage of accuracy of the ELO model
##param df: the dataframe containing the seasons data
##param kValue: a constant
##param eloDict: a dictionary containing the ELO ratings of each team
##
def processSeasonData(df, kValue, eloDict):
    correctCount = 0

    ##Calculation of the expected score of team one playing against team two
    ##param teamOne: ELO rating of team one
    ##param teamTwo: ELO rating of team two
    expectedScore = lambda teamOne, teamTwo : 1/(1+10**((teamTwo - teamOne)/400))

    ##Updated ELO calculation
    ##param oldELO: the teams elo before the match is played
    ##param kValue: a constant
    ##param actualScore: the actual outcome. 1 for a win, 0.5 for a tie, 0 for loss
    ##param expectedScore: the probability of the team winning the match
    updatedELO = lambda oldELO, kValue, actualScore, expectedScore: oldELO + kValue*(actualScore - expectedScore)

    for row in range(len(df)):
        ##getting home team data
        homeTeam = df.loc[row]['Home_Team']
        homeELO = eloDict[homeTeam]
        homeScore = int(df.loc[row]['Home_Score'])

        ##getting away team data
        awayTeam = df.loc[row]['Away_Team']
        awayELO = eloDict[awayTeam]
        awayScore = int(df.loc[row]['Away_Score'])

        ##calculating expected outcomes
        expectedScoreHome = expectedScore(homeELO, awayELO)
        expectedScoreAway = expectedScore(awayELO, homeELO)

        ##creating actual outcome values
        if homeScore == awayScore:
            homeOutcome = 0.5
            awayOutcome = 0.5
        elif homeScore > awayScore:
            homeOutcome = 1
            awayOutcome = 0
        else:
            homeOutcome = 0
            awayOutcome = 1

        ##calculating and updating ELO values
        homeNewELO = updatedELO(homeELO, kValue, homeOutcome, expectedScoreHome)
        awayNewELO = updatedELO(awayELO, kValue, awayOutcome, expectedScoreAway)
        eloDict[homeTeam] = homeNewELO
        eloDict[awayTeam] = awayNewELO

        ##calculating accuracy
        if expectedScoreHome > expectedScoreAway and homeOutcome == 1:
            correctCount += 1
        elif expectedScoreAway > expectedScoreHome and awayOutcome == 1:
            correctCount += 1

    return eloDict, correctCount/len(df)

##This function splits the data from each axis into their own lists
##param list: a list of lists containing a coordinate of kValues and accuracy
##return: returns two lists, one with kValue data and a second with accuracy data
def splitAxisData(list):
    kValueData = [x[0] for x in list]
    accuracyData = [x[1] for x in list]
    return kValueData, accuracyData

##This function takes a dataframe without ELO and adds ELO for home team and away team
##param df: the dataframe that is going to be updated with ELO
##param kValue: a constant
##param eloDict: dictionary that contains the appropriate elo dictionary required for the season
def updateDataframe(df, kValue,  eloDict):
    ##initialsing the header for the new dataframe
    headers = ['Season', 'Round', 'Venue', 'Kick_Off_Time', 
               'Home_Team', 'Home_Score', 'Home_ELO', 'Home_Completion', 'Home_Tackle',
               'Away_Team', 'Away_Score', 'Away_ELO', 'Away_Completion', 'Away_Tackle']
    newDataframe = pd.DataFrame(columns = headers)

    ##Calculation of the expected score of team one playing against team two
    ##param teamOne: ELO rating of team one
    ##param teamTwo: ELO rating of team two
    expectedScore = lambda teamOne, teamTwo : 1/(1+10**((teamTwo - teamOne)/400))

    ##Updated ELO calculation
    ##param oldELO: the teams elo before the match is played
    ##param kValue: a constant
    ##param actualScore: the actual outcome. 1 for a win, 0.5 for a tie, 0 for loss
    ##param expectedScore: the probability of the team winning the match
    updatedELO = lambda oldELO, kValue, actualScore, expectedScore: oldELO + kValue*(actualScore - expectedScore)

    for row in range(len(df)):
        ##inserting ELO into row of data
        season, round, venue, kickOffTime = df.loc[row]['Season'], df.loc[row]['Round'], df.loc[row]['Venue'], df.loc[row]['Kick_Off_Time']
        homeTeam, homeScore, homeCompletion, homeTackle = df.loc[row]['Home_Team'], df.loc[row]['Home_Score'], df.loc[row]['Home_Completion'], df.loc[row]['Home_Tackle']
        awayTeam, awayScore, awayCompletion, awayTackle = df.loc[row]['Away_Team'], df.loc[row]['Away_Score'], df.loc[row]['Away_Completion'], df.loc[row]['Away_Tackle']
        homeELO, awayELO = eloDict[homeTeam], eloDict[awayTeam]

        data = [season, round, venue, kickOffTime, homeTeam, homeScore, homeELO, homeCompletion, homeTackle, awayTeam, awayScore, awayELO, awayCompletion, awayTackle]
        newDataframe.loc[len(newDataframe)] = data

        ##calculating expected outcomes
        expectedScoreHome = expectedScore(homeELO, awayELO)
        expectedScoreAway = expectedScore(awayELO, homeELO)

        ##creating actual outcome values
        if homeScore == awayScore:
            homeOutcome = 0.5
            awayOutcome = 0.5
        elif homeScore > awayScore:
            homeOutcome = 1
            awayOutcome = 0
        else:
            homeOutcome = 0
            awayOutcome = 1

        ##calculating and updating ELO values
        homeNewELO = updatedELO(homeELO, kValue, homeOutcome, expectedScoreHome)
        awayNewELO = updatedELO(awayELO, kValue, awayOutcome, expectedScoreAway)
        eloDict[homeTeam] = homeNewELO
        eloDict[awayTeam] = awayNewELO

    return newDataframe

if __name__ == '__main__':
    main()