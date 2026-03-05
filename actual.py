import random
import csv

teams = ["RCB","CSK","SRH","MI","PK","GT","LSG","RR","DC","KKR"]

# ----------------------------
# GLOBAL MATCH VARIABLES
# ----------------------------

batsman_stats_list = []
bowler_stats_list = []
ball_order = 0
bowling_order = [1,2,3,1,2,3,4,5,4,5,4,5,4,5,3,2,1,3,2,1]

# ----------------------------
# BATTING FUNCTIONS
# ----------------------------

def who_on_strike(list_of_batsman):
    for i in range(len(list_of_batsman)):
        if list_of_batsman[i][2]:
            return i

def who_on_non_strike(list_of_batsman):
    for i in range(len(list_of_batsman)):
        if not list_of_batsman[i][2] and list_of_batsman[i][3]==1:
            return i

def order_of_batsman():
    top_order=[0,1,2,4,4,5,6,0,4,2,4,5,6,4,6,4,2,6,4,6]
    mid_order=[0,1,2,4,4,5,0,1,2,6,4,5,6,3,2,4,3,4,4,4]
    low_order=[0,1,2,4,4,5,6,4,1,2,0,2,5,2,3,2,3,2,1,4]
    end_order=[0,1,2,3,4,5,6,0,1,2,2,1,4,6,4,5,5,5,0,0]

    striker = who_on_strike(batsman_stats_list)

    if striker < 3:
        return top_order
    elif striker < 5:
        return mid_order
    elif striker < 7:
        return low_order
    else:
        return end_order

def run_scored():
    order = order_of_batsman()
    return order[random.randint(0,19)]

def total_players_out():
    return sum(1 for i in range(11) if batsman_stats_list[i][3]==-1)

def next_batsman():
    for i in range(11):
        if batsman_stats_list[i][3]==0:
            batsman_stats_list[i][2]=True
            batsman_stats_list[i][3]=1
            return

def strike_changer():
    s = who_on_strike(batsman_stats_list)
    ns = who_on_non_strike(batsman_stats_list)
    batsman_stats_list[s][2], batsman_stats_list[ns][2] = \
        batsman_stats_list[ns][2], batsman_stats_list[s][2]

def batsman_out():
    global ball_order
    striker = who_on_strike(batsman_stats_list)
    print("Out", end=" ")
    batsman_stats_list[striker][1] += ball_order
    print(f"{batsman_stats_list[striker][0]}/{batsman_stats_list[striker][1]}", end=" ")
    batsman_stats_list[striker][2]=False
    batsman_stats_list[striker][3]=-1
    if total_players_out()<10:
        next_batsman()

def update_batsman_stats(run_output):
    global ball_order
    striker = who_on_strike(batsman_stats_list)

    if run_output==5:
        batsman_out()
    else:
        print(f"{run_output}", end=" ")
        batsman_stats_list[striker][0]+=run_output
        batsman_stats_list[striker][1]+=ball_order
        if run_output%2==1:
            strike_changer()

def update_bowler_stats(ball_order,bowler,run_output):
    if run_output==5:
        bowler_stats_list[bowler-1][2]+=1
    elif run_output==0:
        bowler_stats_list[bowler-1][3]+=ball_order
    else:
        bowler_stats_list[bowler-1][1]+=run_output
    bowler_stats_list[bowler-1][0]+=ball_order
teams = ["RCB","CSK","SRH","MI","PK","GT","LSG","RR","DC","KKR"]

def add_final_column():
    for team in teams:
        filename = f"{team}.csv"

        with open(filename, 'r', newline='') as file:
            data = list(csv.reader(file))

        header = data[0]

        if "Final" not in header:
            header.append("Final")

        for i in range(1, 12):
            total_runs = 0
            total_balls = 0

            for col in range(1, len(header)-1):
                cell = data[i][col]
                if cell != "":
                    runs, balls = cell.split("-")
                    total_runs += int(runs)
                    total_balls += int(balls)

            if len(data[i]) < len(header):
                data[i].append(f"{total_runs}-{total_balls}")
            else:
                data[i][-1] = f"{total_runs}-{total_balls}"

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
fixtures = [
['RCB','CSK'], ['CSK','RCB'],
['RCB','SRH'], ['SRH','RCB'],
['RCB','MI'],  ['MI','RCB'],
['RCB','PK'],  ['PK','RCB'],
['RCB','GT'],  ['GT','RCB'],
['RCB','LSG'], ['LSG','RCB'],
['RCB','RR'],  ['RR','RCB'],
['RCB','DC'],  ['DC','RCB'],
['RCB','KKR'], ['KKR','RCB'],
['CSK','SRH'], ['SRH','CSK'],
['CSK','MI'],  ['MI','CSK'],
['CSK','PK'],  ['PK','CSK'],
['CSK','GT'],  ['GT','CSK'],
['CSK','LSG'], ['LSG','CSK'],
['CSK','RR'],  ['RR','CSK'],
['CSK','DC'],  ['DC','CSK'],
['CSK','KKR'], ['KKR','CSK'],
['SRH','MI'],  ['MI','SRH'],
['SRH','PK'],  ['PK','SRH'],
['SRH','GT'],  ['GT','SRH'],
['SRH','LSG'], ['LSG','SRH'],
['SRH','RR'],  ['RR','SRH'],
['SRH','DC'],  ['DC','SRH'],
['SRH','KKR'], ['KKR','SRH'],
['MI','PK'],   ['PK','MI'],
['MI','GT'],   ['GT','MI'],
['MI','LSG'],  ['LSG','MI'],
['MI','RR'],   ['RR','MI'],
['MI','DC'],   ['DC','MI'],
['MI','KKR'],  ['KKR','MI'],
['PK','GT'],   ['GT','PK'],
['PK','LSG'],  ['LSG','PK'],
['PK','RR'],   ['RR','PK'],
['PK','DC'],   ['DC','PK'],
['PK','KKR'],  ['KKR','PK'],
['GT','LSG'],  ['LSG','GT'],
['GT','RR'],   ['RR','GT'],
['GT','DC'],   ['DC','GT'],
['GT','KKR'],  ['KKR','GT'],
['LSG','RR'],  ['RR','LSG'],
['LSG','DC'],  ['DC','LSG'],
['LSG','KKR'], ['KKR','LSG'],
['RR','DC'],   ['DC','RR'],
['RR','KKR'],  ['KKR','RR'],
['DC','KKR'],  ['KKR','DC']
]

played_matches = []

def get_random_match():
    remaining = [m for m in fixtures if m not in played_matches]
    if not remaining:
        return None
    match = random.choice(remaining)
    played_matches.append(match)
    return match

def update_team_csv(team_name, batsman_stats):
    filename = f"{team_name}.csv"
    with open(filename, 'r', newline='') as file:
        reader = list(csv.reader(file))
    match_col = None
    for col in range(1, len(reader[0])):
        if reader[1][col] == "":
            match_col = col
            break
    if match_col is None:
        return
    for i in range(1, 12):
        runs = batsman_stats[i-1][0]
        balls = batsman_stats[i-1][1]
        reader[i][match_col] = f"{runs}-{balls}"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(reader)

def update_table(team1, team2, score1, score2):
    filename = "Table.csv"
    with open(filename, 'r', newline='') as file:
        table = list(csv.reader(file))
    for row in table[1:]:
        if row[0] == team1 or row[0] == team2:
            row[1] = str(int(row[1]) + 1)
    if score1 > score2:
        winner, loser = team1, team2
    elif score2 > score1:
        winner, loser = team2, team1
    else:
        winner = None
    for row in table[1:]:
        if winner and row[0] == winner:
            row[2] = str(int(row[2]) + 1)
            row[5] = str(int(row[5]) + 2)
        if winner and row[0] == loser:
            row[3] = str(int(row[3]) + 1)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table)

match_number = 1

for match in fixtures:

    team1, team2 = match[0], match[1]
    print("\n===================================================")
    print(f"Match {match_number}: {team1} vs {team2}")
    print("===================================================\n")

    all_stats = []
    scores = []
    target = 0
    inning = 0

    while inning < 2:
        input()
        bowler_stats_list=[[0,0,0,0] for _ in range(5)]
        batsman_stats_list=[[0,0,True,1],[0,0,False,1],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0]]

        print(f"\nInnings {inning+1}\n")

        for i in range(0,20):

            ball_order = 1 if (i==17 or i==19) else 2
            bowler=bowling_order[i]

            for ball_num in range(0,6,ball_order):

                run_output = run_scored()
                update_batsman_stats(run_output)
                update_bowler_stats(ball_order,bowler,run_output)

                if total_players_out()==10:
                    break

                total_runs = sum(stats[0] for stats in batsman_stats_list)

                if inning==1 and total_runs>=target:
                    break

            if total_players_out()==10:
                break
            if inning==1 and total_runs>=target:
                break

            strike_changer()
            print(f"\n--- {i+1} Over Complete ---\n")

        print("\nBatting Stats\n")

        for index,stats in enumerate(batsman_stats_list):
            if batsman_stats_list[index][3]==-1:
                print(f"Batsman {index + 1}: Runs: {stats[0]}, Balls: {stats[1]}")
            else:
                print(f"Batsman {index + 1}*: Runs: {stats[0]}, Balls: {stats[1]}")

        total_runs = sum(stats[0] for stats in batsman_stats_list)
        total_balls = sum(stats[1] for stats in batsman_stats_list)
        total_wickets = sum(1 for stats in batsman_stats_list if stats[3] == -1)

        print(f"Total Runs: {total_runs}, Total Balls: {total_balls}, Total Wickets: {total_wickets}")
        print(f"Total Overs: {total_balls // 6}.{total_balls % 6}")

        print("\nBowling Stats\n")
        print("Bowler\tRuns Given\tBalls Bowled\tWickets Taken\tDot Balls")

        for index,stats in enumerate(bowler_stats_list):
            print(f"Bowler {index + 1}\t{stats[1]}\t\t{stats[0]}\t\t{stats[2]}\t\t{stats[3]}")

        scores.append(total_runs)
        all_stats.append([row[:] for row in batsman_stats_list])

        if inning==1 and total_runs>=target:
            print("\nTarget Achieved! It was a succesful chase.")
        elif inning==1 and total_runs==target-1:
            print("\n The fabulous chase fell short by 1 run.")
        elif inning==1:
            print("\n The chasing team couldn't chase the target.")

        if inning==0:
            target=total_runs+1

        inning+=1

    update_team_csv(team1, all_stats[0])
    update_team_csv(team2, all_stats[1])
    update_table(team1, team2, scores[0], scores[1])
    add_final_column()
    print(f"\nFinal Result: {team1} {scores[0]} - {team2} {scores[1]}\n")

    match_number += 1

print("\nLeague Simulation Complete\n")
