import peewee
import datetime
from playhouse.pool import MySQLDatabase


database = MySQLDatabase(
        "ikt441",
        host="wan.uia.io",
        port=3306,
        user="homo",
        passwd="homo123",
)


model_classes = []


class Team(peewee.Model):
    name = peewee.CharField(unique=True)
    num = peewee.DecimalField(null=False)

    class Meta:
        database = database
        db_table = 'tippeliga_team'
model_classes.append(Team)


class Stadium(peewee.Model):
    name = peewee.CharField(null=False, unique=True)
    lat = peewee.DecimalField(decimal_places=6)
    lon = peewee.DecimalField(decimal_places=6)

    class Meta:
        database = database
        db_table = 'tippeliga_stadium'
model_classes.append(Stadium)


class Player(peewee.Model):
    p_name = peewee.CharField(null=True)
    p_id = peewee.IntegerField(null=False, primary_key=True)
    p_age = peewee.DateTimeField(null=True)
    p_weight = peewee.DoubleField(null=True)
    p_borned = peewee.CharField(null=True)
    p_country = peewee.CharField(null=True)
    p_position = peewee.CharField(null=True)
    p_height = peewee.DoubleField(null=True)
    p_number = peewee.IntegerField(null=True)
    p_starts = peewee.IntegerField(null=True)
    p_tot_goals = peewee.IntegerField(null=True)
    p_played_time = peewee.DoubleField(null=True)
    p_exchanged = peewee.IntegerField(null=True)
    p_onbench = peewee.IntegerField(null=True)
    p_assists = peewee.IntegerField(null=True)
    p_points = peewee.IntegerField(null=True)
    p_penalty_kick = peewee.IntegerField(null=True)
    p_penalty_misses = peewee.IntegerField(null=True)
    p_sgoals = peewee.IntegerField(null=True)
    p_yellowcards = peewee.IntegerField(null=True)
    p_redcards = peewee.IntegerField(null=True)
    p_score = peewee.DoubleField(null=False)

    class Meta:
        database = database
        db_table = 'tippeliga_player'
model_classes.append(Player)


class Parameter(peewee.Model):
    last_match_playerscore = peewee.FloatField(null=False)
    last_team_placement = peewee.FloatField(null=False)
    avg_season_score = peewee.FloatField(null=False)
    avg_opponent_score = peewee.FloatField(null=False)
    expected_output = peewee.FloatField(null=False)
    year = peewee.IntegerField(null=False)

    class Meta:
        database = database
        db_table = 'tippeliga_parameter'
model_classes.append(Parameter)


class Match(peewee.Model):

    home_team = peewee.ForeignKeyField(Team, related_name="home_team")
    away_team = peewee.ForeignKeyField(Team, related_name="away_team")

    score_home = peewee.IntegerField(null=True)
    score_away = peewee.IntegerField(null=True)

    score_home_ht = peewee.IntegerField(null=True)
    score_away_ht = peewee.IntegerField(null=True)

    score_home_chances = peewee.IntegerField(null=True)
    score_away_chances = peewee.IntegerField(null=True)
    result = peewee.CharField(null=True)

    audience = peewee.IntegerField(null=True, default=None)
    stadium = peewee.ForeignKeyField(Stadium, related_name="stadium")
    game_date = peewee.DateTimeField(null=False)
    division = peewee.IntegerField(null=False)

    home_team_place = peewee.DecimalField(null=True, default=None)
    away_team_place = peewee.DecimalField(null=True, default=None)

    home_team_players = peewee.TextField(null=True, default=None)
    away_team_players = peewee.TextField(null=True, default=None)

    est_player_score_home = peewee.FloatField(null=True, default=None)
    est_player_score_away = peewee.FloatField(null=True, default=None)

    vg_scoring_home = peewee.IntegerField(null=True, default=None)
    vg_scoring_away = peewee.IntegerField(null=True, default=None)

    rain = peewee.DecimalField(decimal_places=6, null=True, default=None)
    wind = peewee.DecimalField(decimal_places=6, null=True, default=None)
    temperature = peewee.DecimalField(decimal_places=6, null=True, default=None)

    last_updated = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        db_table = 'tippeliga_match'
model_classes.append(Match)


class PlayerScore(peewee.Model):
    player = peewee.ForeignKeyField(Player, related_name="player")
    match = peewee.ForeignKeyField(Match, related_name="match")
    score = peewee.IntegerField(null=False)
    date = peewee.DateField(null=False)

    class Meta:
        database = database
        db_table = 'tippeliga_playerscore'
model_classes.append(PlayerScore)


class WeatherStation(peewee.Model):
    from_date = peewee.DateField(null=False)
    to_date = peewee.DateField(null=True)
    name = peewee.CharField(null=False)
    lat = peewee.DecimalField(null=False, decimal_places=6)
    lon = peewee.DecimalField(null=False, decimal_places=6)

    class Meta:
        database = database
        db_table = 'tippeliga_weather_station'
model_classes.append(WeatherStation)


class WeatherElement(peewee.Model):
    code = peewee.CharField(null=False, primary_key=True)
    name = peewee.CharField(null=False)
    group = peewee.CharField(null=False)
    description = peewee.CharField(null=False)
    unit = peewee.CharField(null=False)

    class Meta:
        database = database
        db_table = 'tippeliga_weather_element'
model_classes.append(WeatherElement)


class WeatherStationElement(peewee.Model):
    station = peewee.ForeignKeyField(WeatherStation, related_name="station")
    code = peewee.ForeignKeyField(WeatherElement, related_name="fk_code")
    group = peewee.CharField(null=False)
    unit = peewee.CharField(null=False)
    from_date = peewee.DateField(null=False)
    to_date = peewee.DateField(null=True)

    class Meta:
        database = database
        db_table = 'tippeliga_weather_station_element'
model_classes.append(WeatherStationElement)


class GeneticResult(peewee.Model):
    team_home = peewee.ForeignKeyField(Team, related_name="team_home", null=False)
    team_away = peewee.ForeignKeyField(Team, related_name="team_away", null=True)
    weight_fitness = peewee.FloatField(null=True)
    parameter_fitness = peewee.FloatField(null=True)
    weight_data = peewee.BlobField(null=True)
    parameter_data = peewee.BlobField(null=True)
    weight_gen = peewee.IntegerField(null=True)
    parameter_gen = peewee.IntegerField(null=True)
    num_matches = peewee.IntegerField(null=True)
    training_data = None

    class Meta:
        database = database
        db_table = 'tippeliga_genetic_result'
model_classes.append(GeneticResult)


########################################################################


for c in model_classes:
    try:
        c.create_table()
        print("Table %s created!" % c.__name__)
    except Exception as e:
        print(e)
