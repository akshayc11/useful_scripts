#!/usr/bin/python

# Author: Akshay Chandrashekaran
# Email: web@akshayc.com
# Copyright 2017

# This script will crawl through squeue periodically, 
# and if it detects any change to a relevant job, it
# will fire off a post to the slack URL

# For safety, I am reading the information from a file
# whose permission is set to be read only by me.
# You can do your own for your own work
# requires slackweb

import argparse
import subprocess
import time
import slackweb


cmd_template = 'squeue -u {} | grep -v "JOBID PARTITION"'
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    This script will check the status of the jobs of a specified
    user every 10 seconds, and if it detects a change, it will send
    a message to a specified webhook obtained from a file of your choosing.
    For security make sure the file can be read only by you.
    NOTE: Requires slackweb package (pip install slackweb)
    ''')

    parser.add_argument('--user', required=True, type=str, help='name of user')
    parser.add_argument('--url-file', required=True, type=str, help='file where webhook url is stored')
    parser.add_argument('--check-period', type=int, help='time between checks (should be >=3)', default=10)

    args = parser.parse_args()

    if args.check_period < 3:
        raise Exception('Not accepting values < 3')

    with open(args.url_file) as f:
        webhook_url = f.readline().strip()

    slack = slackweb.Slack(url=webhook_url)
    user = args.user
    cmd = cmd_template.format(user)
    job_dict = {}
    headline = subprocess.check_output('squeue | head -n1', shell=True).strip()
    while True:
        output = subprocess.check_output(cmd, shell=True).strip().split('\n')
        new_dict = {}
        for line in output:
            if 'error' in line:
                text='Encountered error in line for user: {}. \nKill slackbot in coe and try again'.format(user)
                slack.notify(text=text,
                             icon_emoji=':ghost:')
                break
            else:
                comps = line.strip().split()
                jid = int(comps[0])
                partition = comps[1]
                jobname = comps[2]
                uid = comps[3]
                status =comps[4]
                t = comps[5]
                nodes = comps[6]
                nodelist = comps[7]
                new_dict[jid] = [status, line.strip()]
                if jid not in job_dict:
                    # New job
                    text = 'New job initialized:\n{}\n{}'.format(headline, line.strip())
                    slack.notify(text=text)
                else:
                    if job_dict[jid][0] != status:
                        # Change in status
                        text = 'Change in status of job {}. (old: {}) (new: {})\n{}\n{}'.format(jid,
                                                                                                job_dict[jid][0],
                                                                                                new_dict[jid][0],
                                                                                                headline,
                                                                                                line.strip())
                        slack.notify(text=text)
                    del job_dict[jid]
                        
        # All lines have been parsed
        for jid in job_dict:
            # These are jobs that dont exist in queue.
            text = 'Job {} may be complete. Last status: \n{}\n{}'.format(jid, headline, job_dict[jid][1].strip())
            slack.notify(text=text)
        job_dict = new_dict
        # Sleep
        time.sleep(args.check_period)
