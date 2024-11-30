import pandas as pd


class Processor:
    def __init__(self, jsonchik):
        self.jsonchik = jsonchik

    def process(self):
        df = pd.json_normalize(self.jsonchik)
        print(df)
        return df
