# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import User, Tournament, Golfer, Pick, Result, Winnings

app = Flask(__name__)

# --- User Routes ---
@app.route('/users')
def list_users():
    users = User.get_all()
    return render_template('users/list.html', users=users)


@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email = email)
        user.save()
        return redirect(url_for('list_users'))
    return render_template('users/add.html')


# --- Tournament Routes ---
@app.route('/tournaments')
def list_tournaments():
    tournaments = Tournament.get_all()
    return render_template('tournaments/list.html', tournaments=tournaments)


@app.route('/tournaments/add', methods=['GET', 'POST'])
def add_tournament():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        picks_allowed = request.form['picks_allowed']
        date = request.form.get('date', '')
        tournament = Tournament(name=name, type=type, picks_allowed=picks_allowed, date = date)
        tournament.save()
        return redirect(url_for('list_tournaments'))
    return render_template('tournaments/add.html')

# --- Golfer Routes ---
@app.route('/golfers')
def list_golfers():
    golfers = Golfer.get_all()
    return render_template('golfers/list.html', golfers=golfers)

@app.route('/golfers/add', methods=['GET', 'POST'])
def add_golfer():
    if request.method == 'POST':
        name = request.form['name']
        golfer = Golfer(name=name)
        golfer.save()
        return redirect(url_for('list_golfers'))
    return render_template('golfers/add.html')


@app.route('/picks')
def list_picks():
    picks = Pick.get_all()
    users = User.get_all()
    tournaments = Tournament.get_all()

      # Create a list of formatted picks
    formatted_picks = []
    for pick in picks:
        user = User.get_by_id(pick.user_id)
        tournament = Tournament.get_by_id(pick.tournament_id)
        golfer = Golfer.get_by_id(pick.golfer_id)
        if user and tournament and golfer:
            formatted_picks.append({
                'user_id': user.id,
                'username': user.username,
                'tournament_id': tournament.id,
                'tournament_name': tournament.name,
                'golfer_name': golfer.name,
                'is_additional_pick': pick.is_additional_pick
              })
    return render_template('picks/list.html', formatted_picks=formatted_picks, users = users, tournaments = tournaments)

@app.route('/picks/add', methods=['GET', 'POST'])
def add_pick():
    users = User.get_all()
    tournaments = Tournament.get_all()
    golfers = Golfer.get_all()
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        tournament_id = int(request.form['tournament_id'])
        golfer_id = int(request.form['golfer_id'])
        is_additional_pick = bool(request.form.get('is_additional_pick'))
        user = User.get_by_id(user_id)
        tournament = Tournament.get_by_id(tournament_id)
        golfer = Golfer.get_by_id(golfer_id)

        if not user or not tournament or not golfer:
            return "Invalid user, tournament, or golfer.", 400

           # Check if user has existing picks for this tournament
        existing_picks = Pick.get_by_user_tournament(user_id, tournament_id)
        num_picks_for_user = len(existing_picks)


        if num_picks_for_user >= tournament.picks_allowed and not is_additional_pick:
            return f"You are not allowed to select more than {tournament.picks_allowed} for {tournament.name}", 400

          # Check golfer picks for this season
        all_picks = Pick.get_all()
        golfer_picks_for_season = [pick for pick in all_picks if pick.golfer_id == golfer_id and pick.user_id == user_id]
        num_golfer_picks_for_season = len(golfer_picks_for_season)

          #Check major limits
        if tournament.type == "major":
            golfer_picks_for_major = [pick for pick in golfer_picks_for_season if Tournament.get_by_id(pick.tournament_id).type == "major"]
            if len(golfer_picks_for_major) >= 1:
                return "You cannot pick the same golfer more than once in a major.", 400

          # Check regular and signature limits
        elif num_golfer_picks_for_season >= 2:
            return "You cannot pick the same golfer more than twice in the season.", 400

           # Handle additional pick fees
        if is_additional_pick:
            winnings_record = Winnings.get_by_user_tournament(user_id, tournament_id)
            if not winnings_record:
                winnings_record = Winnings(user_id = user_id, tournament_id = tournament_id, additional_pick_fee = 5.00)
            else:
                winnings_record.additional_pick_fee = winnings_record.additional_pick_fee + 5.00
            winnings_record.save()
        pick = Pick(user_id=user_id, tournament_id=tournament_id, golfer_id=golfer_id, is_additional_pick = is_additional_pick)
        pick.save()
        return redirect(url_for('list_picks'))
    return render_template('picks/add.html', users=users, tournaments=tournaments, golfers=golfers)


# --- Results Routes ---
@app.route('/results')
def list_results():
    results = Result.get_all()
    formatted_results = []
    for result in results:
        tournament = Tournament.get_by_id(result.tournament_id)
        golfer = Golfer.get_by_id(result.golfer_id)
        if tournament and golfer:
           formatted_results.append({
               'tournament_name': tournament.name,
               'golfer_name': golfer.name,
               'purse_money': result.purse_money
            })
    return render_template('results/list.html', results=formatted_results)

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    tournaments = Tournament.get_all()
    golfers = Golfer.get_all()
    if request.method == 'POST':
        tournament_id = int(request.form['tournament_id'])
        golfer_id = int(request.form['golfer_id'])
        purse_money = float(request.form['purse_money'])
        result = Result(tournament_id = tournament_id, golfer_id = golfer_id, purse_money = purse_money)
        result.save()
        return redirect(url_for('list_results'))
    return render_template('results/add.html', tournaments = tournaments, golfers = golfers)

# --- Winnings Routes ---
@app.route('/winnings')
def list_winnings():
    winnings = Winnings.get_all()
    users = User.get_all()
    tournaments = Tournament.get_all()
    formatted_winnings = []
    for tournament in tournaments:
        for winning in winnings:
            if winning.tournament_id == tournament.id:
                user = User.get_by_id(winning.user_id)
                picks = Pick.get_by_user_tournament(winning.user_id, tournament.id)
                if len(picks) > 0:
                    golfer = Golfer.get_by_id(picks[0].golfer_id)
                    if golfer:
                        formatted_winnings.append({
                            'tournament_name': tournament.name,
                            'user_name': user.username if user else "no user",
                            'golfer_name': golfer.name if golfer else "no golfer",
                            'weekly_winnings': winning.weekly_winnings,
                            'additional_pick_fee': winning.additional_pick_fee
                        })


    return render_template('winnings/list.html', formatted_winnings=formatted_winnings)

@app.route('/winnings/add', methods=['GET', 'POST'])
def add_winnings():
   users = User.get_all()
   tournaments = Tournament.get_all()
   if request.method == 'POST':
    user_id = request.form['user_id']
    tournament_id = request.form['tournament_id']
    weekly_winnings = request.form['weekly_winnings']
    cumulative_winnings = request.form['cumulative_winnings']
    additional_pick_fee = request.form['additional_pick_fee']
    winnings = Winnings(user_id = user_id, tournament_id = tournament_id, weekly_winnings = weekly_winnings, cumulative_winnings = cumulative_winnings, additional_pick_fee = additional_pick_fee)
    winnings.save()
    return redirect(url_for('list_winnings'))
    return render_template('winnings/add.html', users = users, tournaments = tournaments)

@app.route('/calculate_winnings')
def calculate_winnings():
    tournaments = Tournament.get_all()
    for tournament in tournaments:
        results = Result.get_by_tournament(tournament.id)
        if not results:
            continue

      # Find the best purse
        best_purse = 0
        winning_golfers = []
        for result in results:
            if result.purse_money > best_purse:
                winning_golfers = [result.golfer_id]
                best_purse = result.purse_money
            elif result.purse_money == best_purse:
                winning_golfers.append(result.golfer_id)

        picks = Pick.get_all()
        tournament_picks = [pick for pick in picks if pick.tournament_id == tournament.id]

      # Calculate pot
        pot = 0
        for pick in tournament_picks:
            winnings_record = Winnings.get_by_user_tournament(pick.user_id, pick.tournament_id)
            if winnings_record:
                pot = pot + winnings_record.additional_pick_fee

       # determine the winning user
        winning_users = []
        for pick in tournament_picks:
            if pick.golfer_id in winning_golfers:
                winning_users.append(pick.user_id)

# Distribute pot among winning users
        if winning_users:
            split_pot = pot / len(winning_users)  # Split winnings if multiple winners
            for user_id in winning_users:
                winnings_record = Winnings.get_by_user_tournament(user_id, tournament.id)
                if not winnings_record:
                    winnings_record = Winnings(user_id=user_id, tournament_id=tournament.id, weekly_winnings=0)
                winnings_record.weekly_winnings += split_pot  # Add instead of overwrite
                winnings_record.save()

    return redirect(url_for('list_winnings'))


if __name__ == '__main__':
    app.run(debug=True)