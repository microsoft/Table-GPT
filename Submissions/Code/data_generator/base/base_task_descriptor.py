from .table_serializer import *
import numpy as np
import json

class BaseTaskDescriptor(object):
    def __init__(self, serializer="markdownshort", random_state=1, use_random_description=False, use_cot=False, use_format_suffix=True):
        if serializer == "stanford":
            self.serializer = TextSerializer()
        elif serializer == "markdown":
            self.serializer = MarkdownSerializer()
        elif serializer == "markdownshort":
            self.serializer = MarkdownShortSerializer()
        elif serializer == "markdownshortline":
            self.serializer = MarkdownShortLineSerializer()
        elif serializer == "html":
            self.serializer = HTMLSerializer()
        elif serializer == "json":
            self.serializer = JsonSerializer()
        elif serializer == "keyvalue":
            self.serializer = KeyValueSerializer()
        elif serializer == "csv":
            self.serializer = CSVSerializer()
        else:
            raise Exception("Wrong serializer", serializer)
        
        self.use_random_description = use_random_description
        self.random_state = random_state
        self.use_cot = use_cot
        self.use_format_suffix = use_format_suffix
    
    def get_task_description(self, random_state):
        desc = self._get_task_description(random_state=random_state)
        if self.use_format_suffix:
            desc = self.add_format_suffix(desc)
        if self.use_cot:
            desc += "  Let's think step by step and show your reasoning before showing the final result."
        return desc
    
    def _get_task_description(self):
        raise Exception("Not implemented")
    
    def get_input(self, data):
        raise Exception("Not implemented")
    
    def _get_output(self, y):
        raise Exception("Not implemented")
    
    def get_output(self, y):
        answer = self._get_output(y)
        return self.answer_to_json(answer)
    
    def get_output_example(self):
        raise Exception("Not implemented")
    
    def select_one_option(self, options, random_state=None):
        if not self.use_random_description:
            return options[0]
        else:
            if random_state is not None:
                np.random.seed(random_state)
            idx = np.random.choice(len(options))
            return options[idx]
    
    def add_format_suffix(self, desc):
        key, placeholder = self.get_output_example()
        if len(desc) > 0 and desc[-1] != "\n":
            desc += " "
        text = f"{desc}Return the final result as JSON in the format {self.answer_to_json(placeholder)}."
        return text
        
    def answer_to_json(self, answer):
        key, placeholder = self.get_output_example()
        return json.dumps({key: answer})
    