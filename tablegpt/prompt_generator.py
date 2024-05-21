import pandas as pd
import tiktoken
import numpy as np


class PromptGenerator(object):
    def __init__(
        self,
        table_task,
        drop_long_prompt=True,
        max_token_length=2048,
        min_fewshot_samples=1,
        random_state=1,
        use_random_template=False,
        use_cot=False,
        count_token_fn=None,
        use_format_suffix=True,
    ):
        self.table_task = table_task
        self.drop_long_prompt = drop_long_prompt
        self.max_token_length = max_token_length
        self.count_token_fn = count_token_fn
        self.min_fewshot_samples = min_fewshot_samples
        self.random_state = random_state
        self.use_random_template = use_random_template
        self.use_cot = use_cot
        self.use_format_suffix = use_format_suffix

    def generate_prompt(self, test_example, fewshot_examples):
        prev_prompt = None

        while True:
            if fewshot_examples is not None and len(fewshot_examples) > 0:
                prompt = self._generate_fewshot_prompt(test_example, fewshot_examples)
            else:
                prompt = self._generate_zeroshot_prompt(test_example)

            if self.check_prompt_length(prompt):
                return prompt

            if prompt == prev_prompt:
                # break if the prompt does not change after shortening
                break
            else:
                prev_prompt = prompt

            if (
                fewshot_examples is not None
                and len(fewshot_examples) > self.min_fewshot_samples
            ):
                # reduce fewshow samples to truncate prompt
                fewshot_examples = fewshot_examples[1:]
            else:
                test_example = self.table_task.shorten_data(test_example)
                fewshot_examples_shorten = [
                    self.table_task.shorten_data(example)
                    for example in fewshot_examples
                ]
                fewshot_examples = fewshot_examples_shorten

        # return None if the example can not be truncated
        if self.drop_long_prompt:
            return None
        else:
            print(
                "Warning: the prompt is longer than the max token and cannot be shortened."
            )
            return prompt

    def _get_output(self, test_example):
        if self.use_cot:
            return self.table_task.get_cot_output(test_example)
        else:
            return self.table_task.get_output(test_example)

    def generate_completion(self, test_example):
        completion = self._get_output(test_example)
        return completion

    def check_prompt_length(self, prompt):
        if self.count_token_fn is None:
            tokenizer = tiktoken.encoding_for_model("text-curie-001")
            token_ids = tokenizer.encode(prompt)
            token_length = len(token_ids) / 0.7
        else:
            token_length = self.count_token_fn(prompt)
        return token_length <= self.max_token_length

    def _generate_zeroshot_prompt(self, test_example):
        test_query = self.table_task.get_input(test_example)
        task_description = self._get_task_description(
            test_example, random_state=self.random_state
        )
        task_desc_title = self._get_task_desc_title(random_state=self.random_state)
        input_title, output_title = self._get_input_output_section_title_pair(
            random_state=self.random_state
        )
        suffix = self._get_suffix(test_example)
        prompt = (
            f"{task_desc_title} "
            f"{task_description}\n\n"
            f"{input_title}\n"
            f"{test_query.strip()}\n\n"
            f"{suffix}\n"
            f"{output_title}\n"
        )
        return prompt

    def _generate_fewshot_prompt(self, test_example, fewshot_examples):
        """fewshot_examples: a dataframe with multi-index (lid, rid, label).
        The columns from left and right table have suffix "_A" and "_B".
        """
        test_query = self.table_task.get_input(test_example)

        train_prompt_list = []
        for sample in fewshot_examples:
            query = self.table_task.get_input(sample)
            answer = self._get_output(sample)
            prompt = self._generate_fewshot_example_prompt(
                query, answer, random_state=self.random_state
            )
            train_prompt_list.append(prompt)

        task_description = self._get_task_description(
            test_example, random_state=self.random_state
        )
        task_desc_title = self._get_task_desc_title(random_state=self.random_state)
        input_title, output_title = self._get_input_output_section_title_pair(
            self.random_state
        )
        suffix = self._get_suffix(test_example)

        few_shot_text = []
        for ex in train_prompt_list:
            ex_text = f"{ex}"
            few_shot_text.append(ex_text)

        train_prompt = f"\n\n".join(few_shot_text)

        prompt = (
            f"{task_desc_title} "
            f"{task_description}\n\n"
            f"{train_prompt}\n\n"
            f"{input_title}\n"
            f"{test_query.strip()}\n\n"
            f"{suffix}\n"
            f"{output_title}\n"
        )
        return prompt

    def _get_suffix(self, test_example):
        suffix = ""
        if self.use_cot:
            suffix += f"Let's think step by step and show your reasoning before showing the final result."
        if self.use_format_suffix:
            format_suffix = self._get_format_suffix(test_example)
            if len(format_suffix) > 0:
                suffix += " " + format_suffix

        if len(suffix) > 0:
            suffix = suffix.strip()
            suffix += "\n"
        return suffix

    def _get_format_suffix(self, test_example):
        output_template = self.table_task.get_output_template(test_example)
        if output_template is None:
            return ""
        else:
            return f"Return the final result as JSON in the format {output_template}."

    def _get_input_output_section_title_pair(self, random_state=None):
        if self.random_state is not None:
            np.random.seed(random_state)
        titles = [
            ("## Input:", "## Output:"),
            ("Q:", "A:"),
            ("In:", "Out:"),
            ("Question:", "Answer:"),
            ("[Q]:", "[A]:"),
            ("Input:", "Output:"),
        ]
        return self._select_one_option(titles, random_state=random_state)

    def _get_task_desc_title(self, random_state=None):
        titles = [
            "# Task Description:",
            "Objective:",
            "Task:",
            "Description:",
            "Instruction:",
        ]
        return self._select_one_option(titles, random_state=random_state)

    def _generate_fewshot_example_prompt(self, query, answer, random_state=None):
        input_title, output_title = self._get_input_output_section_title_pair(
            random_state=random_state
        )
        prompt = (
            f"{input_title}\n" f"{query.strip()}\n\n" f"{output_title}\n" f"{answer}"
        )
        return prompt

    def _get_task_description(self, test_example, random_state=None):
        descriptions = self.table_task.get_task_descriptions(test_example)
        return self._select_one_option(descriptions, random_state=random_state)

    def _select_one_option(self, options, random_state=None):
        """Randomly select one choice from options"""
        if not self.use_random_template:
            return options[0]
        else:
            if random_state is not None:
                np.random.seed(random_state)
            idx = np.random.choice(len(options))
            return options[idx]
