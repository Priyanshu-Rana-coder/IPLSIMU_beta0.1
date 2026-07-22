import random
import csv
import statistics

score_bins = {
    "<100":0,"100-109":0,"110-119":0,"120-129":0,
    "130-139":0,"140-149":0,"150-159":0,"160-169":0,
    "170-179":0,"180-189":0,"190-199":0,"200-209":0,
    "210-219":0,"220-229":0,"230-239":0,"240+":0
}

scores = []
wickets_list = []
balls_list = []
run_rates = []
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
    top_order = [0]*32+[1]*23+[2]*13+[3]*5+[4]*12+[6]*10+[5]*5
    mid_order = [0]*40 + [1]*19 + [2]*11 + [3]*5 + [4]*12 + [6]*8 + [5]*5
    low_order = [0]*40 + [1]*20 + [2]*14 + [3]*3 + [4]*8 + [6]*8 + [5]*7
    end_order = [0]*50 + [1]*27 + [2]*4 + [3]*3 + [4]*5 + [6]*5 + [5]*6

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
    return order[random.randint(0,99)]

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
    batsman_stats_list[striker][1] += ball_order
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

def update_score_frequency(score):
    if score < 100:
        score_bins["<100"] += 1
    elif score >= 240:
        score_bins["240+"] += 1
    else:
        lower = (score // 10) * 10
        score_bins[f"{lower}-{lower+9}"] += 1
header = [
    "batter_runs",
    "batter_balls",
    "wickets",
    "target_left",
    "balls_left",
    "non_striker_runs",
    "non_striker_balls",
    "partnership_runs",
    "partnership_balls",
    "partnership_boundaries",
    "partnership_dots",
    "team_runs",
    "team_balls",
    "batter_group",
    "non_striker_group",
    "intent",
    "risk"
]
num = 8000

with open("dataset.csv", "w", newline="") as f:

    writer = csv.writer(f)
    writer.writerow(header)

    num = 4000

    for match_id in range(num):

        if match_id % 400 == 0:
            print(match_id)

        virtual_target = random.randint(160, 190)
        target = 0
        inning = 0

        while inning < 2:

            bowler_stats_list = [[0,0,0,0] for _ in range(5)]

            batsman_stats_list = [
                [0,0,True,1],[0,0,False,1],[0,0,False,0],
                [0,0,False,0],[0,0,False,0],[0,0,False,0],
                [0,0,False,0],[0,0,False,0],[0,0,False,0],
                [0,0,False,0],[0,0,False,0]
            ]

            partnership_runs = 0
            partnership_balls = 0
            partnership_boundaries = 0
            partnership_dots = 0

            for over in range(20):
                ball_order = 1
                bowler = bowling_order[over]
                for ball_num in range(0, 6, ball_order):
                    striker = who_on_strike(batsman_stats_list)
                    non_striker = who_on_non_strike(batsman_stats_list)

                    team_runs = sum(x[0] for x in batsman_stats_list)
                    team_balls = sum(x[1] for x in batsman_stats_list)
                    wickets = total_players_out()

                    balls_left = 120 - team_balls

                    if inning == 0:

                        if team_runs < virtual_target:
                            target_left = virtual_target - team_runs
                        else:
                            current_run_rate = (
                                team_runs / team_balls if team_balls > 0 else 0
                            )
                            projected_score = int(current_run_rate * 120 + 15)
                            target_left = projected_score - team_runs

                    else:
                        target_left = target - team_runs

                    if striker < 3:
                        batter_group = 1
                    elif striker < 5:
                        batter_group = 2
                    elif striker < 7:
                        batter_group = 3
                    else:
                        batter_group = 4

                    if non_striker < 3:
                        non_striker_group = 1
                    elif non_striker < 5:
                        non_striker_group = 2
                    elif non_striker < 7:
                        non_striker_group = 3
                    else:
                        non_striker_group = 4

                    writer.writerow([
                        batsman_stats_list[striker][0],
                        batsman_stats_list[striker][1],
                        wickets,
                        target_left,
                        balls_left,
                        batsman_stats_list[non_striker][0],
                        batsman_stats_list[non_striker][1],
                        partnership_runs,
                        partnership_balls,
                        partnership_boundaries,
                        partnership_dots,
                        team_runs,
                        team_balls,
                        batter_group,
                        non_striker_group,
                        0,
                        0
                    ])

                    run_output = run_scored()

                    update_batsman_stats(run_output)
                    update_bowler_stats(ball_order, bowler, run_output)

                    if run_output == 5:
                        partnership_runs = 0
                        partnership_balls = 0
                        partnership_boundaries = 0
                        partnership_dots = 0
                    else:
                        partnership_runs += run_output
                        partnership_balls += ball_order

                        if run_output == 0:
                            partnership_dots += ball_order

                        if run_output == 4 or run_output == 6:
                            partnership_boundaries += 1

                    if total_players_out() == 10:
                        break

                    total_runs = sum(stats[0] for stats in batsman_stats_list)

                    if inning == 1 and total_runs >= target:
                        break

                if total_players_out() == 10:
                    break

                if inning == 1 and total_runs >= target:
                    break

                strike_changer()

            total_runs = sum(stats[0] for stats in batsman_stats_list)
            total_balls = sum(stats[1] for stats in batsman_stats_list)
            total_wickets = total_players_out()

            scores.append(total_runs)
            wickets_list.append(total_wickets)
            balls_list.append(total_balls)
            run_rates.append(total_runs * 6 / total_balls)

            if inning == 0:
                target = total_runs + 1
            update_score_frequency(total_runs)
            inning += 1
print("Dataset generation complete.")
print("\n" + "=" * 40)
print("SCORE DISTRIBUTION")
print("=" * 40)

total_innings = sum(score_bins.values())

for rng, freq in score_bins.items():
    percentage = freq * 100 / total_innings
    print(f"{rng:<10} : {freq:>5} ({percentage:5.2f}%)")
print("\n" + "="*45)
print("OVERALL STATISTICS")
print("="*45)

print(f"Average Score      : {statistics.mean(scores):.2f}")
print(f"Median Score       : {statistics.median(scores):.2f}")
print(f"Std Deviation      : {statistics.stdev(scores):.2f}")
print(f"Highest Score      : {max(scores)}")
print(f"Lowest Score       : {min(scores)}")
print(f"Average Wickets    : {statistics.mean(wickets_list):.2f}")
print(f"Average Balls      : {statistics.mean(balls_list):.2f}")
print(f"Average Overs      : {statistics.mean(balls_list)/6:.2f}")
print(f"All-out %%          : {100*wickets_list.count(10)/total_innings:.2f}%")
print(f"Average Run Rate   : {statistics.mean(run_rates):.2f}")