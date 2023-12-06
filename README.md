# NTU-Sport-Center Gym and Swimming Pool Attendance web crawler

台大綜合體育館場館人數爬蟲

It can run on a Raspberry Pi 4B, recording the NTU Sport Center attendance from 06:00-21:30.

At 22:00 it will generate the line graph of attendance.

Before running gym.py, you should install packages required:

```pip install pyppeteer matplotlib pandas asyncio```

After that you can run gym.py using:

```python3 gym.py```

