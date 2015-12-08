#!/usr/bin/python

import main

reboot = [100]
while True:
    exit_code = main.main()
    print(str(exit_code))
    if exit_code in reboot:
        print("rebooting")
        continue
    break
