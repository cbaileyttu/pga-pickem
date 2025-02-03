# models.py
import sqlite3

class User:
    def __init__(self, id=None, username=None, email=None):
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def get_all():
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [User(**dict(zip([column[0] for column in cursor.description], row))) for row in cursor.fetchall()]
        conn.close()
        return users

    @staticmethod
    def get_by_id(user_id):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
             return User(**dict(zip([column[0] for column in cursor.description], row)))
        return None

    @staticmethod
    def get_by_username(username):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(**dict(zip([column[0] for column in cursor.description], row)))
        return None

    def save(self):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        if self.id is None:
             if not self.email or self.email.strip() == "":
                 raise ValueError("Email cannot be empty.")
             cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (self.username, self.email))
             self.id = cursor.lastrowid
        else:
             cursor.execute("UPDATE users SET username = ?, email = ? WHERE id = ?", (self.username, self.email, self.id))
        conn.commit()
        conn.close()


class Tournament:
    def __init__(self, id=None, name=None, type=None, picks_allowed=None, date = None):
        self.id = id
        self.name = name
        self.type = type
        self.picks_allowed = picks_allowed
        self.date = date

    @staticmethod
    def get_all():
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tournaments")
        tournaments = [Tournament(*row) for row in cursor.fetchall()]
        conn.close()
        return tournaments

    @staticmethod
    def get_by_id(tournament_id):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tournaments WHERE id = ?", (tournament_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Tournament(*row)
        return None

    def save(self):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        if self.id is None:
           cursor.execute("INSERT INTO tournaments (name, type, picks_allowed, date) VALUES (?, ?, ?, ?)",
                           (self.name, self.type, self.picks_allowed, self.date))
           self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE tournaments SET name = ?, type = ?, picks_allowed = ?, date = ? WHERE id = ?",
                       (self.name, self.type, self.picks_allowed, self.date, self.id))
        conn.commit()
        conn.close()

class Golfer:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @staticmethod
    def get_all():
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM golfers")
        golfers = [Golfer(*row) for row in cursor.fetchall()]
        conn.close()
        return golfers

    @staticmethod
    def get_by_id(golfer_id):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM golfers WHERE id = ?", (golfer_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Golfer(*row)
        return None

    @staticmethod
    def get_by_name(golfer_name):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM golfers WHERE name = ?", (golfer_name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Golfer(*row)
        return None

    def save(self):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO golfers (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
             cursor.execute("UPDATE golfers SET name = ? WHERE id = ?", (self.name, self.id))
        conn.commit()
        conn.close()

class Pick:
    def __init__(self, id=None, user_id=None, tournament_id=None, golfer_id=None, is_additional_pick=0):
        self.id = id
        self.user_id = user_id
        self.tournament_id = tournament_id
        self.golfer_id = golfer_id
        self.is_additional_pick = is_additional_pick

    @staticmethod
    def get_all():
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM picks")
        picks = [Pick(*row) for row in cursor.fetchall()]
        conn.close()
        return picks

    @staticmethod
    def get_by_id(pick_id):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM picks WHERE id = ?", (pick_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Pick(*row)
        return None

    @staticmethod
    def get_by_user_tournament(user_id, tournament_id):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM picks WHERE user_id = ? AND tournament_id = ?", (user_id, tournament_id,))
        picks = [Pick(*row) for row in cursor.fetchall()]
        conn.close()
        return picks

    def save(self):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO picks (user_id, tournament_id, golfer_id, is_additional_pick) VALUES (?, ?, ?, ?)",
                        (self.user_id, self.tournament_id, self.golfer_id, self.is_additional_pick))
            self.id = cursor.lastrowid
        else:
           cursor.execute("UPDATE picks SET user_id = ?, tournament_id = ?, golfer_id = ?, is_additional_pick = ? WHERE id = ?",
                        (self.user_id, self.tournament_id, self.golfer_id, self.is_additional_pick, self.id))
        conn.commit()
        conn.close()

class Result:
    def __init__(self, id=None, tournament_id=None, golfer_id=None, purse_money=None):
        self.id = id
        self.tournament_id = tournament_id
        self.golfer_id = golfer_id
        self.purse_money = purse_money

    @staticmethod
    def get_all():
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM results")
        results = [Result(*row) for row in cursor.fetchall()]
        conn.close()
        return results

    @staticmethod
    def get_by_id(result_id):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM results WHERE id = ?", (result_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Result(*row)
        return None

    @staticmethod
    def get_by_tournament(tournament_id):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM results WHERE tournament_id = ?", (tournament_id,))
        results = [Result(*row) for row in cursor.fetchall()]
        conn.close()
        return results

    def save(self):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        if self.id is None:
           cursor.execute("INSERT INTO results (tournament_id, golfer_id, purse_money) VALUES (?, ?, ?)",
                           (self.tournament_id, self.golfer_id, self.purse_money))
           self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE results SET tournament_id = ?, golfer_id = ?, purse_money = ? WHERE id = ?",
                        (self.tournament_id, self.golfer_id, self.purse_money, self.id))
        conn.commit()
        conn.close()

class Winnings:
     def __init__(self, id=None, user_id=None, tournament_id=None, weekly_winnings=0, cumulative_winnings=0, additional_pick_fee = 0):
        self.id = id
        self.user_id = user_id
        self.tournament_id = tournament_id
        self.weekly_winnings = weekly_winnings
        self.cumulative_winnings = cumulative_winnings
        self.additional_pick_fee = additional_pick_fee

     @staticmethod
     def get_all():
         conn = sqlite3.connect('golf_picks.db')
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM winnings")
         winnings = [Winnings(*row) for row in cursor.fetchall()]
         conn.close()
         return winnings

     @staticmethod
     def get_by_id(winnings_id):
         conn = sqlite3.connect('golf_picks.db')
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM winnings WHERE id = ?", (winnings_id,))
         row = cursor.fetchone()
         conn.close()
         if row:
             return Winnings(*row)
         return None

     @staticmethod
     def get_by_user_tournament(user_id, tournament_id):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM winnings WHERE user_id = ? AND tournament_id = ?", (user_id, tournament_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Winnings(*row)
        return None

     def save(self):
        conn = sqlite3.connect('golf_picks.db')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO winnings (user_id, tournament_id, weekly_winnings, cumulative_winnings, additional_pick_fee) VALUES (?, ?, ?, ?, ?)",
                       (self.user_id, self.tournament_id, self.weekly_winnings, self.cumulative_winnings, self.additional_pick_fee))
            self.id = cursor.lastrowid
        else:
             cursor.execute("UPDATE winnings SET user_id = ?, tournament_id = ?, weekly_winnings = ?, cumulative_winnings = ?, additional_pick_fee = ? WHERE id = ?",
                        (self.user_id, self.tournament_id, self.weekly_winnings, self.cumulative_winnings, self.additional_pick_fee, self.id))
        conn.commit()
        conn.close()