#!/usr/bin/bash

RBC=100
while true; do
python anna.py
ECODE=$?
if [ $RBC -eq $ECODE ]; then
echo rebooting
continue
fi
break
done


