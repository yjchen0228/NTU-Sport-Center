# NTU-Sport-Center 台大綜合體育館(新體) Gym and Swimming Pool Attendance web crawler

[台大綜合體育館]( <https://rent.pe.ntu.edu.tw/> "Title") 場館人數爬蟲，自06:00到21:30，每五分鐘抓取場館人數，22:00會畫出該日的人數折線圖

It can run on a Raspberry Pi 4B, recording the NTU Sport Center attendance from 06:00-21:30.

At 22:00 it will generate the line graph of attendance.

Before running gym.py, you should install packages required:

```pip install pyppeteer matplotlib pandas asyncio```

After that you can run gym.py using:

```python3 gym.py```

