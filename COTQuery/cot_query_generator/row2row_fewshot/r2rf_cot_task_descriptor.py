import sys
sys.path.append("../Finetune")
from data_generator.row2row_fewshot.r2rf_task_descriptor import R2RFTaskDescriptor
import numpy as np

class R2RFCOTTaskDescriptor(R2RFTaskDescriptor):       
    def get_task_description(self, random_state=None):
        desc = super().get_task_description(random_state=random_state)
        cot_suffix = (
            " The correct answer has been given to you. Your task is to provide an explanation for the answer. Please keep the explanation brief and focus on the main points. Specifically, you should explain the pattern between an input value and an output value. Please think step by step."
            ' Return your explanation in JSON following the format {"explanation": "<YOUR EXPLANATION>"}.'
        )
        cot_desc = desc + cot_suffix
        return cot_desc