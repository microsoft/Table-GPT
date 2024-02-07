from ..base.base_task_descriptor import BaseTaskDescriptor
# https://huggingface.co/datasets/glue

class GlueTaskDescriptor(BaseTaskDescriptor):
    def __init__(self, task=None, **kwargs):
        super().__init__(**kwargs)
        self.task = task

    def _get_task_description(self, random_state=None):
        if self.task == "cola":
            desc = "Please determine whether the input sentence makes sense or not. Your final answer should be 'Yes' or 'No'."
        elif self.task == "mrpc":
            desc = "Given two sentences, please determine whether Sentence 1 and Sentence 2 mean the same thing. Your final answer should be 'Yes' or 'No'."
        elif self.task == "qnli":
            desc = "Given a question and a response, please determine whether the response answers the question. Your final answer should be 'Yes' or 'No'."
        elif self.task == "qqp":
            desc = "Given two questions, please determine whether Question 1 and Question 2 are semantically equivalent. Your final answer should be 'Yes' or 'No'."
        elif self.task == "rte":
            desc = "Given two sentences, please determine whether the meaning of one sentence is entailed from another. Your final answer should be 'Yes' or 'No'."
        elif self.task == "sst2":
            desc = "Please determine whether the input sentence is positive or negative. Your final answer should be 'Positive' or 'Negative'."
        elif self.task == "wnli":
            desc = "Given two sentences, please determine whether Sentence 2 is entailed by Sentence 1. Your final answer should be 'Yes' or 'No'."
        elif "mnli" in self.task:
            desc = "Given a premise sentence and a hypothesis sentence, please determine whether the premise entails the hypothesis (entailment), contradicts the hypothesis (contradiction), or neither (neutral). Your final answer should be 'Entailment', 'Contradiction' or 'Neutral'."
        else:
            raise

        descriptions = [desc]
        return self.select_one_option(descriptions, random_state=random_state)

    def get_input(self, data, random_state=None):
        if self.task == "cola":
            return data["sentence"]
        elif self.task == "mrpc":
            text = (
                f'Sentence 1: {data["sentence1"]}\n'
                f'Sentence 2: {data["sentence2"]}'
            )
            return text
        elif self.task == "qnli":
            text = (
                f'Question: {data["question"]}\n'
                f'Response: {data["sentence"]}'
            )
            return text
        elif self.task == "qqp":
            text = (
                f'Question 1: {data["question1"]}\n'
                f'Question 2: {data["question2"]}'
            )
            return text
        elif self.task == "rte":
            text = (
                f'Sentence 1: {data["sentence1"]}\n'
                f'Sentence 2: {data["sentence2"]}'
            )
            return text
        elif self.task == "wnli":
            text = (
                f'Sentence 1: {data["sentence1"]}\n'
                f'Sentence 2: {data["sentence2"]}'
            )
            return text
        elif "mnli" in self.task:
            text = (
                f'Premise: {data["premise"]}\n'
                f'Hypothesis: {data["hypothesis"]}'
            )
            return text
        elif self.task == "sst2":
            return data["sentence"]
        else:
            raise
    
    def _get_output(self, y):
        if self.task in ["cola", "mrpc", "qnli", "qqp", "wnli"]:
            if y["label"] == 0:
                return "No"
            elif y["label"] == 1:
                return "Yes"
            else:
                raise Exception(f"Wrong label {y['label']}.")
        elif self.task == "rte":
            if y["label"] == 0:
                return "Yes"
            elif y["label"] == 1:
                return "No"
            else:
                raise Exception(f"Wrong label {y['label']}.")
        elif self.task == "sst2":
            if y["label"] == 0:
                return "Negative"
            elif y["label"] == 1:
                return "Positive"
            else:
                raise Exception(f"Wrong label {y['label']}.")
        elif "mnli" in self.task:
            if y["label"] == 0:
                return 'Entailment'
            elif y["label"] == 1:
                return "Neutral"
            elif y["label"] == 2:
                return 'Contradiction'
            else:
                raise Exception(f"Wrong label {y['label']}.")            
        else:
            raise

    def get_output_example(self):
        if self.task in ["cola", "mrpc", "qnli", "qqp", "rte", "wnli"]:
            return "answer", "<Yes or No>"
        elif self.task == "sst2":
            return "answer", "<Positive or Negative>"
        elif "mnli" in self.task:
            return "answer", "<Entailment or Contradiction or Neutral>"
        else:
            raise

    