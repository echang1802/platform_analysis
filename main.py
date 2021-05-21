
from platform_analysis import simulator, campaign_control
import pandas as pd

if __name__ == "__main__":

    sim = simulator(pd.read_csv("data/test_data.csv"))
    periods, reached = sim.simulate(users = {
        "money_size" : 100,
        "subsidy_size" : 100
    }, campaigns = campaign_control(100),
    periods_to_evolve = 2)

    if reached:
        print(f"Total periods needed to reach critical mass: {periods}")
    else:
        print(f"In {periods} periods the critical mass wasn't reached")
