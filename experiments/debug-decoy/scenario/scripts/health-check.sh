#!/bin/bash
# service health check — used by the ops dashboard
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -m 3 http://127.0.0.1:8081/api/health)
if [ "$STATUS" = "200" ]; then
  echo "UP"
else
  echo "DOWN (http=$STATUS)"
fi
