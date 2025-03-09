from transformers import AutoModelForCausalLM, AutoTokenizer; \
AutoTokenizer.from_pretrained('deepseek-ai/deepseek-r1-distill-qwen-7b', \
    local_files_only=False,
    force_download=False);
AutoModelForCausalLM.from_pretrained('deepseek-ai/deepseek-r1-distill-qwen-7b', \
    local_files_only=False,
    force_download=False)