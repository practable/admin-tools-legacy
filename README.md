# admin-tools
Administrative tools - these require credentials from your system administrator (no credentials included in the repo)

## Prerequsites

- [jq](https://stedolan.github.io/jq/)
- [websocat](https://github.com/vi/websocat)
- [mo](https://github.com/tests-always-included/mo)


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
## 
