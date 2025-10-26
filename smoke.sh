# #!/usr/bin/env bash
# # scripts/smoke.sh
# set -euo pipefail

# API_BASE="${API_BASE:-http://127.0.0.1:8000}"
# FILE_PATH="${1:-msp-agreement.pdf}"   # pass a path or it defaults to msp-agreement.pdf
# QA_QUERY="${QA_QUERY:-What is the payment amount and due date?}"
# K="${K:-3}"
# RETRIES="${RETRIES:-10}"
# SLEEP_SECONDS="${SLEEP_SECONDS:-1}"

# if ! command -v jq >/dev/null 2>&1; then
#   echo "[error] 'jq' is required. Install it (brew install jq) and retry." >&2
#   exit 1
# fi

# echo "==> Checking server health at ${API_BASE}/api/health"
# curl -fsS "${API_BASE}/api/health" | jq .

# echo "==> Uploading file: ${FILE_PATH}"
# if [ ! -f "$FILE_PATH" ]; then
#   echo "[error] File not found: $FILE_PATH" >&2
#   exit 1
# fi

# RESP="$(curl -fsS -F "file=@${FILE_PATH}" "${API_BASE}/api/upload")"
# echo "$RESP" | jq .
# DOC_ID="$(echo "$RESP" | jq -r .doc_id)"
# if [ -z "${DOC_ID}" ] || [ "${DOC_ID}" = "null" ]; then
#   echo "[error] Upload did not return a doc_id" >&2
#   exit 1
# fi
# echo "==> doc_id: ${DOC_ID}"

# echo "==> Running extraction"
# EXTRACT_PAYLOAD="$(jq -n --arg doc_id "$DOC_ID" '{doc_id:$doc_id, use_llm:true, fallback_rules:true}')"
# curl -fsS -H "Content-Type: application/json" \
#   -d "${EXTRACT_PAYLOAD}" \
#   "${API_BASE}/api/extract" | jq .

# echo "==> QA (debug) — query: ${QA_QUERY}"
# QA_PAYLOAD="$(jq -n --arg doc_id "$DOC_ID" --arg q "$QA_QUERY" --argjson k "$K" '{doc_id:$doc_id, query:$q, k:$k}')"

# # Try immediately, then retry on 202 (index building)
# attempt=1
# while : ; do
#   HTTP_CODE=0
#   # capture both body and status
#   BODY="$(curl -sS -w '\n%{http_code}\n' -H "Content-Type: application/json" \
#             -d "${QA_PAYLOAD}" \
#             "${API_BASE}/api/qa/debug")"
#   HTTP_CODE="$(echo "$BODY" | tail -n1)"
#   JSON="$(echo "$BODY" | sed '$d')"

#   if [ "$HTTP_CODE" = "200" ]; then
#     echo "$JSON" | jq .
#     echo "==> Done."
#     exit 0
#   elif [ "$HTTP_CODE" = "202" ]; then
#     echo "[info] Index is preparing (202). Retry ${attempt}/${RETRIES} after ${SLEEP_SECONDS}s…"
#     attempt=$((attempt+1))
#     if [ $attempt -gt $RETRIES ]; then
#       echo "[error] QA index did not become ready after ${RETRIES} retries." >&2
#       echo "$JSON" | jq .
#       exit 2
#     fi
#     sleep "${SLEEP_SECONDS}"
#   else
#     echo "[error] QA call failed with HTTP ${HTTP_CODE}" >&2
#     echo "$JSON" | jq .
#     exit 3
#   fi
# done
#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://127.0.0.1:8000}"
FILE_PATH="${1:-msp-agreement.pdf}"
QA_QUERY="${QA_QUERY:-What is the payment amount and due date?}"
JQ="${JQ_BIN:-jq}"

if ! command -v "${JQ}" >/dev/null 2>&1; then
  echo "[error] 'jq' is required (brew install jq)" >&2
  exit 1
fi

echo "==> Health"
curl -fsS "${API_BASE}/api/health" | ${JQ} .

echo "==> Upload: ${FILE_PATH}"
RESP="$(curl -fsS -F "file=@${FILE_PATH}" "${API_BASE}/api/upload")"
echo "$RESP" | ${JQ} .
DOC_ID="$(echo "$RESP" | ${JQ} -r .doc_id)"
echo "doc_id: $DOC_ID"

echo "==> Extract (flash-lite)"
curl -fsS -H "Content-Type: application/json" \
  -d "$( ${JQ} -n --arg d "$DOC_ID" '{doc_id:$d, use_llm:true, fallback_rules:true}' )" \
  "${API_BASE}/api/extract" | ${JQ} .

echo "==> QA (full-text only)"
curl -fsS -H "Content-Type: application/json" \
  -d "$( ${JQ} -n --arg d "$DOC_ID" --arg q "$QA_QUERY" '{doc_id:$d, query:$q, strategy:"full"}' )" \
  "${API_BASE}/api/qa" | ${JQ} .

echo "==> Done."
