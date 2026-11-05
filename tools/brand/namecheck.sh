#!/bin/bash
# Check whether a name is free as a YouTube handle, a TikTok handle and a .com domain.
# Usage: bash tools/brand/namecheck.sh name1 name2 ...
# FREE = no account/registration found (a handle can still be blocked for other reasons).
# Instagram needs a login, so check it by hand.
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
T=$(mktemp)
printf "%-14s %-8s %-8s %-8s\n" name youtube tiktok dotcom
for n in "$@"; do
  yt=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 -A "$UA" "https://www.youtube.com/@$n")
  curl -s -o "$T" --max-time 20 -A "$UA" "https://www.tiktok.com/@$n"; sc=$(grep -o '"statusCode":[0-9]*' "$T" | head -1 | cut -d: -f2)
  dc=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "https://rdap.verisign.com/com/v1/domain/$n.com")
  y=$([ "$yt" = 404 ] && echo FREE || ([ "$yt" = 200 ] && echo taken || echo "?$yt"))
  t=$([ "$sc" = 10221 ] && echo FREE || ([ "$sc" = 0 ] && echo taken || echo "?$sc"))
  d=$([ "$dc" = 404 ] && echo FREE || ([ "$dc" = 200 ] && echo taken || echo "?$dc"))
  printf "%-14s %-8s %-8s %-8s\n" "$n" "$y" "$t" "$d"
  sleep 0.5
done
rm -f "$T"
