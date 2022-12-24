#!/bin/sh

#this script identifies the app id from google play

url='https://play.google.com/store/search?q='
cart='&c=apps'
path='/tmp/google_play.url'

query=$(cat app_id.txt)

# query=$(printf '%s' "$*" | tr ' ' '+')
# app_disp=$(printf '%s' "$*" | tr '+' ' ')
# echo "\033[0;33m[Locating: $app_disp ID ...]"

app_list=$(wget -q -O $path $url$query | grep -Eo "torrent\/[0-9]{7}\/[a-zA-Z0-9?%-]*/" | grep mp4 | head -n 1)

app=$(cat $path | grep -Eo "[?]id=[a-z]*.[a-z]*.[a-z]*.[a-z]*.[a-z]*" | head -n 1 > app_id.txt)


#