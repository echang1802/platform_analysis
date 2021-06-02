
from platform_analysis import simulator, campaign_control
import pandas as pd

if __name__ == "__main__":

    sim = simulator(pd.read_csv("data/test_data.csv"))
    periods, reached, periods_stats = sim.simulate(campaigns = campaign_control(700),
                periods_to_evolve = 5)

    if reached:
        print(f"Total periods needed to reach critical mass: {periods}")
    else:
        print(f"In {periods} periods the critical mass wasn't reached")

    periods_stats.to_csv("data/periods_stats.csv", index = False)
