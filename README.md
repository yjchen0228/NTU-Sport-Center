
# NTU-Sport-Center 台大綜合體育館(新體) Gym and Swimming Pool Attendance web crawler

[台大綜合體育館]( <https://rent.pe.ntu.edu.tw/> "Title") 場館人數爬蟲，自06:00到21:30，每五分鐘抓取場館人數，22:00會畫出該日的人數折線圖

It can run on a Raspberry Pi 4B, recording the NTU Sport Center attendance from 06:00-21:30.

At 22:00 it will generate the line graph of attendance.
![2023-12-29-Fri](https://github.com/yjchen0228/NTU_Sport_Center/assets/107047202/edd7c178-3f67-4c31-9c1e-446be676a1d4)

In the end of the week (Sunday), it will plot the whole week's attendance (Attendance of one day will show in the the same cplor).
![weekly_aligned_2023-12-31-Sun](https://github.com/yjchen0228/NTU_Sport_Center/assets/107047202/d685aede-510b-4418-a4d3-bbc9e32e9f5b)


Before running gym.py, you should install packages required:

```pip install pyppeteer matplotlib pandas asyncio```

After that you can run gym.py using:

```python3 gym.py```

