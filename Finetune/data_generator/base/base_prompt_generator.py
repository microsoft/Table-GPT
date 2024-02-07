import pandas as pd
import tiktoken
import numpy as np

class BasePromptGenerator(object):
    def __init__(self, 
                 task_descriptor=None,
                 max_token_length=2048, 
                 min_fewshot_samples=3, 
                 random_state=1, 
                 use_random_template=False,
                 model_name="text-curie-001", 
                 prompt_ending="\n\n###\n\n", 
                 completion_ending="END",
                 use_system_message=False,
                 use_cot=False
                ):
        self.task_descriptor = task_descriptor
        self.max_token_length = max_token_length
        self.model_name = model_name
        self.prompt_ending = prompt_ending
        self.completion_ending = completion_ending
        self.min_fewshot_samples = min_fewshot_samples
        self.random_state = random_state
        self.use_random_template = use_random_template
        self.use_system_message = use_system_message
        self.use_cot = use_cot

    def generate_prompt(self, test_data, train_samples):
        stop_generate = False
        prev_prompt = ""
        
        while not stop_generate:
            if train_samples is None:
                prompt = self._generate_zeroshot_prompt(test_data) + self.prompt_ending
            else:
                prompt = self._generate_fewshot_prompt(test_data, train_samples) + self.prompt_ending
            
            if self.check_prompt_length(prompt):
                return prompt
            
            if len(prompt) == len(prev_prompt):
                break
            
            test_data, train_samples, stop_generate = self._shorten_input_data(test_data, train_samples)
            prev_prompt = prompt
            
        return None
    
    def generate_completion(self, y):
        completion = self._generate_completion(y)
        return  f" {completion} {self.completion_ending}"

    def check_prompt_length(self, prompt):
        tokenizer = tiktoken.encoding_for_model(self.model_name)
        token_ids = tokenizer.encode(prompt)
        return len(token_ids) <= (self.max_token_length * 0.7)
    
    def isna(self, value):
        return pd.isna(value) or str(value).strip() == "" or str(value).lower() == "nan"

    def _generate_zeroshot_prompt(self, test_data):
        """train_samples: a dataframe with multi-index (lid, rid, label). 
                            The columns from left and right table have suffix "_A" and "_B".
        """
        test_query = self.task_descriptor.get_input(test_data, random_state=self.random_state)
        prompt = self.format_zeroshot_prompt(test_query.strip(), random_state=self.random_state)        
        if self.use_system_message:
            system_message = self.get_system_message()
            prompt = f"{system_message}\n\n{prompt}"
        return prompt

    def _generate_fewshot_prompt(self, test_data, train_samples):
        """train_samples: a dataframe with multi-index (lid, rid, label). 
                            The columns from left and right table have suffix "_A" and "_B".
        """
        test_query = self.task_descriptor.get_input(test_data, random_state=self.random_state)
        
        train_prompt_list = []
        for i, (train_data, y) in enumerate(train_samples):
            query = self.task_descriptor.get_input(train_data, random_state=self.random_state)
            answer = self._generate_completion(y)  
            prompt = self.generate_fewshot_example_prompt(query, answer, random_state=self.random_state)
            train_prompt_list.append(prompt)
        
        prompt = self.format_fewshot_prompt(train_prompt_list, test_query)
        if self.use_system_message:
            system_message = self.get_system_message()
            prompt = f"{system_message}\n\n{prompt}"
        return prompt
    
    def _get_suffix(self):
        suffix = ""
        if self.use_cot:
            suffix += f"Let's think step by step and show your reasoning before showing the final result."
        if self.task_descriptor.use_format_suffix:
            suffix = self.task_descriptor.add_format_suffix(suffix) 
        if len(suffix) > 0:
            suffix += "\n"
        return suffix
    
    def _shorten_input_data(self, test_data, train_samples):
        # reduce samples in fewshot examples
        if train_samples is None or len(train_samples) <= self.min_fewshot_samples:
            return test_data, train_samples, True
    
        train_samples = train_samples[1:]
        return test_data, train_samples, False
    
    def _generate_completion(self, y) -> str:
        return self.task_descriptor.get_output(y)
    
    def lowercase_first_letter(self, x):
        res = x[0].lower() + x[1:]
        return res

    def get_system_message(self):
        text = (
            "# System Message:\n"
            "You are a helpful AI assistant that specializes in markdown tables. When you look at tables, you should look not only at rows, but also values in the same table column from different rows, which typically have homogeneous values drawn from the same domain. You will inspect tables carefully before answering any questions."
        )
        return text
    
    def get_input_section_title(self, random_state=None):
        titles = [
            "## Input:",
            "Q:",
            "In:",
            "Question:",
            "[Q]:",
            "Input Tables:",
            "Here are the inputs.",
            "The inputs of the problem are described as follows.",
            "The problem's inputs are shown as follows.",
            "The following provides details about the problem's inputs."
        ]
        return self.select_one_option(titles, random_state=random_state)
   
    def get_output_section_title(self, random_state=None):
        titles = [
            "## Output:",
            "A:",
            "Out:",
            "Answer:",
            "[A]:",
            "Result:",
            "Here is the output.",
            "The output of the problem should be:",
            "The answer is expected to be:",
        ]
        return self.select_one_option(titles, random_state=random_state)
    
    def get_input_output_section_title(self, random_state=None):
        if self.random_state is not None:
            np.random.seed(random_state)
        input_title = self.get_input_section_title()
        output_title = self.get_output_section_title()
        return input_title, output_title
    
    def get_input_output_section_title_pair(self, random_state=None):
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
        return self.select_one_option(titles, random_state=random_state)
    
    def get_task_desc_title(self, random_state=None):
        titles = [
            "# Task Description:",
            "Objective:",
            "Task:",
            "Description:",
            "Instruction:",
            # "The task instruction is described as follows:",
            # "Here is a description of the task:",
            # "The following is a description of the task instruction.",
            # "This is the explanation for the task instruction:",
            # "The task instruction is articulated as follows.",
            # "The task instruction is defined as follows:",
        ]
        return self.select_one_option(titles, random_state=random_state)  
    
    def get_example_section_title(self, random_state=None):
        titles = [
            "# Examples",
            "For example:",
            "Let's see some examples as follows.",
            "Here are some examples.",
            "Consider the following examples:",
            "These are a few samples:",
            "Here's a collection of examples:",
            "Here's a list of examples.",
            "These are some examples.",
        ]
        return self.select_one_option(titles, random_state=random_state)
   
    def generate_fewshot_example_prompt(self, query, answer, random_state=None):
        input_title, output_title = self.get_input_output_section_title_pair(random_state=random_state)
        prompt = (
            f"{input_title}\n"
            f"{query.strip()}\n\n"
            f"{output_title}\n"
            f"{answer}"
        )
        return prompt
    
    def get_zeroshot_position(self, random_state=None):
        options = [
            "decription_first",
            'input_first'
        ]
        return self.select_one_option(options, random_state=random_state) 
    
    def format_zeroshot_prompt(self, test_query, random_state=None):
        if random_state is not None:
            np.random.seed(random_state)
        
        position = self.get_zeroshot_position(random_state=None)
        task_desc_title = self.get_task_desc_title(random_state=None)
        task_desc_text = self.task_descriptor.get_task_description(random_state=None)
        # output_title = self.get_output_section_title(random_state=None)
        # input_title = self.get_input_section_title(random_state=None)
        input_title, output_title = self.get_input_output_section_title_pair(random_state=random_state)
        
        # if position == "decription_first":
        prompt = (
            f"{task_desc_title} "
            f"{task_desc_text}\n\n"
            f"{input_title}\n"
            f"{test_query.strip()}\n\n"
            f"{self._get_suffix()}"
            f"{output_title}\n"
        )
        # else:
        #     prompt = (
        #         f"{task_desc_title}\n\n"
        #         f"{input_title}\n"
        #         f"{test_query.strip()}\n\n"
        #         f"{task_desc_text}\n\n"
        #         f"{output_title}\n"
        #     )
        return prompt
    
    def get_example_sep(self, random_state=None):
        example_seps = [
            "\n----------\n",
            "\n----\n",
            "\n\n",
            "\n====\n",
            "\n==========\n",
            "\n:::\n",
        ]
        return self.select_one_option(example_seps, random_state=random_state) 
    
    def format_fewshot_prompt(self, train_prompt_list, test_query, random_state=None):
        if random_state is not None:
            np.random.seed(random_state)
            
        example_sep = self.get_example_sep(random_state=None)
        section_sep = self.get_example_sep(random_state=None)
        task_desc_title = self.get_task_desc_title(random_state=None)
        task_desc_title_2 = self.get_task_desc_title(random_state=None)
        task_desc_text = self.task_descriptor.get_task_description(random_state=None)
        task_desc_text_2 = self.task_descriptor.get_task_description(random_state=None)
        # input_title = self.get_input_section_title(random_state=None)
        # output_title = self.get_output_section_title(random_state=None)
        task_desc_text_2 = task_desc_text
        task_desc_title_2 = task_desc_title
        input_title, output_title = self.get_input_output_section_title_pair(self.random_state)
        
        example_title = self.get_example_section_title(random_state=None)
        position = self.get_zeroshot_position(random_state=None)
        
        few_shot_text = []
        for i, ex in enumerate(train_prompt_list):
            ex_text = (
                # f"Example {i+1}:\n"
                f"{ex}"
            )
            few_shot_text.append(ex_text)
        # train_prompt = f"{example_sep}".join(few_shot_text)
        train_prompt = f"\n\n".join(few_shot_text)
        
        # if position == "decription_first":
        prompt = (
            f"{task_desc_title} "
            f"{task_desc_text}\n\n"
            # f"{section_sep}"
            # f"{example_title}\n"
            f"{train_prompt}\n\n"
            # f"{section_sep}"
            # f"{task_desc_title_2}\n"
            # f"{task_desc_text_2}\n\n"
            f"{input_title}\n"
            f"{test_query.strip()}\n\n"
            f"{self._get_suffix()}"
            f"{output_title}\n"
        )
        # else:
        #     prompt = (
        #         f"{task_desc_title}\n"
        #         f"{task_desc_text}\n"
        #         f"{section_sep}"
        #         f"{example_title}\n"
        #         f"{train_prompt}\n"
        #         f"{section_sep}"
        #         f"# Task:\n"
        #         f"{input_title}\n"
        #         f"{test_query.strip()}\n\n"
        #         f"{task_desc_text_2}\n"
        #         f"{output_title}\n"
        #     )
        return prompt
    
    def select_one_option(self, options, random_state=None):
        if not self.use_random_template:
            return options[0]
        else:
            if random_state is not None:
                np.random.seed(random_state)
            idx = np.random.choice(len(options))
            return options[idx]
    