#!/usr/bin/env bash
set -euo pipefail

APP_NAME="vllm"
SERVICE_NAME="vllm-vllm.service"
ENV_FILE="${HOME}/.johnny/${APP_NAME}/vllm.env"

if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Could not find ${ENV_FILE}."
    echo "Install vLLM first with: johnny install vllm"
    exit 1
fi

current_model="$(grep -E '^MY_MODEL=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
current_context="$(grep -E '^MY_CONTEXT_SIZE=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
current_gpu_utilization="$(grep -E '^MY_GPU_UTILIZATION=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
current_kv_cache_dtype="$(grep -E '^MY_KV_CACHE_DTYPE=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"

echo "Current vLLM model: ${current_model:-unset}"
read -r -p "Hugging Face model [${current_model:-neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8}]: " model
model="${model:-${current_model:-neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8}}"

read -r -p "Context size [${current_context:-32768}]: " context_size
context_size="${context_size:-${current_context:-32768}}"

read -r -p "GPU utilization [${current_gpu_utilization:-1.0}]: " gpu_utilization
gpu_utilization="${gpu_utilization:-${current_gpu_utilization:-1.0}}"

read -r -p "KV cache dtype [${current_kv_cache_dtype:-fp8}]: " kv_cache_dtype
kv_cache_dtype="${kv_cache_dtype:-${current_kv_cache_dtype:-fp8}}"

tmp_file="$(mktemp)"
trap 'rm -f "${tmp_file}"' EXIT

update_or_append() {
    local key="$1"
    local value="$2"

    if grep -q -E "^${key}=" "${tmp_file}"; then
        sed -i "s|^${key}=.*|${key}=${value}|" "${tmp_file}"
    else
        printf "%s=%s\n" "${key}" "${value}" >> "${tmp_file}"
    fi
}

cp "${ENV_FILE}" "${tmp_file}"
update_or_append "MY_MODEL" "${model}"
update_or_append "MY_CONTEXT_SIZE" "${context_size}"
update_or_append "MY_GPU_UTILIZATION" "${gpu_utilization}"
update_or_append "MY_KV_CACHE_DTYPE" "${kv_cache_dtype}"

cp "${tmp_file}" "${ENV_FILE}"

echo "Updated ${ENV_FILE}"
echo "Restarting ${SERVICE_NAME}..."

systemctl --user reset-failed "${SERVICE_NAME}" >/dev/null 2>&1 || true
systemctl --user stop "${SERVICE_NAME}" >/dev/null 2>&1 || true

if systemctl --user restart "${SERVICE_NAME}"; then
    echo "vLLM restarted with model: ${model}"
    systemctl --user status "${SERVICE_NAME}" --no-pager -l --lines=0
else
    echo "Failed to restart ${SERVICE_NAME}."
    echo "Recent logs:"
    journalctl --user -u "${SERVICE_NAME}" -n 80 --no-pager
    exit 1
fi
