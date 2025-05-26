-- Create the seasons table
CREATE TABLE seasons (
    id SERIAL PRIMARY KEY,
    year VARCHAR(10) NOT NULL
);

-- Create the teams table
CREATE TABLE teams (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create the team_statistics table
CREATE TABLE team_statistics (
    id SERIAL PRIMARY KEY,
    season_id INTEGER REFERENCES seasons(id),
    team_id VARCHAR(20) REFERENCES teams(id),
    
    -- Offensive Statistics
    goalsScored INTEGER,
    goalsConceded INTEGER,
    ownGoals INTEGER,
    assists INTEGER,
    shots INTEGER,
    penaltyGoals INTEGER,
    penaltiesTaken INTEGER,
    freeKickGoals INTEGER,
    freeKickShots INTEGER,
    goalsFromInsideTheBox INTEGER,
    goalsFromOutsideTheBox INTEGER,
    shotsFromInsideTheBox INTEGER,
    shotsFromOutsideTheBox INTEGER,
    headedGoals INTEGER,
    leftFootGoals INTEGER,
    rightFootGoals INTEGER,
    bigChances INTEGER,
    bigChancesCreated INTEGER,
    bigChancesMissed INTEGER,
    shotsOnTarget INTEGER,
    shotsOffTarget INTEGER,
    blockedScoringAttempt INTEGER,
    successfulDribbles INTEGER,
    dribbleAttempts INTEGER,
    corners INTEGER,
    hitWoodwork INTEGER,
    fastBreaks INTEGER,
    fastBreakGoals INTEGER,
    fastBreakShots INTEGER,
    
    -- Possession Statistics
    averageBallPossession DECIMAL(10,3),
    totalPasses INTEGER,
    accuratePasses INTEGER,
    accuratePassesPercentage DECIMAL(10,3),
    totalOwnHalfPasses INTEGER,
    accurateOwnHalfPasses INTEGER,
    accurateOwnHalfPassesPercentage DECIMAL(10,3),
    totalOppositionHalfPasses INTEGER,
    accurateOppositionHalfPasses INTEGER,
    accurateOppositionHalfPassesPercentage DECIMAL(10,3),
    totalLongBalls INTEGER,
    accurateLongBalls INTEGER,
    accurateLongBallsPercentage DECIMAL(10,3),
    totalCrosses INTEGER,
    accurateCrosses INTEGER,
    accurateCrossesPercentage DECIMAL(10,3),
    
    -- Defensive Statistics
    cleanSheets INTEGER,
    tackles INTEGER,
    interceptions INTEGER,
    saves INTEGER,
    errorsLeadingToGoal INTEGER,
    errorsLeadingToShot INTEGER,
    penaltiesCommited INTEGER,
    penaltyGoalsConceded INTEGER,
    clearances INTEGER,
    clearancesOffLine INTEGER,
    lastManTackles INTEGER,
    
    -- Duels
    totalDuels INTEGER,
    duelsWon INTEGER,
    duelsWonPercentage DECIMAL(10,3),
    totalGroundDuels INTEGER,
    groundDuelsWon INTEGER,
    groundDuelsWonPercentage DECIMAL(10,3),
    totalAerialDuels INTEGER,
    aerialDuelsWon INTEGER,
    aerialDuelsWonPercentage DECIMAL(10,3),
    
    -- Other Statistics
    possessionLost INTEGER,
    offsides INTEGER,
    fouls INTEGER,
    yellowCards INTEGER,
    yellowRedCards INTEGER,
    redCards INTEGER,
    avgRating DECIMAL(10,3),
    matches INTEGER,
    awardedMatches INTEGER,

    -- Against Statistics
    accurateFinalThirdPassesAgainst INTEGER,
    accurateOppositionHalfPassesAgainst INTEGER,
    accurateOwnHalfPassesAgainst INTEGER,
    accuratePassesAgainst INTEGER,
    bigChancesAgainst INTEGER,
    bigChancesCreatedAgainst INTEGER,
    bigChancesMissedAgainst INTEGER,
    clearancesAgainst INTEGER,
    cornersAgainst INTEGER,
    crossesSuccessfulAgainst INTEGER,
    crossesTotalAgainst INTEGER,
    dribbleAttemptsTotalAgainst INTEGER,
    dribbleAttemptsWonAgainst INTEGER,
    errorsLeadingToGoalAgainst INTEGER,
    errorsLeadingToShotAgainst INTEGER,
    hitWoodworkAgainst INTEGER,
    interceptionsAgainst INTEGER,
    keyPassesAgainst INTEGER,
    longBallsSuccessfulAgainst INTEGER,
    longBallsTotalAgainst INTEGER,
    offsidesAgainst INTEGER,
    redCardsAgainst INTEGER,
    shotsAgainst INTEGER,
    shotsBlockedAgainst INTEGER,
    shotsFromInsideTheBoxAgainst INTEGER,
    shotsFromOutsideTheBoxAgainst INTEGER,
    shotsOffTargetAgainst INTEGER,
    shotsOnTargetAgainst INTEGER,
    blockedScoringAttemptAgainst INTEGER,
    tacklesAgainst INTEGER,
    totalFinalThirdPassesAgainst INTEGER,
    oppositionHalfPassesTotalAgainst INTEGER,
    ownHalfPassesTotalAgainst INTEGER,
    totalPassesAgainst INTEGER,
    yellowCardsAgainst INTEGER,
    
    -- Additional Statistics
    throwIns INTEGER,
    goalKicks INTEGER,
    ballRecovery INTEGER,
    freeKicks INTEGER,
    keyPasses INTEGER,
    
    UNIQUE(season_id, team_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_team_statistics_season ON team_statistics(season_id);
CREATE INDEX idx_team_statistics_team ON team_statistics(team_id); 