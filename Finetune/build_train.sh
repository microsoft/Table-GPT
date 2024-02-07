screen -dmS train python main_build_data.py --task em di ed hvm le ts ns sm cg rg r2rf rcf rcs rcsw  --n_jobs 48 --cot --variant_prompt
screen -dmS val python main_build_data.py --task mcrs mcrn mccs mccn --n_jobs 48  --tag ValData --max_size 500


screen -dmS train python main_build_data.py --task ed --n_jobs 48 --cot --variant_prompt


screen -dmS train python main_build_data.py --task em di ed hvm le ts ns sm cg rg r2rf rcf rcs rcsw  --n_jobs 48 --cot --tag NoPromptVariant

screen -dmS train python main_build_data.py --task em di ed hvm le ts ns sm cg rg r2rf rcf rcs rcsw  --n_jobs 48 --variant_prompt --tag NoCOT

# 2048 token
screen -dmS train python main_build_data.py --task em di ed hvm le ts ns sm cg rg r2rf rcf rcs rcsw  --n_jobs 48 --cot --variant_prompt --max_token_length 2048

# json
screen -dmS train python main_build_data.py --task em di ed hvm le ts ns sm cg rg r2rf rcf rcs rcsw  --n_jobs 48 --cot --variant_prompt --serializer json --tag JSON
screen -dmS train python main_build_data.py --task em di ed hvm le ts ns sm cg rg r2rf rcf rcs rcsw  --n_jobs 48 --cot --variant_prompt --serializer csv --tag CSV
# csv

# single task finetune
screen -dmS st python main_build_data.py --task cta --n_jobs 48 --cot --variant_prompt --tag ST-CTA  --max_size 1000000
screen -dmS st python main_build_data.py --task tq --n_jobs 48 --cot --variant_prompt --tag ST-TQ --max_size 1000000

screen -dmS val python main_build_data.py --task mcrs mcrn mccs mccn --n_jobs 48  --tag ValData --max_size 500 --max_token_length 2048

