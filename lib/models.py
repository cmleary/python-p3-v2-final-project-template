
from __init__ import CONN, CURSOR

class Player:

    all = []

    def __init__(self, name):
        self.id = None
        self.name = name
        self.scores = []

    def __repr__(self):
        return f'Player # {self.id}: {self.name}'

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS players
        """

        CURSOR.execute(sql)
        
        cls.all = []

    @classmethod
    def new_from_db(cls, row):
        player = cls(row[1])
        player.id = row[0]
        return player
    
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM players
        """

        all = CURSOR.execute(sql).fetchall()
        
        cls.all = [cls.new_from_db(row) for row in all]

        return cls.all
    
    
    @classmethod
    def find_by_id(cls, id):
        players = [player for player in Player.all if player.id == id]

        if players:
            return players[0]
        else:
            return None

    @classmethod
    def create(cls, name):
        player = Player(name)
        player.save()
        cls.all.append(player)
        return player
    
    def save(self):
        sql = """
            INSERT INTO players (name)
            VALUES (?)
        """

        CURSOR.execute(sql, (self.name,))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM players").fetchone()[0]
        CONN.commit()

    def update(self):
        sql = """
            UPDATE players
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM players
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        

        Player.all = [player for player in Player.all if player.id != self.id]


        for score in self.scores:
            if score.player_id == self.id:
                score.delete()

class Score:

    all = []

    def __init__(self, player_id, scoring):
        self.id = None
        self.player_id = player_id
        self.player = Player.find_by_id(player_id)
        self.player.scores.append(self)
        self.scoring = scoring

    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, player_parameter):
        if isinstance(player_parameter, Player):
            self._player = player_parameter
        else:
            raise Exception(f"Error: Player # {self.player_id} does not exist!")
        
    @property
    def scoring(self):
        return self._scoring
    
    @scoring.setter
    def scoring(self, scoring_parameter):
        if 0 <= scoring_parameter:
            self._scoring = scoring_parameter
        else:
            raise Exception("Error: Git good!")

    def __repr__(self):
        return f'Score {self.id}: {self.player.name} received a scoring of {self.scoring}'

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                player_id INTEGER,
                scoring INTEGER
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS scores
        """

        CURSOR.execute(sql)
        
        cls.all = []

    @classmethod
    def new_from_db(cls, row):
        score = cls(row[1], row[2])
        score.id = row[0]
        return score
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM scores
        """

        all = CURSOR.execute(sql).fetchall()
        
        cls.all = [cls.new_from_db(row) for row in all]

        return cls.all
    
    @classmethod
    def find_by_id(cls, id):
        scores = [score for score in Score.all if score.id == id]

        if scores:
            return scores[0]
        else:
            return None

    @classmethod
    def create(cls, player_id, scoring):
        score = Score(player_id, scoring)
        score.save()
        cls.all.append(score)
        return score
    
    def save(self):
        sql = """
            INSERT INTO scores (player_id, scoring)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.player_id, self.scoring))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM scores").fetchone()[0]
        CONN.commit()

    def update(self):
        sql = """
            UPDATE scores
            SET player_id = ?, scoring = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.player_id, self.scoring, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM scores
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
    
        Score.all = [score for score in Score.all if score.id != self.id]

        
        self.player.scores = [score for score in self.player.scores if score.id != self.id]