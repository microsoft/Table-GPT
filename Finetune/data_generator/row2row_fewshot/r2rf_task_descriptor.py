from ..base.base_task_descriptor import BaseTaskDescriptor
import pandas as pd
import numpy as np

class R2RFTaskDescriptor(BaseTaskDescriptor):
    def __init__(self, instruction=None, **kwargs):
        super().__init__(**kwargs)
        self.instruction = instruction
        
    def _get_task_description(self, random_state=None):
        descriptions = [
            "You are given a table of inputs and outputs in two columns. Please figure out the patterns between inputs and outputs from the first few rows and then determine the output value for the last row (denoted by '[Output Value]'). Please only return the output value.",
            "You've been provided with a table containing input-output pairs in two columns. Analyze the patterns between inputs and outputs from the initial rows and predict the value for the last row labeled as '[Output Value].' Please exclude any other information and provide the output value only.",
            "Use the table given with input-output data in two columns to identify the underlying patterns between them based on the initial rows. Afterward, calculate the output value for the last row marked as '[Output Value].' Share only the final output value and exclude any other details.",
            "Examine the table featuring inputs and outputs in two columns and identify patterns from the initial rows. Once patterns are determined, predict the value for the last row labeled as '[Output Value].' Present the output value exclusively and disregard all other information.",
            "Your task is to analyze the table of input-output pairs in two columns and establish patterns based on the first few rows. Afterward, compute the output value for the last row denoted as '[Output Value].' Limit your response to providing only the output value.",
            "Given a table with inputs and outputs in two columns, your goal is to deduce the patterns between them using the initial rows. Then, calculate the output value for the last row identified as '[Output Value].' Please return only the output value and omit all other information.",
            "Examine the table displaying inputs and outputs in two columns. Determine the patterns between them by observing the first few rows and predict the output value for the last row marked as '[Output Value].' Present the output value alone and exclude any additional details.",
            "Take a look at the table containing input-output data in two columns. Analyze the patterns based on the initial rows and compute the output value for the last row designated as '[Output Value].' Provide only the output value and do not include any other data.",
            "Your task involves analyzing the table of inputs and outputs in two columns to discover patterns from the initial rows. Subsequently, calculate the output value for the last row labeled as '[Output Value].' Share solely the output value and disregard any other information.",
            "Use the table given with input-output pairs in two columns to identify patterns based on the first few rows. Afterward, predict the value for the last row denoted as '[Output Value].' Please only return the output value and exclude all other details.",
            "You are presented with a table containing inputs and outputs in two columns. Your objective is to deduce the patterns between them from the initial rows and determine the output value for the last row labeled as '[Output Value].' Limit your response to providing only the output value and omitting any other information.",
            "Given a table with inputs and outputs in two columns, your task is to analyze the patterns between them using the first few rows. Then, calculate the output value for the last row denoted as '[Output Value].' Please provide only the output value and exclude any additional data.",
            "Examine the table featuring input-output pairs in two columns and identify patterns based on the initial rows. Once patterns are determined, predict the output value for the last row marked as '[Output Value].' Share only the final output value and disregard any other details.",
            "Your goal is to analyze the table of inputs and outputs in two columns and establish patterns from the initial rows. Afterward, compute the output value for the last row denoted as '[Output Value].' Limit your response to providing only the output value.",
            "Given a table displaying inputs and outputs in two columns, your task is to deduce the patterns between them by observing the first few rows. Then, calculate the output value for the last row identified as '[Output Value].' Please return only the output value and omit all other information.",
            "Examine the table containing input-output data in two columns. Determine the patterns between them by observing the first few rows and predict the output value for the last row designated as '[Output Value].' Present the output value alone and exclude any additional details.",
            "Take a look at the table of inputs and outputs in two columns. Analyze the patterns based on the initial rows and compute the output value for the last row labeled as '[Output Value].' Provide only the output value and do not include any other data.",
            "Your task involves analyzing the table of input-output pairs in two columns to discover patterns from the initial rows. Subsequently, calculate the output value for the last row labeled as '[Output Value].' Share solely the output value and disregard any other information.",
            "Use the table given with inputs and outputs in two columns to identify patterns based on the first few rows. Afterward, predict the value for the last row denoted as '[Output Value].' Please only return the output value and exclude all other details.",
            "You are presented with a table containing inputs and outputs in two columns. Your objective is to deduce the patterns between them from the initial rows and determine the output value for the last row labeled as '[Output Value].' Limit your response to providing only the output value and omitting any other information.",
            "Given a table with inputs and outputs in two columns, your task is to analyze the patterns between them using the first few rows. Then, calculate the output value for the last row denoted as '[Output Value].' Please provide only the output value and exclude any additional data.",
            "The task requires you to study a table consisting of inputs and outputs in two columns. Find the patterns between inputs and outputs based on the initial rows and deduce the output value for the last row marked as '[Output Value].' Please share only the output value and nothing else.",
            "You have been given a table with input-output data in two columns. Analyze the patterns observed in the initial rows to predict the output value for the last row designated as '[Output Value].' Your response should contain only the output value, excluding any other details.",
            "Examine the table containing inputs and outputs in two columns. By studying the first few rows, determine the patterns between them and calculate the output value for the last row identified as '[Output Value].' Provide solely the output value and disregard any additional information.",
            "Given a table with inputs and outputs in two columns, your objective is to identify patterns based on the initial rows. Subsequently, predict the value for the last row labeled as '[Output Value].' Please return only the output value and omit all other information.",
            "Analyze the table displaying input-output pairs in two columns and establish patterns from the initial rows. Afterward, compute the output value for the last row denoted as '[Output Value].' Share only the final output value and disregard any other details.",
            "Your task is to analyze the table of inputs and outputs in two columns to discover patterns from the first few rows. Then, calculate the output value for the last row marked as '[Output Value].' Limit your response to providing only the output value and excluding any other information.",
            "Use the table given with input-output data in two columns to identify patterns based on the initial rows. Afterward, predict the output value for the last row denoted as '[Output Value].' Please only return the output value and exclude all other details.",
            "You are presented with a table containing input-output pairs in two columns. Your goal is to deduce the patterns between them from the initial rows and determine the output value for the last row labeled as '[Output Value].' Limit your response to providing only the output value and omitting any other information.",
            "Given a table featuring inputs and outputs in two columns, your task is to analyze the patterns between them using the first few rows. Then, calculate the output value for the last row identified as '[Output Value].' Please provide only the output value and exclude any additional data.",
            "Examine the table of inputs and outputs in two columns. Determine the patterns based on the initial rows and compute the output value for the last row labeled as '[Output Value].' Provide only the output value and do not include any other data.",
            "Your task involves analyzing the table of input-output pairs in two columns to discover patterns from the initial rows. Subsequently, calculate the output value for the last row labeled as '[Output Value].' Share solely the output value and disregard any other information.",
            "Use the table given with inputs and outputs in two columns to identify patterns based on the first few rows. Afterward, predict the value for the last row denoted as '[Output Value].' Please only return the output value and exclude all other details.",
            "You are presented with a table containing inputs and outputs in two columns. Your objective is to deduce the patterns between them from the initial rows and determine the output value for the last row labeled as '[Output Value].' Limit your response to providing only the output value and omitting any other information.",
            "Given a table with inputs and outputs in two columns, your task is to analyze the patterns between them using the first few rows. Then, calculate the output value for the last row denoted as '[Output Value].' Please provide only the output value and exclude any additional data.",
            "Examine the table featuring input-output data in two columns. Determine the patterns between them by observing the first few rows and predict the output value for the last row designated as '[Output Value].' Present the output value alone and exclude any additional details.",
            "Take a look at the table of inputs and outputs in two columns. Analyze the patterns based on the initial rows and compute the output value for the last row labeled as '[Output Value].' Provide only the output value and do not include any other data.",
            "Your task involves analyzing the table of input-output pairs in two columns to discover patterns from the initial rows. Subsequently, calculate the output value for the last row labeled as '[Output Value].' Share solely the output value and disregard any other information.",
            "Use the table given with inputs and outputs in two columns to identify patterns based on the first few rows. Afterward, predict the value for the last row denoted as '[Output Value].' Please only return the output value and exclude all other details.",
            "You are presented with a table containing inputs and outputs in two columns. Your objective is to deduce the patterns between them from the initial rows and determine the output value for the last row labeled as '[Output Value].' Limit your response to providing only the output value and omitting any other information.",
            "Given a table with inputs and outputs in two columns, your task is to analyze the patterns between them using the first few rows. Then, calculate the output value for the last row denoted as '[Output Value].' Please provide only the output value and exclude any additional data.",
        ]
        desc = self.select_one_option(descriptions, random_state=random_state)
        if self.instruction is not None:
            desc += f" (Hint: {self.instruction})"
        return desc
    
    def get_input(self, df, random_state=None):
        if random_state is not None:
            np.random.seed(random_state)
        
        df_ex = df.copy()
        df_ex.iloc[-1]["Output"] = "[Output Value]"
        prompt = self.serializer.serialize_df(df_ex)
        return prompt
    
    def get_output(self, y):
        answer = str(y["label"])
        answer = self.answer_to_json(answer)
 
        if y["cot"] is not None:
            cot_text = y["cot"].strip()
            completion = f"{cot_text} Therefore, the final answer is {answer}."
        else:
            completion = answer
        return completion
    
    def get_output_example(self):
        return "output_value", "<output value transformed from the input value>"