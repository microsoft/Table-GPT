from tablegpt import DataGenerator
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        required=True,
        choices=[
            "ColumnFinding",
            "MissingValueIdentification",
            "TableQuestion",
            "ColumnTypeAnnotation",
            "EntityMatching",
            "SchemaMatching",
            "DataImputation",
            "ErrorDetection",
            "ListExtraction",
            "HeaderValueMatching",
            "NL2SQL",
            "TableSummary",
            "ColumnAugmentation",
            "RowAugmentation",
            "RowColumnSwapping",
            "RowColumnFiltering",
            "RowColumnSorting",
            "Row2RowTransformation",
        ],
    )
    parser.add_argument("--mode", default="train", choices=["train", "test"])
    parser.add_argument("--source_dir", default="source")
    parser.add_argument("--save_dir", default="tablegpt_data")
    parser.add_argument("--num_test_fewshot_samples", default=3, type=int)
    parser.add_argument("--prob_train_fewshot", default=0.5, type=float)
    parser.add_argument("--seed", default=1, type=int)
    parser.add_argument("--augment", default=False, action="store_true")
    parser.add_argument("--n_jobs", default=8, type=int)
    args = parser.parse_args()

    task_data_dir = os.path.join(args.source_dir, args.task)
    train_data_dir = os.path.join(task_data_dir, "train")
    test_data_dir = os.path.join(task_data_dir, "test")

    print(f"Generating {args.mode} data for {args.task}")

    if args.mode == "train":
        data_generator = DataGenerator(
            args.task,
            mode="train",
            use_random_template=True,
            n_jobs=args.n_jobs,
            random_state=args.seed,
            augment=args.augment,
        )
        data = data_generator.generate_data(train_data_dir, train_data_dir)

        save_name = f"{args.mode}_{args.task}"
        if args.augment:
            save_name += "_augment"

    else:
        test_data_generator = DataGenerator(
            args.task,
            mode="test",
            use_random_template=False,
            n_jobs=args.n_jobs,
            random_state=args.seed,
            num_test_fewshot_samples=args.num_test_fewshot_samples,
        )
        data = test_data_generator.generate_data(test_data_dir, train_data_dir)

        save_name = f"{args.mode}_{args.task}"
        if args.num_test_fewshot_samples == 0:
            save_name += "_zeroshot"
        else:
            save_name += "_fewshot"

    if not os.path.exists(os.path.join(args.save_dir, args.mode)):
        os.makedirs(os.path.join(args.save_dir, args.mode))

    data.to_json(
        os.path.join(
            args.save_dir,
            args.mode,
            f"{save_name}.jsonl",
        ),
        lines=True,
        orient="records",
    )
