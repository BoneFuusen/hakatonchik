import pandas as pd
import numpy as np


class Processor:
    def __init__(self, json: dict | list[dict]):
        self.json = json

    def preprocess(self):
        df = pd.json_normalize(self.json)

        segment = ["Малый бизнес", "Средний бизнес", "Крупный бизнес"]
        role = ["ЕИО", "Сотрудник"]
        available_methods = ["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"]

        count = 1 if isinstance(self.json, dict) else len(self.json)
        segment_one_hot = np.zeros((count, len(segment)), dtype=np.int8)
        role_one_hot = np.zeros((count, len(role)), dtype=np.int8)
        available_methods_one_hot = np.zeros((count, len(available_methods)), dtype=np.int8)

        for i in range(len(df)):
            row = df.iloc[i]
            segment_one_hot[i][segment.index(row["segment"])] += 1
            role_one_hot[i][role.index(row["role"])] += 1
            for method in row["availableMethods"]:
                available_methods_one_hot[i][available_methods.index(method)] += 1

        df["mobileApp"] = df["mobileApp"].astype(int)

        df.drop("segment", axis=1, inplace=True)
        df[list(map(lambda x: "segment." + x, segment))] = segment_one_hot

        df.drop("role", axis=1, inplace=True)
        df[list(map(lambda x: "role." + x, role))] = role_one_hot

        df.drop("currentMethod", axis=1, inplace=True)

        df.drop("availableMethods", axis=1, inplace=True)
        df[list(map(lambda x: "available_methods." + x, available_methods))] = available_methods_one_hot

        df.drop("clientId", axis=1, inplace=True)
        df.drop("organizationId", axis=1, inplace=True)

        return df
