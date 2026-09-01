#!/bin/bash
# Model connectivity test for Muses models configured in ~/.grok/config.toml
# Tests each model with a simple prompt, measures latency, and checks response quality.

BASE_URL="${MUSES_BASE_URL:-http://muses-openapi-prod.weizhipin.com/v1}"
PERSONAL_KEY="${MUSES_PERSONAL_KEY:?set MUSES_PERSONAL_KEY in your env (do not commit keys)}"
TEAM_KEY="${MUSES_TEAM_KEY:?set MUSES_TEAM_KEY in your env (do not commit keys)}"
TIMEOUT=60

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Results tracking
declare -a RESULTS
PASS=0
FAIL=0

echo ""
echo "============================================================"
echo "   Muses 模型连通性测试"
echo "   $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

test_model() {
    local label="$1"
    local model_id="$2"
    local api_key="$3"
    local backend="$4"  # chat_completions or messages
    
    local endpoint
    local body
    
    if [ "$backend" == "messages" ]; then
        endpoint="${BASE_URL}/messages"
        body=$(cat <<EOF
{
  "model": "$model_id",
  "max_tokens": 50,
  "messages": [{"role": "user", "content": "Reply with exactly: OK"}]
}
EOF
)
    else
        endpoint="${BASE_URL}/chat/completions"
        body=$(cat <<EOF
{
  "model": "$model_id",
  "max_tokens": 50,
  "messages": [{"role": "user", "content": "Reply with exactly: OK"}]
}
EOF
)
    fi
    
    printf "${BOLD}%-35s${NC} " "$label"
    
    # Measure time
    local start_time=$(perl -MTime::HiRes=time -e 'printf "%.3f", time' 2>/dev/null || echo $(date +%s))
    
    local response
    response=$(curl -s -w "\n%{http_code}\n%{time_total}" \
        --max-time $TIMEOUT \
        -X POST "$endpoint" \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        -d "$body" 2>&1)
    
    local exit_code=$?
    
    # Parse response
    local http_code=$(echo "$response" | tail -2 | head -1)
    local time_total=$(echo "$response" | tail -1)
    local resp_body=$(echo "$response" | head -n -2)
    
    # Extract content from response (different formats for chat_completions vs messages)
    local content=""
    if [ "$backend" == "messages" ]; then
        content=$(echo "$resp_body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0]['text'])" 2>/dev/null)
        if [ -z "$content" ]; then
            content=$(echo "$resp_body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error',{}).get('message','PARSE_ERROR'))" 2>/dev/null)
        fi
    else
        content=$(echo "$resp_body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'])" 2>/dev/null)
        if [ -z "$content" ]; then
            content=$(echo "$resp_body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error',{}).get('message','PARSE_ERROR'))" 2>/dev/null)
        fi
    fi
    
    # Trim content
    content=$(echo "$content" | head -1 | cut -c1-50)
    
    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✓ PASS${NC}  ${CYAN}${time_total}s${NC}  → \"$content\""
        PASS=$((PASS + 1))
        RESULTS+=("${GREEN}PASS${NC}|$label|${time_total}s|$content")
    else
        echo -e "${RED}✗ FAIL${NC}  HTTP $http_code  ${time_total}s  → \"$content\""
        FAIL=$((FAIL + 1))
        RESULTS+=("${RED}FAIL${NC}|$label|${time_total}s|HTTP $http_code: $content")
    fi
}

echo -e "${BOLD}── GPT 系列 ──${NC}"
echo ""
test_model "GPT-5.4 (personal)"            "openai/gpt-5.4"                  "$PERSONAL_KEY" "chat_completions"
test_model "GPT-5.5 (personal)"            "openai/gpt-5.5"                  "$PERSONAL_KEY" "chat_completions"

echo ""
echo -e "${BOLD}── Qwen 系列 ──${NC}"
echo ""
test_model "Qwen3.7 Max (personal)"        "bailian/qwen3.7-max"             "$PERSONAL_KEY" "chat_completions"

echo ""
echo -e "${BOLD}── Claude 系列 ──${NC}"
echo ""
test_model "Claude Opus 4.8 (personal)"    "Claude-Opus-4-8"                 "$PERSONAL_KEY" "messages"
test_model "Claude Fable 5 (personal)"     "Claude-Fable-5"                  "$PERSONAL_KEY" "messages"
test_model "Claude Sonnet 5 (personal)"    "Claude-Sonnet-5"                 "$PERSONAL_KEY" "messages"

echo ""
echo -e "${BOLD}── DeepSeek 系列 ──${NC}"
echo ""
test_model "DeepSeek V4 Pro (personal)"    "DeepSeek/deepseek-v4-pro"        "$PERSONAL_KEY" "chat_completions"
test_model "DeepSeek V4 Flash (personal)"  "DeepSeek/deepseek-v4-flash"      "$PERSONAL_KEY" "chat_completions"
test_model "DeepSeek V4 Pro (team)"        "DeepSeek/deepseek-v4-pro"        "$TEAM_KEY"     "chat_completions"
test_model "DeepSeek V4 Flash (team)"      "DeepSeek/deepseek-v4-flash"      "$TEAM_KEY"     "chat_completions"

echo ""
echo "============================================================"
printf "  结果: ${GREEN}%d 通过${NC} / ${RED}%d 失败${NC} / %d 总计\n" $PASS $FAIL $((PASS + FAIL))
echo "============================================================"
echo ""

# Slowest models
echo -e "${BOLD}── 响应时间排名 (慢 → 快) ──${NC}"
for entry in "${RESULTS[@]}"; do
    echo "$entry"
done | sort -t'|' -k3 -rn | while IFS='|' read status name time detail; do
    printf "  %-35s %s\n" "$name" "$time"
done

echo ""
