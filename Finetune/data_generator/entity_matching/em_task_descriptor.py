from ..base.base_task_descriptor import BaseTaskDescriptor
import numpy as np
import json

class EMTaskDescriptor(BaseTaskDescriptor):
    # decribe em task using natural language
    def __init__(self, topic="Entity", **kwargs):
        super().__init__(**kwargs)
        self.topic = topic
        self.entity_1, self.entity_2 = self.get_entity_names(random_state=self.random_state)
        
    def get_entity_names(self, random_state=None):
        pairs = [
            (f"{self.topic} A", f"{self.topic} B"),
            (f"{self.topic} 1", f"{self.topic} 2"),
            (f"{self.topic} I", f"{self.topic} II"),
            (f"the First {self.topic}", f"the Second {self.topic}"),
            (f"{self.topic} (1)", f"{self.topic} (2)"),
        ]
        return self.select_one_option(pairs, random_state=random_state)
        
    def _get_task_description(self, random_state=None):
        descriptions = [
            f"Please determine whether {self.entity_1} and {self.entity_2} refer to the same entity or not. Your final answer should be 'Yes' or 'No'.",
            f"Kindly ascertain whether {self.entity_1} and {self.entity_2} pertain to the identical entity or not. Provide your ultimate response as either 'Yes' or 'No'.",
            f"I request you to establish if {self.entity_1} and {self.entity_2} are referring to the same entity. State your final answer as 'Yes' or 'No'.",
            f"Please determine if {self.entity_1} and {self.entity_2} denote the same entity. Your conclusive answer should be 'Yes' or 'No'.",
            f"Could you confirm whether {self.entity_1} and {self.entity_2} point to the same entity or not? Indicate your final response as either 'Yes' or 'No'.",
            f"We need to establish if {self.entity_1} and {self.entity_2} represent the same entity. Provide your ultimate answer as 'Yes' or 'No'.",
            f"I would like you to determine whether {self.entity_1} and {self.entity_2} are referring to the same entity or not. Please respond with 'Yes' or 'No'.",
            f"It is essential to ascertain if {self.entity_1} and {self.entity_2} refer to the same entity. Your final response should be 'Yes' or 'No'.",
            f"Please verify whether {self.entity_1} and {self.entity_2} are denoting the same entity. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Let's determine if {self.entity_1} and {self.entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to confirm whether {self.entity_1} and {self.entity_2} represent the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Could you establish if {self.entity_1} and {self.entity_2} are referring to the same entity or not? Indicate your final response as either 'Yes' or 'No'.",
            f"We need to verify if {self.entity_1} and {self.entity_2} denote the same entity. Provide your ultimate answer as 'Yes' or 'No'.",
            f"I would like you to ascertain whether {self.entity_1} and {self.entity_2} are referring to the same entity or not. Your final response should be 'Yes' or 'No'.",
            f"It is crucial to determine if {self.entity_1} and {self.entity_2} represent the same entity. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Please confirm whether {self.entity_1} and {self.entity_2} are denoting the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Let's verify if {self.entity_1} and {self.entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to establish whether {self.entity_1} and {self.entity_2} represent the same entity or not. Indicate your final response as either 'Yes' or 'No'.",
            f"Could you determine if {self.entity_1} and {self.entity_2} are referring to the same entity or not? Provide your ultimate answer as 'Yes' or 'No'.",
            f"We need to ascertain if {self.entity_1} and {self.entity_2} denote the same entity. Your final response should be 'Yes' or 'No'.",
            f"I would like you to verify whether {self.entity_1} and {self.entity_2} are referring to the same entity or not. Your final response should be 'Yes' or 'No'.",
            f"Please determine whether {self.entity_1} and {self.entity_2} refer to the same entity or not. Your final answer should be 'Yes' or 'No'.",
            f"I request you to establish if {self.entity_1} and {self.entity_2} denote the same entity. State your final answer as 'Yes' or 'No'.",
            f"Could you confirm whether {self.entity_1} and {self.entity_2} point to the same entity or not? Indicate your final response as either 'Yes' or 'No'.",
            f"We need to establish if {self.entity_1} and {self.entity_2} represent the same entity. Provide your ultimate answer as 'Yes' or 'No'.",
            f"I would like you to determine whether {self.entity_1} and {self.entity_2} are referring to the same entity or not. Please respond with 'Yes' or 'No'.",
            f"It is essential to ascertain if {self.entity_1} and {self.entity_2} refer to the same entity. Your final response should be 'Yes' or 'No'.",
            f"Please verify whether {self.entity_1} and {self.entity_2} are denoting the same entity or not. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Let's determine if {self.entity_1} and {self.entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to confirm whether {self.entity_1} and {self.entity_2} represent the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Could you establish if {self.entity_1} and {self.entity_2} are referring to the same entity or not? Provide your ultimate answer as 'Yes' or 'No'.",
            f"We need to verify if {self.entity_1} and {self.entity_2} denote the same entity. Your final response should be 'Yes' or 'No'.",
            f"I would like you to ascertain whether {self.entity_1} and {self.entity_2} are referring to the same entity or not. Your final response should be 'Yes' or 'No'.",
            f"It is crucial to determine if {self.entity_1} and {self.entity_2} represent the same entity. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Please confirm whether {self.entity_1} and {self.entity_2} are denoting the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Let's verify if {self.entity_1} and {self.entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to establish whether {self.entity_1} and {self.entity_2} represent the same entity or not. Indicate your final response as either 'Yes' or 'No'.",
            f"Could you determine if {self.entity_1} and {self.entity_2} are referring to the same entity or not? Provide your ultimate answer as 'Yes' or 'No'.",
            f"We need to ascertain if {self.entity_1} and {self.entity_2} denote the same entity. Your final response should be 'Yes' or 'No'.",
            f"I would like you to verify whether {self.entity_1} and {self.entity_2} are referring to the same entity or not. Your final response should be 'Yes' or 'No'.",
            f"It is essential to determine if {self.entity_1} and {self.entity_2} refer to the same entity. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Please verify whether {self.entity_1} and {self.entity_2} are denoting the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Let's determine if {self.entity_1} and {self.entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to confirm whether {self.entity_1} and {self.entity_2} represent the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Could you establish if {self.entity_1} and {self.entity_2} are referring to the same entity or not? Provide your ultimate answer as 'Yes' or 'No'.",
            f"We need to verify if {self.entity_1} and {self.entity_2} denote the same entity. Your final response should be 'Yes' or 'No'.",
        ]
        return self.select_one_option(descriptions, random_state=random_state)
    
    def get_input_suffix(self, name, random_state=None):
        suffix = [
            f"{name} is:",
            f"{name} can be described as:",
            f"{name} is shown as:",
            f"{name} can be represented as:",
            f"{name}:",
            f"{name} can be presented as follows.",
            f"Here is the description of {name}.",
            f"The below table depicts {name}.",
            f"The following table provides details of {name}.",       
        ]
        return self.select_one_option(suffix, random_state=random_state)
    
    def get_input(self, data, random_state=None):
        row_l, row_r = data
        l_text = self.serializer.serialize_row(row_l)
        r_text = self.serializer.serialize_row(row_r)
        
        if random_state is not None:
            np.random.seed(random_state)
        suffix_1 = self.get_input_suffix(self.entity_1, random_state=None)
        suffix_2 = self.get_input_suffix(self.entity_2, random_state=None)
        
        text = (
            f"{suffix_1}\n"
            f"{l_text}\n"
            f"{suffix_2}\n"
            f"{r_text}"
        )
        return text
    
    def get_output_example(self):
        return "answer", "<Yes or No>"
    
    def get_output(self, y):
        if y["label"] == "1":
            answer = "Yes"
        elif y["label"] == "0":
            answer = "No"
        else:
            raise Exception(f"invalid label {y['label']}")
        
        answer = self.answer_to_json(answer)
        
        if y["cot"] is not None:
            cot_text = y["cot"].strip()

            if cot_text[-1] != ".":
                cot_text += "."
                
            cot_text = cot_text.replace(f"{self.topic} A", self.entity_1).replace(f"{self.topic} B", self.entity_2)
            if y["cot_position"] == "before_answer":
                completion = f"{cot_text} Therefore, the final answer is {answer}."
            elif y["cot_position"] == "after_answer":
                completion = f"{answer}. {cot_text}"
            else:
                raise Exception(f"Wrong cot position {y['cot_position']}")
        else:
            completion = answer
            
        return completion