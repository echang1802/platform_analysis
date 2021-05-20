
from platform_analysis import simulator, campaign_control
import pandas as pd

if __name__ == "__main__":

    sim = simulator(pd.read_csv("data/test_data.csv"))
    periods = simulator.simulate({
        "money_size" : 100,
        "sudsidy_size" : 100
    }, campaign_control(100))

    print(f"Total periods needed to reach critical mass: {periods}")
