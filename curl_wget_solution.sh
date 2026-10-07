#!/usr/bin/env bash
URL="http://hw1.alexbers.com"
TOKEN="67777a5609f9778299777f23da96993f"
PY="${PY:-python3}"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT # временная папка удалится после завершения

fetch() {
  curl -s -b "user=$TOKEN" "$@"
}

html=$(fetch "$URL/")

while true; do
  if ! printf '%s' "$html" | "$PY" parse_cli.py "$URL" "$TMP" > "$TMP/args"; then
    break # если ссылка не найдена, финальная страница выведется в stderr
  fi
  mapfile -d '' -t args < "$TMP/args" # записываем файл в массив
#  echo "${args[2]}"
  html=$(fetch "${args[@]}")
done