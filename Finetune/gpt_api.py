import openai
from time import sleep
from multiprocessing import Pool
import multiprocessing
import numpy as np

class GPT(object):
    def __init__(self, api_keys, model_name, max_tokens=3, temperature=0, n_jobs=4):
        self.api_keys = api_keys
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.n_jobs = min(n_jobs, len(api_keys))
        
        if self.model_name == "gpt-3.5-turbo":
            self.api = self.invoke_one_case_chat_turbo_35
        elif self.model_name in ["gpt-4-32k", "gpt-4"]:
            self.api = self.invoke_one_case_gpt4
        else:
            self.api = self.invoke_one_case_davinci_3

    def run_multi(self, prompts):
        prompt_groups = np.array_split(prompts, self.n_jobs)
        args = [(prompt_groups[i], self.api_keys[i]) for i in range(self.n_jobs)]
        
        if self.n_jobs == 1:
            results_groups = [self.run_arg(arg) for arg in args]
        else:
            with Pool(self.n_jobs) as pool:
                results_groups = pool.map(self.run_arg, args)

        merge_results = []
        for results in results_groups:
            merge_results.extend(results)
        return merge_results

    def run_arg(self, arg):
        prompts, api_key = arg
        results = []
        for prompt in prompts:
            result = self.run_one(prompt, api_key)
            results.append(result)
        return results
    
    def run_one(self, prompt, api_key=None):
        if api_key is None:
            api_key = np.random.choice(self.api_keys)
            
        while True:
            try:
                pred = self.api(prompt, api_key)
                return "success", pred
            except Exception as e:
                print(f"An error occurred: {e}")
                if "too long" in str(e).lower():
                    return "prompt too long", None
                else:
                    if self.model_name in ["gpt-4-32k", "gpt-4"]:
                        sleep(1)
                    else:
                        sleep(1)
            
    def invoke_one_case_davinci_3(self, prompt, api_key):
        openai.api_key = api_key
        response = openai.Completion.create(
            model=self.model_name,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        prediction = response['choices'][0].text
        return prediction

    def invoke_one_case_chat_turbo_35(self, prompt, api_key):
        openai.api_key = api_key

        response = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
            model = 'gpt-3.5-turbo',
            messages = [ # Change the prompt parameter to the messages parameter
                {'role': 'user', 'content': prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        prediction = response['choices'][0].message.content
        return prediction
    
    def invoke_one_case_gpt4(self, prompt, api_key):
        if api_key[0] == '9':
            self.model_name = "gpt-4"
        else:
            self.model_name = "gpt-4-32k"
            
        openai.api_type = "azure"
        openai.api_key = api_key
        openai.api_base = "https://gcrgpt4aoai4c.openai.azure.com"
        openai.api_version = "2023-05-15"  # subject to change
        response = openai.ChatCompletion.create(
            messages= [ # Change the prompt parameter to the messages parameter
                {'role': 'user', 'content': prompt}
            ],
            deployment_id=self.model_name,
            max_tokens=self.max_tokens,
            #engine="gpt-4"
        )
        prediction = response['choices'][0].message.content
        # sleep(0.5)
        return prediction