import openai
from time import sleep
from multiprocessing import Pool
import multiprocessing
import numpy as np

class GPT4(object):
    def __init__(self, api_keys, api_bases, model_name, max_tokens=3, temperature=0, n_jobs=4):
        self.api_keys = api_keys
        self.api_bases = api_bases
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.n_jobs = min(n_jobs, len(self.api_bases))
        self.api = self.invoke_one_case_gpt4

    def run_multi(self, prompts):
        prompt_groups = np.array_split(prompts, self.n_jobs)
        args = [(prompt_groups[i], self.api_keys[0], self.api_bases[i]) for i in range(self.n_jobs)]
        
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
        prompts, api_key, api_base = arg
        results = []
        for prompt in prompts:
            result = self.run_one(prompt, api_key, api_base)
            results.append(result)
        return results
    
    def run_one(self, prompt, api_key, api_base):            
        while True:
            try:
                pred = self.api(prompt, api_key, api_base)
                return "success", pred
            except Exception as e:
                print(f"An error occurred: {e}")
                if "too long" in str(e).lower():
                    return "prompt too long", None
                else:
                    sleep(5)
                  
    def invoke_one_case_gpt4(self, prompt, api_key, api_base):
        openai.api_key = api_key
        openai.api_base = api_base
        model = "gpt-4"
            
        response = openai.ChatCompletion.create(
            messages= [ # Change the prompt parameter to the messages parameter
                {'role': 'user', 'content': prompt}
            ],
            model=model,
            max_tokens=self.max_tokens,
        )
        prediction = response['choices'][0].message.content
        print(prediction)
        sleep(5)
        return prediction