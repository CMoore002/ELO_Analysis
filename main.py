
import pandas as pd

def main():
    eloDict = getNewEloDict()
    kValue = 55
    season = input("Enter Season: ")
    fileName = lambda x: "{}_SEASON_NRL_DATA_v1.1".format(x)
    print(fileName(season))
    dfOne = pd.read_csv(fileName(int(season) - 2))
    dfTwo = pd.read_csv(fileName(int(season) - 1))
    dfThree = pd.read_csv(fileName(season))
    print(dfOne.iloc[0])


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
##param kValue: the constant that we're trying to optimise
##param eloDict: a dictionary containing the ELO ratings of each team
##
def processSeasonData(df, kValue, eloDict):
    correctCount = 0
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

if __name__ == '__main__':
    main()