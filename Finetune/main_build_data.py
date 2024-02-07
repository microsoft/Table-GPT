import pandas as pd
import os
import argparse
import numpy as np
from datetime import date
import utils
from data_generator.entity_matching.em_data_generator import EMDataGenerator
from data_generator.data_imputation.di_data_generator import DIDataGenerator
from data_generator.error_detection.ed_data_generator import EDDataGenerator
from data_generator.header_value_matching.hvm_data_generator import HVMDataGenerator
from data_generator.list_extraction.le_data_generator import LEDataGenerator
from data_generator.schema_matching.sm_data_generator import SMDataGenerator
from data_generator.table_summary.ts_data_generator import TSDataGenerator
from data_generator.nl_to_sql.ns_data_generator import NSDataGenerator
from data_generator.row2row_fewshot.r2rf_data_generator import R2RFDataGenerator
from data_generator.row2row_zeroshot.r2rz_data_generator import R2RZDataGenerator
from data_generator.column_type_annotation.cta_data_generator import CTADataGenerator
from data_generator.missing_cell_row_sep.mcrs_data_generator import MCRSDataGenerator
from data_generator.missing_cell_row_nosep.mcrn_data_generator import MCRNDataGenerator
from data_generator.missing_cell_col_sep.mccs_data_generator import MCCSDataGenerator
from data_generator.missing_cell_col_nosep.mccn_data_generator import MCCNDataGenerator
from data_generator.table_transformation_zeroshot.ttz_data_generator import TTZDataGenerator
from data_generator.table_transformation_fewshot.ttf_data_generator import TTFDataGenerator
from data_generator.col_generation.cg_data_generator import CGDataGenerator
from data_generator.row_generation.rg_data_generator import RGDataGenerator
from data_generator.semantic_dedup.sd_data_generator import SDDataGenerator
from data_generator.row_column_sorting.rcs_data_generator import RCSDataGenerator
from data_generator.row_column_swapping.rcsw_data_generator import RCSWDataGenerator
from data_generator.row_column_filtering.rcf_data_generator import RCFDataGenerator
from data_generator.table_question.tq_data_generator import TQDataGenerator
from data_generator.relation_extraction.re_data_generator import REDataGenerator
from data_generator.column_finding.cf_data_generator import CFDataGenerator
from data_generator.table_fact.tf_data_generator import TFDataGenerator
from data_generator.table_fact_fewshot.tff_data_generator import TFFDataGenerator
import json

parser = argparse.ArgumentParser()
parser.add_argument("--root_dir", default="data")
parser.add_argument("--data_version", default="14.19")
parser.add_argument("--cot_data_dir", default="../COTQuery/data")
parser.add_argument("--cot_version", default="1.1.0")
parser.add_argument("--task", nargs="+", default=None)
parser.add_argument("--mode", default="train", choices=["train", "test", "val"])
parser.add_argument("--serializer", default="markdownshortline")
parser.add_argument("--tag", default=None)
parser.add_argument("--num_trials", type=int, default=1)
parser.add_argument("--max_token_length", type=int, default=4096)
parser.add_argument("--max_size_per_dataset", type=int, default=500)
parser.add_argument("--num_col_perturb", type=int, default=1)
parser.add_argument("--sample_method", type=str, help="Example generation method", default="random", choices=["random", "stanford"])
parser.add_argument("--num_few_shot_samples", type=int, help="Number examples in few-shot prompt", default=10)
parser.add_argument("--max_train_num_few_shot_samples", type=int, default=10)
parser.add_argument("--min_train_num_few_shot_samples", type=int, default=4)
parser.add_argument("--seed", type=int, default=1)
parser.add_argument("--n_jobs", type=int, default=-1)
parser.add_argument("--variant_prompt", action="store_true", default=False)
parser.add_argument("--cot", action="store_true", default=False)
parser.add_argument("--test_cot", action="store_true", default=False)
parser.add_argument("--system", action="store_true", default=False)
parser.add_argument("--cot_position", default="before_answer", choices=["before_answer", "after_answer"])
parser.add_argument("--debug", action="store_true", default=False)
parser.add_argument("--result_dir", default=None)
parser.add_argument("--verbose", action="store_true", default=False)
parser.add_argument("--max_size", type=int, default=5000)
parser.add_argument("--max_test_size", type=int, default=None)
args = parser.parse_args()

generator_version = "30"
data_version = f"{args.data_version}.{generator_version}"

if args.n_jobs < 0:
    args.n_jobs = os.cpu_count()
    
today = date.today().strftime("%m%d")

if args.result_dir is None:
    args.result_dir = f"TrainTestData_v{data_version}"
    
if args.mode == "train":
    save_folder = f"TrainData-data_v{data_version}"
elif args.mode == "val":
    save_folder = f"ValData-data_v{data_version}"
    args.num_col_perturb = 0
else:
    save_folder = f"TestData-data_v{data_version}"
    args.num_col_perturb = 0
    
if args.cot:
    save_folder += f"-COT_v{args.cot_version}"

if args.test_cot:
    save_folder += f"-COTTest"

if args.system:
    save_folder += f"-SystemMessage"
    
if args.variant_prompt:
    save_folder += f"-VariantPrompt"
    
if args.num_col_perturb > 0:
    save_folder += f"-ColPerturb_{args.num_col_perturb}"
    
save_folder += f"-tokens_{args.max_token_length}"

if args.tag is not None:
    save_folder += f"-{args.tag}"
    
for task in args.task:
    save_dir = utils.makedir([args.result_dir, save_folder])
    debug_dir = utils.makedir([save_dir, "debug", task]) if args.debug else None
    cot_data_dir = os.path.join(args.cot_data_dir, f"cot_data_v{args.cot_version}", "cot")

    default_use_cot = False
    if args.mode == "train":
        max_num_datasets = args.max_size
    else:
        max_num_datasets = args.max_test_size

    params = {
        "serializer": args.serializer,
        "num_few_shot_trials": args.num_trials,
        "max_token_length": args.max_token_length,
        "num_col_perturb": args.num_col_perturb,
        "prob_train_few_shot": 0.5,
        "max_train_size": args.max_size_per_dataset,
        "random_state": args.seed,
        "debug_dir": debug_dir,
        "verbose": args.verbose,
        "n_jobs": args.n_jobs,
        "use_random_description": args.variant_prompt,
        "use_random_template": args.variant_prompt,
        "use_cot": default_use_cot,
        "cot_data_dir": cot_data_dir,
        "cot_position": args.cot_position,
        "max_num_datasets": max_num_datasets,
        "use_system_message": args.system
    }

    if task == "em":
        params["max_train_num_few_shot_samples"] = 10
        params["min_train_num_few_shot_samples"] = 4
        params["num_few_shot_samples"] = 10
        params["task"] = "EntityMatching"
        params["use_cot"] = args.cot or default_use_cot
        data_generator = EMDataGenerator(**params)
            
    elif task == "di":
        params["task"] = "DataImputation"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 10
        data_generator = DIDataGenerator(**params)
        
    elif task == "ed":
        params["task"] = "ErrorDetection"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 10
        params["use_cot"] = args.cot or default_use_cot
        data_generator = EDDataGenerator(**params)
        
    elif task == "hvm":
        params["task"] =  "HeaderValueMatching"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        data_generator = HVMDataGenerator(**params)
        
    elif task == "le":
        params["task"] =  "ListExtraction"
        params["max_train_num_few_shot_samples"] = 3
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 2
        params["num_col_perturb"] = 0
        data_generator = LEDataGenerator(**params)
        
    elif task == "sm":
        params["task"] =  "SchemaMatching"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        data_generator = SMDataGenerator(**params)
        
    elif task == "ts":
        params["task"] =  "TableSummary"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = TSDataGenerator(**params)
        
    elif task == "ns":
        params["task"] =  "NL2SQL"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = NSDataGenerator(**params)
        
    elif task == "r2rz":
        params["task"] =  "Row2RowZeroshot"
        params["max_train_num_few_shot_samples"] = 0
        params["min_train_num_few_shot_samples"] = 0
        params["num_few_shot_samples"] = 0
        params["num_few_shot_trials"] = 0
        params["num_col_perturb"] = 0
        data_generator = R2RZDataGenerator(**params)

    elif task == "r2rf":
        params["task"] =  "Row2RowFewshot"
        params["max_train_num_few_shot_samples"] = 0
        params["min_train_num_few_shot_samples"] = 0
        params["num_few_shot_samples"] = 0
        params["num_few_shot_trials"] = 0
        params["num_col_perturb"] = 0
        data_generator = R2RFDataGenerator(**params)

    elif task == "cta":
        params["task"] =  "ColumnTypeAnnotation"
        params["max_train_num_few_shot_samples"] = 3
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 6
        params["num_col_perturb"] = 0
        data_generator = CTADataGenerator(**params)
        
    elif task == "mcrs":
        params["task"] = "MissingCellRowSep"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = MCRSDataGenerator(**params)
        
    elif task == "mcrn":
        params["task"] = "MissingCellRowNoSep"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = MCRNDataGenerator(**params)
        
    elif task == "mccs":
        params["task"] = "MissingCellColSep"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = MCCSDataGenerator(**params)

    elif task == "mccn":
        params["task"] = "MissingCellColNoSep"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = MCCNDataGenerator(**params)
        
    elif task == "ttz":
        params["task"] = "TableTransformationZeroshot"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        params["num_few_shot_trials"] = 0
        data_generator = TTZDataGenerator(**params)

    elif task == "ttf":
        params["task"] = "TableTransformationFewshot"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        params["num_few_shot_trials"] = 0
        data_generator = TTFDataGenerator(**params)
        
    elif task == "cg":
        params["task"] = "ColGeneration"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        params["num_few_shot_trials"] = 0
        data_generator = CGDataGenerator(**params)
        
    elif task == "rg":
        params["task"] = "RowGeneration"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        params["num_few_shot_trials"] = 0
        data_generator = RGDataGenerator(**params)
        
    elif task == "sd":
        params["task"] = "SemanticDedup"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 10
        params["num_col_perturb"] = 0
        data_generator = SDDataGenerator(**params)
        
    elif task == "rcs":
        params["task"] = "RowColumnSorting"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = RCSDataGenerator(**params)

    elif task == "rcsw":
        params["task"] = "RowColumnSwapping"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = RCSWDataGenerator(**params)
        
    elif task == "rcf":
        params["task"] = "RowColumnFiltering"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = RCFDataGenerator(**params)

    elif task == "tq":
        params["task"] = "TableQuestion"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = TQDataGenerator(**params)

    elif task == "re":
        params["task"] = "RelationExtraction"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_few_shot_trials"] = 0
        params["num_col_perturb"] = 0
        data_generator = REDataGenerator(**params)
        
    elif task == "cf":
        params["task"] = "ColumnFinding"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        data_generator = CFDataGenerator(**params)
        
    elif task == "tf":
        params["task"] = "TableFact"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 3
        params["num_col_perturb"] = 0
        params["use_cot"] = args.cot or default_use_cot
        data_generator = TFDataGenerator(**params)

    elif task == "tff":
        params["task"] = "TableFact"
        params["max_train_num_few_shot_samples"] = 5
        params["min_train_num_few_shot_samples"] = 1
        params["num_few_shot_samples"] = 0
        params["num_col_perturb"] = 0
        params["use_cot"] = args.cot or default_use_cot
        data_generator = TFFDataGenerator(**params)

    else:
        raise Exception(f"Wrong task {task}")

    root_data_dir = os.path.join(args.root_dir, f"data_v{args.data_version}")
    
    data_mode = "train" if args.mode == "train" else "test"
    data, invalid_data = data_generator.generate_data(root_data_dir, mode=data_mode)

    # save data
    save_name = save_folder + f"-{task.upper()}"
    save_name = save_name.replace(".", "_")
    jsonl_save_dir = utils.makedir([save_dir, "jsonl"], f"{save_name}-Size_{len(data)}.jsonl")
    params_save_dir = utils.makedir([save_dir, "params"], f"{save_name}.json")
    params["data_size"] = len(data)
    params["invalid_data_size"] = len(invalid_data)
    json.dump(params, open(params_save_dir, "w"), indent=4)
    if len(invalid_data) > 0:
        invalid_save_dir = utils.makedir([save_dir, "invalid"], f"{save_name}.csv")
        invalid_data.to_csv(invalid_save_dir, index=False)

    data.to_csv(utils.makedir([save_dir, "csv"], f"{save_name}.csv"), index=False)

    if args.mode == "train":
        # shuffle train data
        data = data.sample(frac=1, random_state=args.seed)
        data[["prompt", "completion", "metadata"]].to_json(jsonl_save_dir, orient='records', lines=True)
    elif args.mode == "val":
        data[["prompt", "completion", "metadata"]].to_json(jsonl_save_dir, orient='records', lines=True)
    else:
        data[["prompt", "metadata"]].to_json(jsonl_save_dir, orient='records', lines=True)