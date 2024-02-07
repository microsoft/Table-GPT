from preprocessor.ColumnTypeAnnotation.build_cta_limaye_t2d import build_limaye, build_t2d, build_efthymiou
from preprocessor.DataImputation.build_di_buy_restaurant import build_buy_restaurant
from preprocessor.DataImputation.build_di_buy_restaurant_row_by_row import build_buy_restaurant_row_by_row
from preprocessor.NL2SQL.build_nl2sql_wikisql import buil_wikisql
from preprocessor.Row2Row.build_r2r_tde_wiki import build_tde_wiki
from preprocessor.SchemaMatching.build_sm_deepm import build_deepm
from preprocessor.SchemaMatching.build_sm_fabricated import build_fabricated
from preprocessor.SchemaMatching.build_sm_synthetic import build_synthetic_sm
from preprocessor.TableSummary.build_web import build_ts_web
from preprocessor.ErrorDetection.build_ed_adult_hospital import build_adult_hospital
from preprocessor.ErrorDetection.build_ed_adult_hospital_row_by_row import build_adult_hospital_row_by_row
from preprocessor.ErrorDetection.build_ed_excel_web_real import build_excel_web_real
from preprocessor.EntityMatching.build_em import build_em
from preprocessor.TableTransformation.build_auto_table import build_auto_table
from preprocessor.SemanticDedup.build_excel_web_semantic_dedup import build_excel_web_semantic_dedup
from preprocessor.TableQuestion.build_tq_wiki_new import build_tq_wiki
from preprocessor.ColumnTypeAnnotation.build_sherlock import build_sherlock
from preprocessor.RelationExtraction.build_turl import build_turl
from preprocessor.ColumnTypeAnnotation.build_wikitables import build_wikitables
from preprocessor.TableFact.build_tf import build_tf
from preprocessor.TableFact.build_tf_simple import build_tf_simple
from preprocessor.SQA.build_sqa import build_sqa

from synthesizer.data_imputation_synthesizer import DataImputationSynthesizer
from synthesizer.error_detection_synthesizer import ErrorDetectionSynthesizer
from synthesizer.header_value_matching_synthesizer import HeaderValueMatchingSynthesizer
from synthesizer.list_extraction_synthesizer import ListExtractionSynthesizer
from synthesizer.missing_cell_synthesizer import MissingCellSynthesizer
from synthesizer.row_generation_synthesizer import RowGenerationSynthesizer
from synthesizer.col_generation_synthesizer import ColGenerationSynthesizer
from synthesizer.row_column_sorting_synthesizer import RowColumnSortingSynthesizer
from synthesizer.row_column_filtering_synthesizer import RowColumnFilteringSynthesizer
from synthesizer.row_column_swapping_synthesizer import RowColumnSwappingSynthesizer
from synthesizer.column_finding_synthesizer import ColumnFindingSynthesizer

import argparse
import utils
import os

parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", default="resources/resources_v14")
parser.add_argument("--task", nargs="+", default=None)
parser.add_argument("--mode", default="all", choices=["syn", "real", "all"])
parser.add_argument("--max_size", default=30000, type=int)
parser.add_argument("--seed", default=1, type=int)
parser.add_argument("--n_jobs", default=-1, type=int)
args = parser.parse_args()

version = "19"

root_data_dir = args.data_dir
resource_verison = utils.load_version(root_data_dir)
assert(f"v{resource_verison}" == root_data_dir.split("_")[1])

root_save_dir = f"source/source_v{resource_verison}.{version}"

if args.n_jobs < 0:
    args.n_jobs = os.cpu_count()

alias = {
    "em": "EntityMatching",
    "di": "DataImputation",
    "ed": "ErrorDetection",
    "hvm": "HeaderValueMatching",
    "le": "ListExtraction",
    "sm": "SchemaMatching",
    "ts": "TableSummary",
    "ns": "NL2SQL",
    "r2r": "Row2Row",
    "cta": "ColumnTypeAnnotation",
    "mc": "MissingCell",
    "tt": "TableTransformation",
    "rg": "RowGeneration",
    "cg": "ColGeneration",
    "sd": "SemanticDedup",
    "rcs": "RowColumnSorting",
    "rcf": "RowColumnFiltering",
    "rcsw": "RowColumnSwapping",
    "tq":  "TableQuestion",
    "re": "RelationExtraction",
    "cf": "ColumnFinding",
    "cf2": "ColumnFinding",
    "tf": "TableFact",
    "sqa": "SQA"
}

synthesizer_dict = {
    "di": DataImputationSynthesizer(),
    "ed": ErrorDetectionSynthesizer(),
    "hvm": HeaderValueMatchingSynthesizer(),
    "le": ListExtractionSynthesizer(),
    "mc": MissingCellSynthesizer(),
    "rg": RowGenerationSynthesizer(),
    "cg": ColGenerationSynthesizer(),
    "rcs": RowColumnSortingSynthesizer(),
    "rcf": RowColumnFilteringSynthesizer(),
    "rcsw": RowColumnSwappingSynthesizer(),
    "cf": ColumnFindingSynthesizer(),
}

synthesizer_id = {task: i for i, task in enumerate(synthesizer_dict.keys())}

if args.mode in ["all", "real"]:
    if args.task is None:
        tasks = list(alias.keys())
    else:
        tasks = args.task

    for task in tasks:
        print("- Processing", alias[task])
        data_dir = os.path.join(root_data_dir, alias[task])
        save_dir = os.path.join(root_save_dir, alias[task])
        
        if task == "em":
            build_em(data_dir, save_dir)

        if task == "cta":
            # build_wikitables(data_dir, save_dir, max_train_size=None)
            build_sherlock(data_dir, save_dir)
            build_efthymiou(data_dir, save_dir)
            build_limaye(data_dir, save_dir)
            build_t2d(data_dir, save_dir)
            
        if task == "di":
            build_buy_restaurant(data_dir, "Buy", save_dir)
            build_buy_restaurant(data_dir, "Restaurant", save_dir)
            build_buy_restaurant_row_by_row(data_dir, "Buy", save_dir)
            build_buy_restaurant_row_by_row(data_dir, "Restaurant", save_dir)
            
        if task == "ns":
            buil_wikisql(data_dir, save_dir)
            
        if task == "r2r":
            build_tde_wiki(data_dir, "Wiki", save_dir)
            build_tde_wiki(data_dir, "TDE", save_dir)
            
        if task == "sm":
            # build_fabricated(data_dir, save_dir)
            build_synthetic_sm(data_dir, "Web", save_dir)
            # build_synthetic_sm(data_dir, "Excel", save_dir)
            build_deepm(data_dir, save_dir)

        if task == "ts":
            build_ts_web(data_dir, save_dir)

        if task == "ed":
            build_excel_web_real(data_dir, "ExcelRealV6", save_dir)
            build_excel_web_real(data_dir, "WebRealV6", save_dir)
            # build_adult_hospital(data_dir, "Adult", save_dir)
            # build_adult_hospital(data_dir, "Hospital", save_dir)
            # build_adult_hospital_row_by_row(data_dir, "Adult", save_dir)
            # build_adult_hospital_row_by_row(data_dir, "Hospital", save_dir)
            
        if task == "tt":
            build_auto_table(data_dir, save_dir)
        
        # if task == "sd":
        #     build_excel_web_semantic_dedup(data_dir, "ExcelRealV6", save_dir)
        #     build_excel_web_semantic_dedup(data_dir, "WebRealV6", save_dir)
        
        if task == "tq":
            build_tq_wiki(data_dir, save_dir)
            
        if task == "tf":
            # build_tf(data_dir, save_dir)
            build_tf_simple(data_dir, save_dir)
        
        if task == "sqa":
            build_sqa(data_dir, save_dir)
            
        # if task == "re":
        #     build_turl(data_dir, save_dir)
                
if args.mode in ["all", "syn"]:
    # build synthetic data
    # run all tasks if not specifed
    if args.task is None:
        tasks = list(synthesizer_dict.keys())
    else:
        tasks = [x for x in args.task if x in synthesizer_dict]

    for i, task in enumerate(tasks):
        print("- Processing", task)
        synthesizer = synthesizer_dict[task]
        
        # web train
        train_dataset = f"WebPBISynthetic_{synthesizer_id[task]}"
        train_data_dir = os.path.join(root_data_dir, 'Synthetic', "data")
        train_save_dir = os.path.join(root_save_dir, alias[task], "train_only")
        synthesizer.synthesize(train_data_dir, train_dataset, train_save_dir, max_size=args.max_size, random_state=args.seed+i, n_jobs=args.n_jobs, mode="train")
        
        test_dataset = "ExcelSynthetic"
        test_data_dir = os.path.join(root_data_dir, 'Synthetic', "data")
        test_save_dir = os.path.join(root_save_dir, alias[task], "test_only")
        synthesizer.synthesize(test_data_dir, test_dataset, test_save_dir, max_size=args.max_size, random_state=args.seed+i, n_jobs=args.n_jobs, mode="test")
        
utils.save_version(root_save_dir, f"{resource_verison}.{version}")