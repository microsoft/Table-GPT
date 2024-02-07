from ..base.base_task_descriptor import BaseTaskDescriptor
import pandas as pd
import json
def get_examples():
    # stack 
    column_names = ["Product", "Product Category", "Store", "19-Oct", "20-Oct", "21-Oct", "22-Oct", "23-Oct"]
    rows = [
            ["Huffy 18 in. Boys Bike", "Sports", "s_sk_101", "5", "3", "4", "15", "19"],
            ["Kent 18 In. Boy's BMX Bike", "Sports", "s_sk_101", "8", "5", "11", "12", "8"],
            ["HP 11 in. Chromebook 16W64", "Electronics", "s_sk_102", "17", "9", "14", "5", "19"],
    ]
    stack_df = pd.DataFrame(rows, columns=column_names)
    stack_gt = {"transformation": "stack", "stack_start_idx": 3, "stack_end_idx": 7}
    
    # wide_to_long 
    column_names = ["Country", "Region", "2018 - Revenue ($K)", "2018 - Units Sold", "2018 - Margin %", "2019 - Revenue ($K)", "2019 - Units Sold", "2019 - Margin %", "2020 - Revenue ($K)", "2020 - Units Sold", "2020 - Margin %"]
    rows = [
            ["Albania", "Europe", "$10 ", "224", "4%", "$12 ", "269", "4%", "$16 ", "350", "4%"],
            ["Australia", "Asia Pacific", "$2,492 ", "54824", "13%", "$2,990 ", "65789", "14%", "$3,888 ", "85525", "16%"],
            ["Argentina", "South America", "$495 ", "10890", "9%", "$594 ", "13068", "11%", "$772 ", "16988", "13%"],
    ]
    wide_to_long_df = pd.DataFrame(rows, columns=column_names)
    wide_to_long_gt = {"transformation": "wide_to_long", "wide_to_long_start_idx": 2, "wide_to_long_end_idx": 10}

    # pivot
    column_names = ["name"]
    rows = [
            ["Found: 21-Oct-19 10:21:14"],
            ["Title: Canon EF 100mm f/2.8L Macro IS USM"],
            ["Price: 6900 kr"],
            ["Link: https://www.finn.no/"],
            ["Found: 21-Oct-19 10:21:15"],
            ["Title: Canon EF 85mm f/1.8 USM Medium"],
            ["Price: 7500 kr"],
            ["Link: https://www.finn.no/"],
            ["Found: 21-Oct-19 10:22:46"],
            ["Title: Panasonic Lumix G 25mm F1.4 ASPH"],
            ["Price: 3200 kr"],
            ["Link: https://www.finn.no/"],
    ]
    pivot_df = pd.DataFrame(rows, columns=column_names)
    pivot_gt = {"transformation": "pivot", "pivot_row_frequency": 4}
    
    # transpose
    column_names = ["", "HOTEL MISION JURIQUILLA ", "RAMADA ENCORE HOTEL", "FOUR POINTS BY SHERATON"]
    rows = [
            ["Single Room", "1030", "920", "1150", ],
            ["Lodging tax", "2.50%", "3.50%", "3.50%"],
            ["Address", "Centro, cp. 76000", "Juriquilla, C.P. 76230", "Jurica, C.P. 76127"],
            ["Phone", "(442) 234-0000 ex. 547", "(442) 690-9400", "(4429 103-3030"],
    ]
    transpose_df = pd.DataFrame(rows, columns=column_names)
    transpose_gt = {"transformation": "transpose"}
    
    # explode
    column_names = ["id", "date", "items"]
    rows = [
            ["1", "2021-01-01", "apple, banana, orange"], 
            ["2", "2022-12-12", "banana, carrot"], 
    ]
    explode_df = pd.DataFrame(rows, columns=column_names)
    explode_gt = {"transformation": "explode", "explode_column_idx": 2}
    
    
    # ffill
    column_names = ["year", "cnt"]
    rows = [
            [2022, 2],
            ["", 4],
            [2023, 5],
            ["", 3],
			[2024, 2],
            ["", 4],
    ]
    ffill_df = pd.DataFrame(rows, columns=column_names)
    ffill_gt = {"transformation": "ffill", "ffill_end_idx": 0}

    # subtitles
    column_names = ["year", "cnt"]
    rows = [
            ["microsoft", ""],
            ["2021", "4"],
            ["2022", "5"],
            ["oracle", ""],
            ["2021", "11"],
            ["2022", "329"]
    ]
    subtitle_df = pd.DataFrame(rows, columns=column_names)
    subtitle_gt = {"transformation": "subtitle"}
    
    examples = {
        "stack": [stack_df, stack_gt],
        "wide_to_long": [wide_to_long_df, wide_to_long_gt],
        "transpose": [transpose_df, transpose_gt],
        "pivot": [pivot_df, pivot_gt],
        "ffill": [ffill_df, ffill_gt],
        "explode": [explode_df, explode_gt],
        "subtitle": [subtitle_df, subtitle_gt],
    }
    return examples


class TTFTaskDescriptor(BaseTaskDescriptor):
    # decribe em task using natural language
    def __init__(self, missing_token="[MISSING]", **kwargs):
        super().__init__(**kwargs)
        self.missing_token = missing_token
        
    def get_task_description(self, random_state=None):
        op_params_descr = [
            "- stack: collapse homogeneous cols into rows.",
            "@param (int): stack_start_idx: zero-based starting column index of the homogeneous column-group.",
            "@param (int): stack_end_idx: zero-based ending column index of the homogeneous column-group.\n",
            "- wide_to_long: collapse repeating col-groups into rows.",
            "@param (int): wide_to_long_start_idx: zero-based starting column index of the repeating col-groups.",
            "@param (int): wide_to_long_end_idx: zero-based ending column index of the repeating col-groups.\n",
            "- transpose: convert rows to columns and vice versa.\n",
            "- pivot: pivot repeating row-groups into cols.",
            "@param (int): pivot_row_frequency: frequency of repeating row-groups.\n",
            "- ffill: fill structurally empty cells in tables.",
            "@param (int): ffill_end_idx: zero-based ending column index of the columns to be filled.\n",
            "- explode: convert composite cells into atomic values",
            "@param (int): explode_column_idx: zero-based column index of the column to be exploded.\n",
            "- subtitle: convert table subtitles into a column.\n\n"
        ]
        op_params_descr = "\n".join(op_params_descr)
        
        examples = get_examples()
        example_text = []
        for name, (df, gt) in examples.items():
            row = []
            row.append(f"Example of {name}:")
            row.append(f"## Input")
            row.append(self.serializer.serialize_df(df))
            row.append(f"## Output")
            row.append(json.dumps(gt))
            example_text.append("\n".join(row))
        example_text = "\n-------\n".join(example_text)
        
        descriptions = [
            'Given a markdown table, predict what python pandas transformation may be needed on the given input table. Valid choices for transformation include: {"stack", "wide_to_long", "transpose", "pivot", "explode", "ffill", "subtitles"}. Note that each of these is a common Python Pandas operator. ' 
            'Some transformations can have parameters. Each transformation and its parameters are describe as follows.\n\n'
            f"{op_params_descr}"
            'OUTPUT the predicted transformation name along with its parameters for the given INPUT table in a JSON, e.g., {"transformation": "stack", "stack_start_idx": 1, "stack_end_idx": 5}. '
            'If the input table needs multi-step transformations (e.g, ffill followed by stack), list JSON of each transformation sequentially in a list, e.g., [{"transformation": "ffill", "ffill_end_idx": 1}, {"transformation": "stack", "stack_start_idx": 1, "stack_end_idx": 5}]. No explanation is needed.\n\n'
            '=========\n'
            'Here are some example inputs and outputs for each transformation.\n'
            f'{example_text}\n'
            '=========\n'
            "Your task:"
        ]
        return self.select_one_option(descriptions, random_state=random_state)
        
    def get_input(self, df, random_state=None):
        return self.serializer.serialize_df(df)
    
    def get_output(self, y):
        return json.dumps(y)