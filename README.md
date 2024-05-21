# Table-GPT: Table-tuned GPT for Diverse Table Tasks

This repository contains the source code to generate table-tuning datasets for the SIGMOD'24 paper [Table-GPT: Table-tuned GPT for Diverse Table Tasks](https://arxiv.org/abs/2310.09263). 

## Data Availability
Our training and test table-finetuning data for Table-GPT can be downloaded directly from https://huggingface.co/datasets/LipengCS/Table-GPT.

## Task descriptions
We collect (or synthesize) 18 diverse table-related tasks, which are summarized in the table below. There are 14 training tasks (T5 - T18) and 9 test tasks (T1 - T9). Some of these tasks (T-1 to T-4) are used as unseen hold-out tasks, to evaluate Table-GPT ability to generalize to completely new and unseen tasks. Some of these tasks (T-10 to T-18) are used for training only. 
 
 | **Task Name** | **Task Description** | **Task Category** | **Train/Test** |
|---|---|---|---|
| T-1: Missing-value identification (MV) | Identify the row and column position of the only missing cell in a given table | Table understanding | Test only |
| T-2: Column-finding (CF) | Identify the column-name of a specific value that appears only once in a given table | Table Understanding | Test only |
| T-3: Table-QA (TQA) | Answer a natural-language question based on the content of a table | Table QA | Test only |
| T-4: Column type annotation (CTA) | Find the semantic type of a column from a given list of choices | Table understanding | Test only |
| T-5: Row-to-row transform (R2R) | Transform table data based on input/output examples | Data transformation | Train/Test |
| T-6: Entity matching (EM) | Match rows from two tables that refer to the same real-world entity | Table matching | Train/Test |
| T-7: Schema matching (SM) | Match columns from two tables that refer to the same meaning | Table matching | Train/Test |
| T-8: Data imputation (DI) | Predict the missing values in a cell based on the table context | Data cleaning | Train/Test |
| T-9: Error detection (ED) | Detect data values in a table that is a likely error from misspelling | Data cleaning | Train/Test |
| T-10: List extraction (LE) | Extract a structured table from a list that lacks explicit column delimiters | Data transformation | Train only |
| T-11: Header value matching (HVM) | Match column-headers with its data values drawn from the same table | Table matching | Train only |
| T-12: Natural-language to SQL (NS) | Translate a natural-language question on a table into a SQL query | NL-to-SQL | Train only |
| T-13: Table summarization (TS) | Produce a natural-language summary for the content in a table | Data augmentation | Train only |
| T-14: Column augmentation (CA) | Augment a table with additional columns compatible with a given table | Data augmentation | Train only |
| T-15: Row augmentation (RA) | Augment a table with additional rows compatible with a given table | Data augmentation | Train only |
| T-16: Row/column swapping (RCSW) | Manipulate a given table by swapping the position of two rows or columns | Table manipulation | Train only |
| T-17: Row/column filtering (RCF) | Manipulate a given table by filtering on given rows or columns | Table manipulation | Train only |
| T-18: Row/column sorting (RCS) | Manipulate a given table by performing sorting on given rows or columns | Table manipulation | Train only |

## Data Generation
To generate training or test table-finetuning data using the source code, we provide `generate_tablegpt_data.py` that can easily load source data and transform it into training and testing data for finetuning a large language model. Our genererated data are released and can be downloaded from [here](https://huggingface.co/datasets/LipengCS/Table-GPT).

**Step 1.** Download the source data (source.zip) from [here](https://huggingface.co/datasets/LipengCS/Table-GPT/blob/main/source.zip) and unzip it.

**Step 2.** Run the following code to generate training data for a specific table task or run `bash generate_all_train.sh` to generate all training data.

```
python generate_tablegpt_data.py --mode train --task <task_name> --source_dir <source_data_dir> --prob_train_fewshot <prob> --save_dir <save_data_dir> --seed <integer>
```

- `--task` specifies the training task, which can be chosen from "EntityMatching", "SchemaMatching", "DataImputation", "ErrorDetection", "ListExtraction", "HeaderValueMatching", "NL2SQL", "TableSummary", "ColumnAugmentation", "RowAugmentation", "RowColumnSwapping", "RowColumnFiltering", "RowColumnSorting", "Row2RowTransformation", corresponsing to T5 - T18.  
- `--source_dir` specifies the path of the source data downloaded from step 1.
- `--prob_train_fewshot` specifies the the probility of fewshot prompting examples in the generated training data. If an example is selected for fewshot prompting, the number of the fewshot samples will be randomly chosen from 1 to 10.
- `--save_dir` specifies where the generated data are saved.
- `--seed` specifies seed to control randomness.

**Step 3.** Run the following code to generate test data for a specific table task or run `bash generate_all_test.sh` to generate all test data.
```
python generate_tablegpt_data.py --mode test --task <task_name> --source_dir <source_data_dir> --num_test_fewshot_samples <integer> --save_dir <save_data_dir> --seed <integer>
```

- `--task` specifies the test task, which can be chosen from  "ColumnFinding", "MissingValueIdentification", "TableQuestion",
"ColumnTypeAnnotation","EntityMatching", "SchemaMatching", "DataImputation", "ErrorDetection", "Row2RowTransformation", corresponsing to T1 - T9.
- `--source_dir` specifies the path of the source data downloaded from step 1.
- `--num_test_fewshot_samples` specifies the the number of fewshot prompting examples in the generated test data. Set it to zero to generate zero-shot test data.
- `--save_dir` specifies where the generated data are saved.
- `--seed` specifies seed to control randomness.

## Evaluation and Reproduction
We provide a `Evaluator` class that can compute the performance score for each task. We can use it to evaluate the performance of each model by running the following code.

We provide `evaluate_tablegpt_result.py` to evaluate the model performance on a specific table task. We als provide the result generated from our Table-GPT model. Download our results from [here](https://huggingface.co/datasets/LipengCS/Table-GPT/tree/main/results). See `reproduce.ipynb` for steps to reproduce the main results in our paper.

## Documentation
We `DataGenerator` class to generate training or test data for table tasks.

```python
class DataGenerator:
    def __init__(
        self,
        table_task: Union[str, BaseTableTask],
        mode: str = "train",
        num_test_fewshot_samples: int = 5,
        prob_train_fewshot: float = 0.5,
        max_num_train_fewshot_samples: int = 10,
        min_num_train_fewshot_samples: int = 1,
        max_size: Optional[int] = None,
        max_token_length: int = 4096,
        drop_long_prompt: bool = False,
        random_state: int = 1,
        verbose: bool = False,
        use_random_template: bool = False,
        use_cot: bool = False,
        n_jobs: int = 1,
        augment: bool = False,
    ):
```
**Parameters**
- **table_task** (str or a BaseTableTask object): Specifies the type of table task. Use the name for built-in table tasks or define a `BaseTableTask` object for any customized table task. 

- **mode** (str): Specifies whether it is to generate training data or test data. Default is "train". Possible values include "train", "test".

- **num_test_fewshot_samples** (int): Number of few-shot samples to use during testing. Default is 5.

- **prob_train_fewshot** (float): Probability of including a few-shot sample during training. Default is 0.5.

- **max_num_train_fewshot_samples** (int): Maximum number of few-shot samples to use during training. Default is 10.

- **min_num_train_fewshot_samples** (int): Minimum number of few-shot samples to use during training. Default is 1.

- **max_size** (Optional[int]): Maximum number of generated examples. Default is None, meaning no limit.

- **max_token_length** (int): Maximum token length for the generated data. This only works if truncate=True. Default is 4096.

- **drop_long_prompt** (bool): If True and if the generated prompt is longer than max_token_length, it will be dropped. If False, the long prompt will be kept and a warning will be given. Default is True.

- **random_state** (int): Seed for data generation. Default is 1.

- **verbose** (bool): If True, enables verbose output for debugging and logging. Default is False.

- **use_random_template** (bool): If True, uses random templates for data generation. Default is False.

- **use_cot** (bool): If True, uses chain-of-thought reasoning in data generation if supported. Currently, only entity matching and error detection support COT. Default is False. 

- **n_jobs** (int): Number of jobs to run in parallel for data generation. Default is 1.

- **augment** (bool): If True, use data augmentation (e.g., column permutation) if supported. Currently, only "EntityMatching", "SchemaMatching", "DataImputation", "ErrorDetection" and "HeaderValueMatching" support data augmentation.

**Methods**
```python
    def generate_data(
        self, 
        test_data_dir: str, 
        train_data_dir: Optional[str] = None
    ) -> pd.DataFrame:
```
**Parameters**
- **test_data_dir** (str): the folder containing all test data

- **train_data_dir** (str): the folder containing all training data (used for generating few-shot examples)

**Return**
- **result** (pd.DataFrame): a dataframe containing prompts and completions for all data examples.