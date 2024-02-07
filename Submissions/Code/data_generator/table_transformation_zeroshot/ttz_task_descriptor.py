from ..base.base_task_descriptor import BaseTaskDescriptor
import json

class TTZTaskDescriptor(BaseTaskDescriptor):
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
        
        descriptions = [
            'Given a markdown table, predict what python pandas transformation may be needed on the given input table. Valid choices for transformation include: {"stack", "wide_to_long", "transpose", "pivot", "explode", "ffill", "subtitles"}. Note that each of these is a common Python Pandas operator. ' 
            'Some transformations can have parameters. Each transformation and its parameters are describe as follows.\n\n'
            f"{op_params_descr}"
            'OUTPUT the predicted transformation name along with its parameters for the given INPUT table in a JSON, e.g., {"transformation": "stack", "stack_start_idx": 1, "stack_end_idx": 5}. '
            'If the input table needs multi-step transformations (e.g, ffill followed by stack), list JSON of each transformation sequentially in a list, e.g., [{"transformation": "ffill", "ffill_end_idx": 1}, {"transformation": "stack", "stack_start_idx": 1, "stack_end_idx": 5}]. No explanation is needed.'
        ]
        return self.select_one_option(descriptions, random_state=random_state)
        
    def get_input(self, df, random_state=None):
        return self.serializer.serialize_df(df)
    
    def get_output(self, y):
        return json.dumps(y)