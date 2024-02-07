import sys
sys.path.append("../Finetune")
from data_generator.entity_matching.em_task_descriptor import EMTaskDescriptor
import numpy as np

class EMCOTTaskDescriptor(EMTaskDescriptor):  
    def get_task_description(self, random_state=None):
        desc = super().get_task_description(random_state=random_state)
        cot_suffix = "Please show your reasoning to justify your answer before giving the final answer."
        cot_desc = desc + cot_suffix
        return cot_desc