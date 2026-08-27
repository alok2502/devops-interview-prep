# Gap Topic: Leap Second

## What it is
An occasional **one-second adjustment** added to UTC to keep atomic clocks in sync with the
Earth's (slightly irregular, gradually slowing) rotation. Result: very rarely a minute has
**61 seconds** — `23:59:59 → 23:59:60 → 00:00:00`.

## Why it matters (Linux/DevOps)
Software that assumes a minute is always 60 seconds can break on the `:60`:
- **Crash/hang** — 2012 leap second hit a Linux kernel bug (livelock, CPUs at 100%) → took down
  Reddit, LinkedIn, Mozilla, and others. Famous real outage.
- Time going backward/freezing → breaks time math, timestamps, TLS cert validity windows,
  distributed systems relying on synced clocks (DBs, consensus, logs).

## Modern fix: Leap Smearing
Instead of inserting one jarring extra second, **spread that second gradually over many hours**
(slow all clocks by a tiny fraction across a day) → no system ever sees `:60` or a backward jump.
**AWS and Google do leap smearing on their NTP time servers.** Sync your servers to such an NTP
source → handled smoothly.

## Interview summary
"A leap second is a one-second adjustment to UTC for the Earth's irregular rotation, so a minute
can rarely have 61 seconds. It matters because software assuming 60-second minutes can break — the
2012 leap second caused a Linux kernel bug that took down Reddit and LinkedIn. Modern systems use
'leap smearing' — spreading the second gradually so clocks never jump — which AWS and Google do on
their NTP servers."

## Theme
NTP / clock synchronization is critical infrastructure. Even a 1-second glitch can cause outages
in distributed systems. Keep systems synced to a reliable NTP source.
