# admin-tools
Administrative tools - these require credentials from your system administrator, that will be in a form like [this](https://github.com/practable/credentials-example)

## Prerequsites

- [jq](https://stedolan.github.io/jq/)
- [websocat](https://github.com/vi/websocat)
- [mo](https://github.com/tests-always-included/mo)
- [relay](https://github.com/practable/relay)

For logins via shellrelay, you will get remote host authentication warnings unless you add this line to `~/.ssh/config` (you may need to create the file, in which case you only need this line, no other lines are required)
```
NoHostAuthenticationForLocalhost yes
```

### For token
- python 3
- extra modules required: `humanize`, `pytest`, `pyjwt`

## Session relay

For a quick look at which , say, `trus` experiments are connected, use:

```
./getSessionStats.s | grep trus
```

To see details of message traffic, show extra lines, this example is 

```
$ ./getSessionStats.sh| grep trus -A 18 -B1
  {
    "topic": "trus00-video",
    "canRead": false,
    "canWrite": true,
    "connected": "2022-09-06 17:57:32.005911887 +0000 UTC m=+5005749.041827758",
    "remoteAddr": "129.215.182.88",
    "userAgent": "Go-http-client/1.1",
    "stats": {
      "tx": {
        "last": "20.01161ms",
        "size": 5783,
        "fps": 23.869676144597026
      },
      "rx": {
        "last": "Never",
        "size": 0,
        "fps": 0
      }
    }
  },
--
  {
    "topic": "trus00-data",
    "canRead": true,
    "canWrite": true,
    "connected": "2022-09-06 17:56:36.299197457 +0000 UTC m=+5005693.335113328",
    "remoteAddr": "129.215.182.88",
    "userAgent": "Go-http-client/1.1",
    "stats": {
      "tx": {
        "last": "1.361034858s",
        "size": 65,
        "fps": 1.1077586188437158
      },
      "rx": {
        "last": "210h28m24.519900974s",
        "size": 9,
        "fps": 0.06805585812345667
      }
    }
  },
```

If you are not getting data, check that the access server is working ok (this example is working ok)

```
./checkAccess.sh
$client_token=ey...
https://relay-access.practable.io/session/stats
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    91  100    91    0     0   1716      0 --:--:-- --:--:-- --:--:--  1716
{"uri":"wss://relay.practable.io/session/stats?code=575bf3fd-de78-4349-a9d6-04788fd19ed7"}
```
##  Shellrelay

Note that for a limited period, we are running an older version of the relay code for shell, and the latest version for shell2. Therefore with the latest version of relay installed on your admin machine, only shell2 scripts will work. The shell scripts will fail with a message about an audience in the JSON token. 


## Tokens

This script was written to support a specific use case, with the following features

- short duration tokens (three days) to be issued to students on various days during the semester
- the duration to exclude weekend working time (e.g. a three-day token starting on Friday ends on Wednesday, not Monday)

It relies on the admin credentials being available - see [private credentails repo](https://github.com/practable/credentials-uoe-soe) (note if this 404s it is because you are not an admin on our UoE system and hence won't have access to our credentials file).

### Usage
```
./generate <groups> <start_at> <every> <duration> <end_by> <code> <link_stub>
```


### Example 

```
cd tokens
./generate "truss everyone"  2022-10-04T06:00:00Z 1d 3d  2022-12-21T06:00:00Z truss22 "https://book.practable.io/?c="
```
Note that in the time strings, the T and Z are required to suit the time format, and timezone support is incomplete, so assume everything is in UTC.

The 'every', and 'duration' parameters support durations in a bash-like duration format (represented here in pseudo regexp form): `([0-9]*d)*(?[0-9]*h)*(?[0-9]*m)*(?[0-9]*s)*` i.e. `1d2h` would be 26 hours.

You run the tests in the script with `./test` because pytest ignores files that don't end in `.py` (so this script temporarily makes a file with the right ending, then deletes it after the tests).

The output from the script is found in `./output/<now>`. The `generate` script relies on finding the `user-token.sh` script in the same directory, hence the decision to use automatically-created subdirectories rather than try and get both scripts on the path.

You can check the token details in the `./output/<now>/validated-tokens.csv` file. This is the file to share with your course organiser, so they can distribute the links to their students. The output might look something like this:

|link                                                             |nbf_ts    |nbf                |exp                |signature|duration|groups               |
|-----------------------------------------------------------------|----------|-------------------|-------------------|---------|--------|---------------------|
|https://book.practable.io/?c=truss22-Tue-04-Oct-for-3-days-5YAXQ1|1664875038|2022-10-04 09:17:18|2022-10-07 09:17:18|True     |3 days  |['truss', 'everyone']|
|https://book.practable.io/?c=truss22-Wed-05-Oct-for-5-days-BC12JK|1664946000|2022-10-05 05:00:00|2022-10-10 05:00:00|True     |5 days  |['truss', 'everyone']|
|https://book.practable.io/?c=truss22-Thu-06-Oct-for-5-days-G78MV1|1665032400|2022-10-06 05:00:00|2022-10-11 05:00:00|True     |5 days  |['truss', 'everyone']|


## Develop

Before making this repo public it was scanned for secrets using [git secrets](https://github.com/msalemcode/git-secrets), including these [patterns](https://github.com/timdrysdale/git-secrets-patterns).

```
git secrets --scan-history
```
