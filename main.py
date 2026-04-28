import random

# batsman_stats_list contains individual list of batsman and their data
# data is stored in this format [runs, balls, onStrike, onPitch]
batsman_stats_list=[[0,0,True,1],[0,0,False,1],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0]]

# ball_order is used as aggression multiplier (death overs spike)
ball_order=0

# bowler_stats_list contains individual list of bowlers and their data
# data is stored in this format [balls bowled, runs given, wickets taken, dot balls]
bowler_stats_list=[[0,0,0,0] for _ in range(5)]

# bowling_order list contains the order of bowlers in which they will bowl overs
bowling_order=[1,2,3,1,2,3,4,5,4,5,4,5,4,5,3,2,1,3,2,1]

def who_on_strike(list_of_batsman):
    """
    Function to determine who is on strike.
    Returns index of batsman currently on strike.
    """
    for i in range(len(list_of_batsman)):
        if list_of_batsman[i][2]:
            return i

def who_on_non_strike(list_of_batsman):
    """
    Function to determine who is on non-strike.
    Returns index of batsman currently not on strike.
    """
    for i in range(len(list_of_batsman)):
        if not list_of_batsman[i][2] and list_of_batsman[i][3]==1:
            return i

def order_of_batsman():
    """
    Returns probability run list based on batting position.
    """
    top_order_run_list=[0,1,2,4,4,5,6,0,4,2,4,5,6,4,6,4,2,6,4,6]
    mid_order_run_list=[0,1,2,4,4,5,0,1,2,6,4,5,6,3,2,4,3,4,4,4]
    low_order_run_list=[0,1,2,4,4,5,6,4,1,2,0,2,5,2,3,2,3,2,1,4]
    end_order_run_list=[0,1,2,3,4,5,6,0,1,2,2,1,4,6,4,5,5,5,0,0]

    striker= who_on_strike(batsman_stats_list)

    if striker <3:
        return top_order_run_list
    elif striker <5:
        return mid_order_run_list
    elif striker <7:
        return low_order_run_list
    else:
        return end_order_run_list

def run_scored():
    """
    Returns random run based on batsman order probability.
    """
    order=order_of_batsman()
    return order[random.randint(0,19)]

def total_players_out():
    """
    Returns total number of wickets fallen.
    """
    total_out=0
    for i in range(0,11):
        if batsman_stats_list[i][3]==-1:
            total_out+=1
    return total_out

def batsman_out():
    """
    Handles batsman getting out and brings next batsman.
    """
    striker= who_on_strike(batsman_stats_list)
    print("Out", end=" ")
    batsman_stats_list[striker][1] += ball_order
    print(f"{batsman_stats_list[striker][0]}/{batsman_stats_list[striker][1]:>1}", end=" ")
    batsman_stats_list[striker][2]=False
    batsman_stats_list[striker][3]=-1

    if total_players_out()<10:
        next_batsman()

def next_batsman():
    """
    Sends next batsman to crease.
    """
    for i in range(len(batsman_stats_list)):
        if batsman_stats_list[i][3] == 0:
            batsman_stats_list[i][2] = True
            batsman_stats_list[i][3] = 1
            return

def strike_changer():
    """
    Swaps strike between striker and non-striker.
    """
    striker = who_on_strike(batsman_stats_list)
    non_striker = who_on_non_strike(batsman_stats_list)
    batsman_stats_list[striker][2], batsman_stats_list[non_striker][2] = batsman_stats_list[non_striker][2], batsman_stats_list[striker][2]

def batsman_run_adder(run):
    """
    Adds runs to striker and updates balls.
    """
    striker = who_on_strike(batsman_stats_list)
    print(f"{run:>3}", end=" ")
    batsman_stats_list[striker][0] += run
    batsman_stats_list[striker][1] += ball_order

    if run % 2 == 1:
        strike_changer()

def update_batsman_stats(run_output):
    """
    Updates batsman stats for each delivery.
    """
    if run_output==5:
        batsman_out()
    else:
        batsman_run_adder(run_output)

def update_bowler_stats(ball_order,bowler,run_output):
    """
    Updates bowler stats after every ball.
    """
    if run_output==5:
        bowler_stats_list[bowler-1][2]+=1
    elif not run_output:
        bowler_stats_list[bowler-1][3]+=ball_order
    else:
        bowler_stats_list[bowler-1][1]+=run_output

    bowler_stats_list[bowler-1][0]+=ball_order

[
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


target=0
inning=0

while inning<2:

    # Reset stats for each innings
    bowler_stats_list=[[0,0,0,0] for _ in range(5)]
    batsman_stats_list=[[0,0,True,1],[0,0,False,1],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0],[0,0,False,0]]

    # Loop over 20 overs
    for i in range (0,20):

        # Death overs aggression
        ball_order = 1 if (i== 17 or i==19) else 2
        bowler=bowling_order[i]

        # Loop through balls in over
        for ball_num in range (0,6,ball_order):

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

    # Batting scorecard
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

    # Bowling scorecard
    print("\nBowling Stats\n")
    print("Bowler\tRuns Given\tBalls Bowled\tWickets Taken\tDot Balls")

    for index,stats in enumerate(bowler_stats_list):
        print(f"Bowler {index + 1}\t{stats[1]}\t\t{stats[0]}\t\t{stats[2]}\t\t{stats[3]}")

    # Match result
    if inning==1 and total_runs>=target:
        print("\nTarget Achieved! It was a succesful chase.")
    elif inning==1 and total_runs==target-1:
        print("\n The fabulous chase fell short by 1 run.")
    elif inning==1:
        print("\n The chasing team couldn't chase the target.")

    if inning==0:
        target=total_runs+1

    inning+=1