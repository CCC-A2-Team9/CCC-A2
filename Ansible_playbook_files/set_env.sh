#!/usr/bin/env bash

. ./unimelb-COMP90024-2022-grp-9-openrc.sh; ansible-playbook --ask-become-pass set_env.yaml -i inventory/app_host.ini