#!/usr/bin/env python3

import os
import json
import time
import requests
import argparse
from rich import print
from rich.rule import Rule
import random
import sys
sys.path.append("/home/hipex/ITS3/trigger/software")
from checkTrig import *
import subprocess
# sys.path.append("/home/palpidefs/TB_SPS_June_2023/opamp-utils/QA")
# from uploadImage import ImageUploader

def send_to_mm(channel, msg, hook_url):
    # print(msg)
    r = requests.post(
        hook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"text":msg,"channel":channel})
    )
    if r.text == "ok":
        return True
    print(r.json())
    return False
    # return True

def send_to_mm_with_image(channel, msg, hook_url, image_url):
    # print(msg)
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
        os.system(f"tmux capture-pane -p -J -t %{paneId} > /home/palpidefs/tmux.txt")    
    else:
        os.system(f"tmux capture-pane -p -J -S 7 -E 18 -t %{paneId} > /home/palpidefs/tmux.txt")
    with open("/home/palpidefs/tmux.txt", "r") as f:
        return f.read()

def isBeamTrigger(threshold=100):
    numTrig = getScintTrig()
    print(f"numTrig: {numTrig}")
    if numTrig > 3000:
        return True
    else:
        return False

def getSPSPage1Status():
    link = "https://vistar-capture.s3.cern.ch/sps1.png"
    # Download it to the temp folder
    tempPath = "/tmp/sps1.png"
    os.system(f"wget -q -O {tempPath} {link}")
    imgUploader = ImageUploader()
    imgLink = imgUploader.upload(image=tempPath)
    # Remove the temp file
    os.system(f"rm {tempPath}")
    return imgLink
    

if __name__=="__main__":
    parser = argparse.ArgumentParser("Watch the status of datataking and inform on Mattermost.")
    parser.add_argument("channel", help="Mattermost channel to write to.")
    parser.add_argument("--interval", "-i", default=10, type=float, help="Monitoring interval in minutes (default 5).")
    parser.add_argument("--only-critical", "-c", action="store_true", help="Send only critical messages.")
    parser.add_argument("-t", "--test", action="store_true", help="Test connection to Mattermost and exit.")
    parser.add_argument("--hook", default="https://mattermost.web.cern.ch/hooks/uup6cn6xyinuid9n9z74psc14o", help="Mattermost webhook URL")
    # parser.add_argument("--hook", default="https://mattermost.web.cern.ch/hooks/k6pnuqmky3fo3k36ipd5t3gs6e", help="Mattermost webhook URL")
    parser.add_argument("--trig", action="store_true", help="Check trigger status")
    parser.add_argument("--scopeOn", action="store_true", help="Send scope ready for trigger when no trigger 10 min")
    args = parser.parse_args()
    
    GlobalEventN = None

    if args.test:
        # if send_to_mm_with_image(args.channel, "Current status of SPS page 1", args.hook, getSPSPage1Status()):
        #     print("[green]Test successful, check MM channel![/green]")
        # else:
        #     print("[bold red]Test failed![/bold red]")
        tmuxText = get_tmux_screentext("00", True)
        send_to_mm(args.channel, f"```\n{tmuxText}```", hook_url=args.hook)
        exit()
    # time.sleep(120)
    wasBeamOn = None
    GlobalEventN = None
    wasRunOnGoing = True
    print(Rule("EUDAQ pusher on",characters="="))
    if not send_to_mm(args.channel, "Activated", args.hook):
        print("[bold red]Problem with sending message to Mattermost![/bold red]")
        exit()
    try:
        count = 0
        while True:
            random.seed(random.randrange(999))
            tmuxText = get_tmux_screentext("00", True)
            try:
                send_to_mm(args.channel, f"```\n{tmuxText}```", hook_url=args.hook)
                send_to_mm_with_image(args.channel, "Current status of SPS page 1", args.hook, getSPSPage1Status())
            except:
               print("Error sending message")
               pass

            # Trigger
            # currentEvent = tmuxText.split("RUNNING")[1].strip().split()[0]
            # print(f"Current event: {currentEvent} (last: {GlobalEventN})")
            # if GlobalEventN is not None: # second iteration
            #     if float(currentEvent) == float(GlobalEventN):
            #         if wasRunOnGoing:
            #             # When the run was ongoin before, we will send the notification
            #             msg = f"[Warning] Event counter unchanged in the past {args.interval} minutes! @usavino @blim"
            #             print(msg)
            #             # send_to_mm(args.channel, msg, args.hook)
            #             if args.scopeOn:
            #                 # And send ready trigger signal to the scope
            #                 try:
            #                     # Hard coded but it works... sorry for bad code!
            #                     subprocess.run("/home/palpidefs/SPS_Testbeam_Nov_2022/scopetest.py --displayOn --ready", shell=True)
            #                     msg = f"Send the ready signal to the scope.. Success!"
            #                     print(msg)
            #                     # send_to_mm(args.channel, msg, args.hook)
            #                     msg = f"Current status of SPS page 1"
            #                     print(msg)
            #                     # send_to_mm_with_image(args.channel, msg, args.hook, f"https://vistar-capture.s3.cern.ch/sps1.png?{random.random()}")
            #                 except:
            #                     msg = f"Couldn't connect to scope!! @blim"
            #                     send_to_mm("testbot", msg, args.hook)
            #         # Change wasRunOnGoing to False to prevent further notification.
            #         wasRunOnGoing = False
            #     else:
            #         if wasRunOnGoing is False:
            #             # Number of event was changed while the run was stopped
            #             msg = f"[Recovered] Event counter changed, continue data taking.. @usavino @blim"
            #             print(msg)
            #             # send_to_mm(args.channel, msg, args.hook)
            #             # Now run is on going..
            #             wasRunOnGoing = True
            #         print(f"[green]Current events: {currentEvent} [/green]")
            # else: # First time
            #     GlobalEventN = currentEvent
            #     msg = f"Event counter started from {currentEvent}"
            #     send_to_mm(args.channel, msg, args.hook)
            # # time.sleep(args.interval)
            # GlobalEventN=currentEvent

            try:
                CurrentTriggerStatus = isBeamTrigger()
                if wasBeamOn is None:
                    wasBeamOn = CurrentTriggerStatus
                
                if CurrentTriggerStatus is not True:
                    print(f"[red]Beam is OFF[/red]")
                    if wasBeamOn is True:
                        subprocess.run("/home/palpidefs/SPS_Testbeam_Nov_2022/scopetest.py --displayOn --ready", shell=True)
                        send_to_mm(args.channel, f"[Warning] Scintillator trigger has no trigger input from the beam!! @all", hook_url=args.hook)
                        wasBeamOn = False
                else:
                    print(f"[green]Beam is ON[/green]")
                    if wasBeamOn is False:
                        send_to_mm(args.channel, f"[Recovered] Scintillator trigger got trigger input from the beam.. @all", hook_url=args.hook)
                        wasBeamOn = True
            except:
                print("Error in trigger check")
                pass
            
            time.sleep(args.interval*60)
    except KeyboardInterrupt:
        send_to_mm(args.channel, "Pusher stopped.", args.hook)
    except Exception as e:
        send_to_mm(args.channel, f"Exception: {e}", args.hook)
        raise e
