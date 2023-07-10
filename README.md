# admin-tools-legacy

If you are setting up a new system, please see [practable/getting-started](https://github.com/practable/getting-started) 

This is the repo used to administer both the AWS and GCE versions of the practable services during academic year 2022-23, including serving pendulums and spinners to engineering design 1 in semester 2 (i.e. Q1 2023), using the (then) new booking system and the (then) new single instance version of the cloud services that we hosted at dev.practable.io. This repo is fork of [practable/admin-tools](https://github.com/practable/admin-tools) as of July 2023, before it was updated to include previously-private details of the setting up the GCE instance, and removal of the AWS-related tools (so as to avoid confusion for new adopters). This move was prompted by contact from a potential new user who wants to set up their own instance.

Note - this repo may still receive updates to handle migrations from the AWS system, but all other improvements to be used in future should be made within [practable/admin-tools](https://github.com/practable/admin-tools) 

## Contents

This repo contains scripts to help administer our two currently-running systems.

- aws (running on relay v0.2.3 with instant-use non-cancellable bookings)
- gce-develop (running latest relay with advance, cancellable bookings)

The tools for each system are in a different directory, because they have different pre-requisites.

## Setup

### Practable binaries

Clone the repo, then run the install scripts for each system

```
cd aws
./install.sh
cd ../gce-develop
./install.sh
```

This will install the correct version of the practable binaries for interacting with each system.

### Other pre-requsites

There are additional pre-requisites you may need to install, depending on which system(s) you are using.


- [jq](https://stedolan.github.io/jq/)
- [websocat](https://github.com/vi/websocat)
- [mo](https://github.com/tests-always-included/mo)
- [relay](https://github.com/practable/relay)
- [yq](https://github.com/mikefarah/yq)


## Overview

We currently run a fleet of 129 experiments

10 x gen 1 spinners (on hold)
10 x gen 1 turners (on hold)
10 x gen 1 governors (on hold)
48 x gen 2 spinners (spin30-77)
32 x gen 1 pendulums (pend00-40, with some loaned to other locations)
8 x medium trusses (trus00-08)
5 x pocket VNA one-port (pvna00-04)
6 x pocket VAN two-port (pvna05-10)

All experiments use the AWS system's shellrelay for administrative access. Some experiments connect only to the shellrelay2, some connect to shellrelay as well
All gen 2 spinners and gen 1 pendulums send video and data to both systems, but are currently only bookable on the gce-develop system.
All trusses and pvna are bookable through the aws system only.

It is intended to migrate all experiments to have their data and video directed only to the new system, and retire the sessionrelay and bookrelay service on aws, but keep the shellrelay (for the time being).

## System status

### Experiment health

See what is connected using `./aws/shellrelay/identify2.sh`

## Experiment video and data connections

Check what is connected and streaming using the `./gce-develop/relay/getStats.sh` or `./aws/sessionrelay/getSessionStats.sh` scripts, depending which system is of interest.

## Manifest

See separate repos for manifests

[manifest-aws](https://github.com/practable/manifest-aws)
[manifest-gce-develop](https://github.com/practable/manifest-gce-develop)

## Tokens

### AWS

there are token generation scripts in `./aws/tokens`, such as `./generate` that provides a set of links starting every given interval for a given duration 


Usage:
```
generate <groups> <start_datetime> <every> <duration> <end_datetime> <code> <link_stub>
```

Example::
```
generate "truss everyone"  2022-10-05T07:00:00Z 1d 3d  2022-12-21T07:00:00Z truss22 "https://book.practable.io/?c="
```

### gce-develop


A different approach is taken where actual individual bookings are generated (or pairs or more of bookings) according to a `booking-plan.yaml`

Go to `./gce-develop/book` and edit `booking-plan.yaml` 

The format is like this:

```
---
slot_lists:
  pend:
    policy: p-engdes1-lab-pend
    slots:
    - sl-engdes1-lab-pend00
    - sl-engdes1-lab-pend02
    - sl-engdes1-lab-pend03
    - sl-engdes1-lab-pend04
    - sl-engdes1-lab-pend05
    - sl-engdes1-lab-pend06
    - sl-engdes1-lab-pend07       
    - sl-engdes1-lab-pend08
    - sl-engdes1-lab-pend09
    - sl-engdes1-lab-pend10
    - sl-engdes1-lab-pend11
    - sl-engdes1-lab-pend12
    - sl-engdes1-lab-pend13
    - sl-engdes1-lab-pend14
    - sl-engdes1-lab-pend15
    - sl-engdes1-lab-pend16
    - sl-engdes1-lab-pend17       
    - sl-engdes1-lab-pend20
    - sl-engdes1-lab-pend21
    - sl-engdes1-lab-pend22
    - sl-engdes1-lab-pend23
    - sl-engdes1-lab-pend36
    - sl-engdes1-lab-pend26
    - sl-engdes1-lab-pend27       
    - sl-engdes1-lab-pend28
    - sl-engdes1-lab-pend29
    - sl-engdes1-lab-pend31
    - sl-engdes1-lab-pend33
    - sl-engdes1-lab-pend34
    - sl-engdes1-lab-pend35
    
  spin:
    policy: p-engdes1-lab-spin
    slots: 
    - sl-engdes1-lab-spin30
    - sl-engdes1-lab-spin32
    - sl-engdes1-lab-spin33
    - sl-engdes1-lab-spin34
    - sl-engdes1-lab-spin35
    - sl-engdes1-lab-spin36
    - sl-engdes1-lab-spin37       
    - sl-engdes1-lab-spin38
    - sl-engdes1-lab-spin39
    - sl-engdes1-lab-spin40
    - sl-engdes1-lab-spin41
    - sl-engdes1-lab-spin46
    - sl-engdes1-lab-spin47       
    - sl-engdes1-lab-spin48
    - sl-engdes1-lab-spin49
    - sl-engdes1-lab-spin51
    - sl-engdes1-lab-spin52
    - sl-engdes1-lab-spin53
    - sl-engdes1-lab-spin54
    - sl-engdes1-lab-spin55
    - sl-engdes1-lab-spin56
    - sl-engdes1-lab-spin57       
    - sl-engdes1-lab-spin58
    - sl-engdes1-lab-spin59
    - sl-engdes1-lab-spin60
    - sl-engdes1-lab-spin61
    - sl-engdes1-lab-spin62
    - sl-engdes1-lab-spin63
    - sl-engdes1-lab-spin65
    - sl-engdes1-lab-spin66   
windows:
  friday-10-mar-10am-12pm:
    start: 2023-03-10T09:59:59Z
    end:   2023-03-10T12:00:01Z
  monday-13-mar-2pm-4pm:
    start: 2023-03-13T13:59:59Z
    end:   2023-03-13T16:00:01Z
  monday-13-mar-4pm-6pm:
    start: 2023-03-13T15:59:59Z
    end:   2023-03-13T18:00:01Z
  tuesday-14-mar-2pm-4pm:
    start: 2023-03-14T13:59:59Z
    end:   2023-03-14T16:00:01Z
  tuesday-14-mar-4pm-6pm:
    start: 2023-03-14T15:59:59Z
    end:   2023-03-14T18:00:01Z      
sessions:
  friday-10-mar-2023-12pm-A:
    prefix: engdes1
    suffix: pend-then-spin
    bookings:
      - start: 2023-03-10T10:10:01Z
        end:   2023-03-10T11:09:59Z
        slot_list: pend 
      - start: 2023-03-10T11:10:00Z
        end:   2023-03-10T11:59:59Z
        slot_list: spin
  friday-10-mar-2023-12pm-B:
    prefix: engdes1
    suffix: spin-then-pend
    bookings:
      - start: 2023-03-10T10:10:00Z
        end:   2023-03-10T11:09:59Z
        slot_list: spin
      - start: 2023-03-10T11:10:01Z
        end:   2023-03-10T11:59:59Z
        slot_list: pend 
  monday-13-mar-2023-2pm-A:
    prefix: engdes1
    suffix: pend-then-spin
    bookings:
      - start: 2023-03-13T14:10:01Z
        end:   2023-03-13T15:09:59Z
        slot_list: pend
      - start: 2023-03-13T15:10:00Z
        end:   2023-03-13T15:59:59Z
        slot_list: spin
  monday-13-mar-2023-2pm-B:
    prefix: engdes1
    suffix: spin-then-pend
    bookings:
      - start: 2023-03-13T14:10:00Z
        end:   2023-03-13T15:09:59Z
        slot_list: spin
      - start: 2023-03-13T15:10:01Z
        end:   2023-03-13T15:59:59Z
        slot_list: pend
  monday-13-mar-2023-4pm-A:
    prefix: engdes1
    suffix: pend-then-spin
    bookings:
      - start: 2023-03-13T16:10:01Z
        end:   2023-03-13T17:09:59Z
        slot_list: pend
      - start: 2023-03-13T17:10:01Z
        end:   2023-03-13T17:59:59Z
        slot_list: spin
  monday-13-mar-2023-4pm-B:
    prefix: engdes1
    suffix: spin-then-pend
    bookings:
      - start: 2023-03-13T16:10:01Z
        end:   2023-03-13T17:09:59Z
        slot_list: spin
      - start: 2023-03-13T17:10:01Z
        end:   2023-03-13T17:59:59Z
        slot_list: pend
  tuesday-14-mar-2023-2pm-A:
    prefix: engdes1
    suffix: pend-then-spin
    bookings:
      - start: 2023-03-14T14:10:01Z
        end:   2023-03-14T15:09:59Z
        slot_list: pend
      - start: 2023-03-14T15:10:01Z
        end:   2023-03-14T15:59:59Z
        slot_list: spin
  tuesday-14-mar-2023-2pm-B:
    prefix: engdes1
    suffix: spin-then-pend
    bookings:
      - start: 2023-03-14T14:10:01Z
        end:   2023-03-14T15:09:59Z
        slot_list: spin
      - start: 2023-03-14T15:10:01Z
        end:   2023-03-14T15:59:59Z
        slot_list: pend
  tuesday-14-mar-2023-4pm-A:
    prefix: engdes1
    suffix: pend-then-spin
    bookings:
      - start: 2023-03-14T16:10:01Z
        end:   2023-03-14T17:09:59Z
        slot_list: pend
      - start: 2023-03-14T17:10:01Z
        end:   2023-03-14T17:59:59Z
        slot_list: spin
  tuesday-14-mar-2023-4pm-B:
    prefix: engdes1
    suffix: spin-then-pend
    bookings:
      - start: 2023-03-14T16:10:01Z
        end:   2023-03-14T17:09:59Z
        slot_list: spin
      - start: 2023-03-14T17:10:01Z
        end:   2023-03-14T17:59:59Z
        slot_list: pend          
```


The above plan produces 30 pairs of bookings for each of 10 sessions, for a total of 600 bookings.

More details on how to upload these bookings (including keeping existing user bookings) is [here](./gce-develop/book/README.ms)

The booking links are provided in `gce-develop/book/data/booking-links.txt` with each line containing a description and a booking link similar to

```
engdes1-2023-Mar-14-Tue-1610-1759-spin-then-pend-029-abc123, https://dev.practable.io/book/?s=abc123
```


