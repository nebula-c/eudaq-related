#!/usr/bin/env python3

import os
import json
import time
import requests
import argparse
from rich import print
from rich.rule import Rule
import subprocess
import os
import random


def send_to_mm(channel, msg, hook_url):
    print(msg)
    # return True
    r = requests.post(
        hook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"text":msg,"channel":channel})
    )
    if r.text == "ok":
        return True
    print(r.json())
    return False

def send_to_mm_with_image(channel, msg, hook_url, image_url):
    print(msg)
    r = requests.post(
        hook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"text":msg,"channel":channel, "attachments":[{"image_url":image_url}]})
    )
    if r.text == "ok":
        return True
    print(r.json())
    return False

def get_tmux_screentext(paneId = "00", full = False):
    if full:
        os.system(f"tmux capture-pane -p -J -t %{paneId} > /tmp/tmux.txt")    
    else:
        os.system(f"tmux capture-pane -p -J -S 7 -E 18 -t %{paneId} > /tmp/tmux.txt")
    with open("/tmp/tmux.txt", "r") as f:
        return f.read()

if __name__=="__main__":
    parser = argparse.ArgumentParser("Watch the status of datataking and inform on Mattermost.")
    parser.add_argument("channel", help="Mattermost channel to write to.")
    parser.add_argument("--interval", "-i", default=10, type=float, help="Monitoring interval in minutes (default 5).")
    parser.add_argument("--only-critical", "-c", action="store_true", help="Send only critical messages.")
    parser.add_argument("--test", action="store_true", help="Test connection to Mattermost and exit.")
    parser.add_argument("--hook", default="https://mattermost.web.cern.ch/hooks/k6pnuqmky3fo3k36ipd5t3gs6e", help="Mattermost webhook URL")
    parser.add_argument("--scopeOn", action="store_true", help="Send scope ready for trigger when no trigger 10 min")
    parser.add_argument('--address', '-add', default="10.0.0.11", help='Address of the socpe (default: 10.0.0.11')
    args = parser.parse_args()

    GlobalEventN = None
    wasRunOnGoing = True

    if args.test:
        if send_to_mm(args.channel, "Testing watchdog", hook_url=args.hook):
            print("[green]Test successful, check MM channel![/green]")
        else:
            print("[bold red]Test failed![/bold red]")
        tmuxText = get_tmux_screentext("00", True)
        send_to_mm(args.channel, f"```\n{tmuxText}```", hook_url=args.hook)
        msg = f"Current status of SPS page 1"
        send_to_mm_with_image(args.channel, msg, args.hook, f"https://vistar-capture.s3.cern.ch/sps1.png?{random.random()}")
        exit()

    
    print(Rule("Watchdog operational! Bark bark!",characters="="))
    if not send_to_mm(args.channel, "Watching...", args.hook):
        print("[bold red]Problem with sending message to Mattermost![/bold red]")
        exit()
    time.sleep(120)
    try:
        count = 0
        while True:
            tmuxText = get_tmux_screentext(00, True)
            if "RUNNING" not in tmuxText:
                if not args.only_critical:
                    send_to_mm(args.channel, "@all DAQ not running! waiting for 5 mins @usavino @blim", args.hook)
                tmuxText = get_tmux_screentext("00", True)
                send_to_mm(args.channel, f"```\n{tmuxText}```", hook_url=args.hook)
                time.sleep(5*60)

            currentEvent = tmuxText.split("RUNNING")[1].strip().split()[0]
            print(f"Current event: {currentEvent} (last: {GlobalEventN})")
            if GlobalEventN is not None: # second iteration
                if float(currentEvent) == float(GlobalEventN):
                    if wasRunOnGoing:
                        # When the run was ongoin before, we will send the notification
                        msg = f"[Warning] Event counter unchanged in the past {args.interval} minutes! @usavino @blim"
                        send_to_mm(args.channel, msg, args.hook)
                        if args.scopeOn:
                            # And send ready trigger signal to the scope
                            try:
                                # Hard coded but it works... sorry for bad code!
                                subprocess.run("/home/palpidefs/SPS_Testbeam_Nov_2022/scopetest.py --displayOn --ready", shell=True)
                                msg = f"Send the ready signal to the scope.. Success!"
                                send_to_mm(args.channel, msg, args.hook)
                                msg = f"Current status of SPS page 1"
                                send_to_mm_with_image(args.channel, msg, args.hook, f"https://vistar-capture.s3.cern.ch/sps1.png?{random.random()}")
                            except:
                                msg = f"Couldn't connect to scope!! @blim"
                                send_to_mm("testbot", msg, args.hook)
                    # Change wasRunOnGoing to False to prevent further notification.
                    wasRunOnGoing = False
                else:
                    if wasRunOnGoing is False:
                        # Number of event was changed while the run was stopped
                        msg = f"[Recovered] Event counter changed, continue data taking.. @usavino @blim"
                        send_to_mm(args.channel, msg, args.hook)
                        # Now run is on going..
                        wasRunOnGoing = True
                    print(f"[green]Current events: {currentEvent} [/green]")
                if float(currentEvent) < 1:
                    msg = f"[Warning] Event counter is 0! @usavino @blim (could be a new run?)"
                    send_to_mm(args.channel, msg, args.hook)
                    subprocess.run("/home/palpidefs/SPS_Testbeam_Nov_2022/scopetest.py --displayOff --ready", shell=True)
            else: # First time
                GlobalEventN = currentEvent
                msg = f"Event counter started from {currentEvent}"
                send_to_mm(args.channel, msg, args.hook)
            # time.sleep(args.interval)
            GlobalEventN=currentEvent
            count += 1
            if count%6 == 0:
                msg = f"Still alive! Events: {currentEvent}"
                send_to_mm(args.channel, msg, args.hook)
            time.sleep(args.interval*60)
    except KeyboardInterrupt:
        send_to_mm(args.channel, "Watchdog stopped.", args.hook)
    except Exception as e:
        send_to_mm(args.channel, f"Exception: {e}", args.hook)
        pass
