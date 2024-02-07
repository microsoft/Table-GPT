# screen -dmS test python main_build_data.py --task sd mcrs mcrn mccs mccn cta tq cf re --n_jobs 48 --mode test --num_trials 1 --tag Unseen --test_cot 
# screen -dmS test python main_build_data.py --task di em ed sm r2rz r2rf --n_jobs 48 --mode test --num_trials 1 --tag Seen --test_cot
# screen -dmS test python main_build_data.py --task re cf cta --n_jobs 48 --mode test --num_trials 1 --tag RE_CF_CTA --test_cot

screen -dmS test python main_build_data.py --task mcrs mcrn mccs mccn cta cf tq di em ed sm r2rf --n_jobs 48 --mode test --num_trials 3 --cot 
screen -dmS test python main_build_data.py --task mcrs mcrn mccs mccn cta cf tq di em ed sm r2rf --n_jobs 48 --mode test --num_trials 1 --cot 

screen -dmS test python main_build_data.py --task mcrs mcrn mccs mccn tq --n_jobs 48 --mode test --num_trials 1 --cot --tag MC-TQ

screen -dmS test python main_build_data.py --task tq --n_jobs 48 --mode test --num_trials 1 --cot --tag TQ

screen -dmS test python main_build_data.py --task cta --n_jobs 48 --mode test --num_trials 1 --cot --tag NewCTA

screen -dmS test python main_build_data.py --task cf tq --n_jobs 48 --mode test --num_trials 1 --cot --tag CF-TQ

screen -dmS test python main_build_data.py --task cf --n_jobs 48 --mode test --num_trials 1 --cot --tag NewCF
