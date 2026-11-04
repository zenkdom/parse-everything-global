#!/usr/bin/env bash
# Quickstart cURL commands for Parse Everything API
# https://parse-everything.com

API_KEY="pe_live_YOUR_API_KEY"
API_URL="https://parse-everything.com/api/v1/extract"

echo "=== 1. Simple GET Extraction ==="
curl -s "${API_URL}?target_url=https://example.com" \
     -H "Authorization: Bearer ${API_KEY}"

echo -e "\n\n=== 2. POST Extraction with Cloudflare Bypass & CSS Selectors ==="
curl -s -X POST "${API_URL}" \
     -H "Authorization: Bearer ${API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{
       "target_url": "https://nopecha.com/demo/cloudflare",
       "bypass_cloudflare": true,
       "selectors": {
         "heading": "h1"
       }
     }'

echo -e "\n\n=== 3. Clean Text Extraction for LLM / RAG ==="
curl -s -X POST "${API_URL}" \
     -H "Authorization: Bearer ${API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{
       "target_url": "https://example.com",
       "extract_text": true
     }'

echo -e "\n\nDone!"
