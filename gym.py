import datetime
import asyncio
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyppeteer import launch
import time
# Web scraping setup
url = "https://rent.pe.ntu.edu.tw/"
xpath1 = '//*[@id="CMain"]/div[4]/div/div[1]/div[2]/div[2]/div[1]/span'
xpath2 = '//*[@id="CMain"]/div[4]/div/div[1]/div[1]/div[2]/div[1]/span'

# Function to check if it's the correct time to scrape
def is_time_to_scrape():
    start_time = datetime.time(6, 0)  # 06:00
    end_time = datetime.time(21, 30)  # 21:30
    current_time = datetime.datetime.now().time()
    return start_time <= current_time <= end_time

# Function to scrape website
async def scrape_website():
    browser = None
    try:
        browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'], executablePath='/usr/bin/chromium-browser')
        page = await browser.newPage()
        await page.goto(url)
        await asyncio.sleep(5)

        elements1 = await page.xpath(xpath1)
        if elements1:
            text1 = await page.evaluate('(element) => element.textContent', elements1[0])
        else:
            text1 = 'Not found'

        elements2 = await page.xpath(xpath2)
        if elements2:
            text2 = await page.evaluate('(element) => element.textContent', elements2[0])
        else:
            text2 = 'Not found'

        return text1.strip(), text2.strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Error', 'Error'

    finally:
        if browser:
            await browser.close()

# Function to append data to CSV
import os
def append_to_csv(data1, data2, filename="data.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Swimming Pool', 'Gym'])  # Write headers
        
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        writer.writerow([current_time, data1, data2])

# Function to plot data
def plot_data(filename="data.csv"):
    now = datetime.datetime.now()
    plot_filename = now.strftime("%Y-%m-%d-%a") + '.png'
    plot_title = now.strftime("%Y-%m-%d") + " Gym and Swimming Pool Attendance Over Time"

    # Read data from CSV
    df = pd.read_csv(filename)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M')
    df['Gym'] = pd.to_numeric(df['Gym'], errors='coerce')
    df['Swimming Pool'] = pd.to_numeric(df['Swimming Pool'], errors='coerce')

    # Filter data for the current date
    today_data = df[df['Timestamp'].dt.date == now.date()]

    # Find the maximum attendance for gym and swimming pool
    max_gym = today_data['Gym'].max(skipna=True)
    max_swimming_pool = today_data['Swimming Pool'].max(skipna=True)
    
    # Determine the highest attendance number and round it up to the nearest ten
    max_attendance = max(max_gym, max_swimming_pool)
    y_axis_limit = np.ceil(max_attendance / 10) * 10  # Ceiling division to the nearest ten

    plt.figure(figsize=(10, 6))
    plt.plot(today_data['Timestamp'], today_data['Gym'], label='Gym')
    plt.plot(today_data['Timestamp'], today_data['Swimming Pool'], label='Swimming Pool')

    # Set Y-axis limits based on the maximum attendance rounded up
    plt.ylim(0, y_axis_limit)

    # Format x-axis to show only hour and minute
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))

    plt.xlabel('Time')
    plt.ylabel('Attendance')
    plt.title(plot_title)
    plt.legend()
    plt.xticks(rotation=45)  # Rotate labels for better readability
    plt.tight_layout()  # Adjust layout
    plt.savefig(plot_filename)
    #plt.show()
    plt.close('all') 
def plot_weekly_data_aligned(filename="data.csv"):
    df = pd.read_csv(filename)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M')
    df['Time'] = df['Timestamp'].dt.time  # Extract the time part

    # Define colors for different days
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

    # Start plotting
    plt.figure(figsize=(15, 8))
    
    # Get the minimum date to use as a baseline for alignment
    min_date = df['Timestamp'].dt.date.min()

    for i in range(7):
        # Calculate the date for i days ago
        day = (datetime.datetime.now() - datetime.timedelta(days=i)).date()
        day_data = df[df['Timestamp'].dt.date == day]
        
        if not day_data.empty:
            # Align timestamps by subtracting the date part and adding it to the baseline date
            aligned_timestamps = pd.to_datetime(min_date) + (day_data['Timestamp'] - day_data['Timestamp'].dt.normalize())
            plt.plot(aligned_timestamps, day_data['Gym'], label=day.strftime('%Y-%m-%d'), color=colors[i % len(colors)])
            plt.plot(aligned_timestamps, day_data['Swimming Pool'], color=colors[i % len(colors)])

    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    plt.xlabel('Time of Day')
    plt.ylabel('Attendance')
    plt.title('Weekly Gym and Swimming Pool Attendance Aligned by Time of Day')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    plot_filename = 'weekly_aligned_' + datetime.datetime.now().strftime("%Y-%m-%d-%a") + '.png'
    plt.savefig(plot_filename)
    #plt.show()
    plt.close('all') 
# Main loop
last_scraped_time = None
while True:
    # Data scraping
    if is_time_to_scrape():
        if last_scraped_time is None or (datetime.datetime.now() - last_scraped_time).seconds >= 300:
            data1, data2 = asyncio.get_event_loop().run_until_complete(scrape_website())
            if data1 not in ("Error", "Not found") and data2 not in ("Error", "Not found"):
                append_to_csv(data1, data2)
            last_scraped_time = datetime.datetime.now()
            Swimming="Swimming Pool:"+str(data1) 
            Gym="Gym: "+str(data2)
            print(Swimming)
            print(Gym)
    # Plot at 22:00
    
    today_filename = datetime.datetime.now().strftime("%Y-%m-%d-%a") + '.png'
    if not os.path.isfile(today_filename) and (datetime.datetime.now().time() >= datetime.time(22,0)):
        print("plotting...")
        plot_data()
        #break  # or continue based on your requirement

    time.sleep(60)
    
    if datetime.datetime.now().strftime("%A") == 'Sunday' and datetime.datetime.now().hour >= 22:
        plot_weekly_data_aligned("data.csv")
