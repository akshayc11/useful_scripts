# Slackbot.py

Table of Contents
=================

   * [Slackbot.py](#slackbotpy)
      * [Description](#description)
      * [Note](#note)
      * [Additional Information](#additional-information)
      * [Download](#download)

## Description

Given a username and a pointer to the file with a URL for an incoming webhook from Slack, this script periodically checks for updates to the SLURM queue list for jobs pertaining to the user, and will make posts regarding any changes in status to the webhook.

## Note
This is a simple script in python that should be run as a polling background job in the head node for a single user. 

## Additional Information
To get more information about incoming webhooks, check out [this link](https://api.slack.com/incoming-webhooks)

## Download
The script can be downloaded from [here](http://akshayc.com/useful_scripts/python/slack_SLURM/slackbot.py).

## [Go back to home](http://akshayc.com/useful_scripts)