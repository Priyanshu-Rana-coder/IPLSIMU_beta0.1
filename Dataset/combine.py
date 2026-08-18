import pandas as pd
import os
folder = os.path.dirname(os.path.abspath(__file__))
for i in range(1, 5):
    input_file = os.path.join(folder, f"dataset{i}.csv")
    output_file = os.path.join(folder, f"labeled_dataset{i}.csv")
    df = pd.read_csv(input_file)
    labeled = df[(df["intent"] != 0) & (df["risk"] != 0)]
    labeled.to_csv(output_file, index=False)
    print(f"dataset{i}: {len(labeled)} labeled points")