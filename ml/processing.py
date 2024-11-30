import pandas as pd


class Processor:
    def __init__(self, json: dict | list[dict]):
        self.json = json

    def preprocess(self):
        df = pd.json_normalize(self.json)

        segment = ["Малый бизнес", "Средний бизнес", "Крупный бизнес"]
        role = ["ЕИО", "Сотрудник"]
        current_method = ["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"]
        available_methods = ["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"]

        segment_one_hot = [[0] * len(segment)]
        role_one_hot = [[0] * len(role)]
        current_method_one_hot = [[0] * len(current_method)]
        available_methods_one_hot = [[0] * len(available_methods)]

        for i in range(len(df)):
            row = df.iloc[i]
            segment_one_hot[i][segment.index(row["segment"])] += 1
            role_one_hot[i][role.index(row["role"])] += 1
            current_method_one_hot[i][current_method.index(row["currentMethod"])] += 1
            for method in row["availableMethods"]:
                available_methods_one_hot[i][available_methods.index(method)] += 1

        df["mobileApp"] = df["mobileApp"].astype(int)

        df.drop("segment", axis=1, inplace=True)
        df[list(map(lambda x: "segment." + x, segment))] = segment_one_hot

        df.drop("role", axis=1, inplace=True)
        df[list(map(lambda x: "role." + x, role))] = role_one_hot

        df.drop("currentMethod", axis=1, inplace=True)
        df[list(map(lambda x: "current_method." + x, current_method))] = current_method_one_hot

        df.drop("availableMethods", axis=1, inplace=True)
        df[list(map(lambda x: "available_methods." + x, available_methods))] = available_methods_one_hot

        df.drop("clientId", axis=1, inplace=True)
        df.drop("organizationId", axis=1, inplace=True)

        df["reason_category_type"] = None

        return df
