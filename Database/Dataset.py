import numpy as np
import DBQuery
from Database import Model


def kohonen_dataset(in_features, team=None):
    train_data = []
    test_data = []

    # Query the database for all matches where the given
    # team is the home team. Exclude matches from 2016
    db_matches_home = DBQuery.Match.get_tippeliga_matches(
            (Model.Match.home_team == team) &
            (Model.Match.game_date.year < 2016)
    )

    # Query the database for all matches where the given
    # team is the away team. Exclude matches from 2016
    db_matches_away = DBQuery.Match.get_tippeliga_matches(
            (Model.Match.away_team == team) &
            (Model.Match.game_date.year < 2016)
    )

    # TODO: When algorithm is working, include 2016 for training

    db_matches = db_matches_home + db_matches_away

    for x in db_matches:
        is_home = 1 if x.home_team_id == team.id else -1

        # Get wins vs losses
        wins = 0
        loss = 0
        tie = 0

        # Matches as HOME TEAM
        for h_match in db_matches_home:
            # Skip newer - COMMENT[JT]: Why?
            if h_match.game_date >= x.game_date or h_match.away_team_id != x.away_team_id:
                continue

            if h_match.score_home > h_match.score_away:
                wins += 1
            elif h_match.score_home < h_match.score_away:
                loss += 1
            else:
                tie += 1

        # Matches as AWAY TEAM
        for h_match in db_matches_away:
            # Skip newer - COMMENT[JT]: Why?
            if h_match.game_date >= x.game_date or h_match.home_team_id != x.home_team_id:
                continue

            if h_match.score_home < h_match.score_away:
                wins += 1
            elif h_match.score_home > h_match.score_away:
                loss += 1
            else:
                tie += 1

        # Take care of wind, rain and temp
        rain = float(x.rain) if x.rain else 0.0
        wind = float(x.wind) if x.wind else 0.0
        temp = float(x.temperature) if x.temperature else 0.0

        # Time-related data
        month = x.game_date.month
        day = x.game_date.day
        hour = x.game_date.hour
        year = x.game_date.year

        # Player-scores from VG site
        vg_scoring_team = x.vg_scoring_home if x.home_team_id == team.id else x.vg_scoring_away
        vg_scoring_other = x.vg_scoring_away if x.home_team_id == team.id else x.vg_scoring_home

        # Table placement
        team_place_team = x.home_team_place if x.home_team_id == team.id else x.vg_scoring_away
        team_place_other = x.away_team_place if x.home_team_id == team.id else x.vg_scoring_away

        feature_set = {
            "rain": rain,
            "wind": wind,
            "temp": temp,
            "is_home": is_home,
            "month": month,
            "day": day,
            "hour": hour,
            "vg_scoring": vg_scoring_team,
            "vg_scoring_other": vg_scoring_other,
            "team_place": team_place_team,
            "team_place_other": team_place_other,
            "wins": wins,
            "loss": loss,
            "tie": tie
        }

        result_set = {
            "H": 0,
            "B": 1,
            "U": 2
        }

        # Select the features given
        features = [feature_set[feature] for feature in in_features]

        # Append the match result as a feature
        features.append(result_set[x.result])

        if year == 2015:
            test_data.append(features)
        elif year >= 2012:
            train_data.append(features)
        else:
            pass

    # Create Numpy array train and test sets
    train = np.array(train_data, dtype=np.float64)
    test = np.array(test_data, dtype=np.float64)

    return train, test
