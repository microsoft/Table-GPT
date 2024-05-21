from tablegpt import Evaluator
import pandas as pd
import argparse


def evalute_result(result):
    # Compute the performance score for each dataset
    zeroshot = []
    fewshot = []

    for (task, setting, dataset), res in result.groupby(
        ["task", "prompt_setting", "dataset"]
    ):
        evaluator = Evaluator(task=task)
        score = evaluator.compute_score(res)
        eval_result = {
            "task": task,
            "dataset": dataset,
            f"{setting}": round(score, 3),
        }
        if setting == "zero-shot":
            zeroshot.append(eval_result)
        else:
            fewshot.append(eval_result)

    zeroshot = pd.DataFrame(zeroshot).set_index(["task", "dataset"])
    fewshot = pd.DataFrame(fewshot).set_index(["task", "dataset"])
    scores = pd.concat([zeroshot, fewshot], axis=1)
    return scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result_path", default="None")
    args = parser.parse_args()

    # load result
    result = pd.read_json(args.result_path, lines=True)
    scores = evalute_result(result)
    print(scores)
