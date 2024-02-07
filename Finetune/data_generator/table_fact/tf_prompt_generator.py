from ..base.base_prompt_generator import BasePromptGenerator
import json

class TFPromptGenerator(BasePromptGenerator):
    pass
    # def _shorten_input_data(self, test_data, train_samples):
    #     if train_samples is not None and len(train_samples) > self.min_fewshot_samples:
    #         train_samples = train_samples[1:]
    #         return test_data, train_samples, False
        
    #     # try drop very long column for test
    #     df_test, question_test = test_data
        
    #     if df_test.shape[1] < 2:
    #         return test_data, train_samples, True
        
    #     # only drop na columns and very long column 
    #     df_test_short = self.drop_long_column(df_test)

    #     if train_samples is not None:
    #         train_samples_short = []
    #         for (df_sample, q_sample), y in train_samples:
    #             df_sample_short = self.drop_long_column(df_sample)
    #             train_samples_short.append(((df_sample_short, q_sample), y))
    #     else:
    #         train_samples_short = None
        
    #     return (df_test_short, question_test), train_samples_short, False

    # def drop_long_column(self, df):
    #     max_c = None
    #     max_length = float("-inf")
        
    #     for c in df.columns:
    #         length = sum([len(str(x)) for x in df[c].values])
    #         if length > max_length:
    #             max_c = c
    #             max_length = length
        
    #     new_columns = [c for c in df.columns if c != max_c]
    #     return df[new_columns]