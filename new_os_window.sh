#!/bin/sh
printf "New OS window title: "
read -r title
if [ -n "$title" ]; then
    kitten @ launch --type=os-window --os-window-title "$title"
fi
