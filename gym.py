import datetime
import asyncio
import csv
import matplotlib.pyplot as plt
import pandas as pd
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
    plt_title=now.strftime("%Y-%m-%d") + " Gym and Swimming Pool Attendance Over Time"
    df = pd.read_csv(filename, parse_dates=['Timestamp'])
    #df = pd.read_csv(filename, parse_dates=['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date
    today_data = df[df['Date'] == now.date()]

    plt.figure(figsize=(10, 6))
    plt.plot(today_data['Timestamp'], today_data['Gym'], label='Gym')
    plt.plot(today_data['Timestamp'], today_data['Swimming Pool'], label='Swimming Pool')

    # Format x-axis to show only hour and minute
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))

    plt.xlabel('Time')
    plt.ylabel('Attendance')
    plt.title(plt_title)
    plt.legend()
    plt.xticks(rotation=45)  # Rotate labels for better readability
    plt.tight_layout()  # Adjust layout
    plt.savefig(plot_filename)
    plt.show()
# Main loop
last_scraped_time = None
while True:
    # Data scraping
    if is_time_to_scrape():
        if last_scraped_time is None or (datetime.datetime.now() - last_scraped_time).seconds >= 300:
            data1, data2 = asyncio.get_event_loop().run_until_complete(scrape_website())
            if data1 != "Not found" and data2 != "Not found":
                append_to_csv(data1, data2)
            last_scraped_time = datetime.datetime.now()
            Swimming="Swimming Pool:"+str(data1) 
            Gym="Gym: "+str(data2)
            print(Swimming)
            print(Gym)
    # Plot at 22:00
    if datetime.datetime.now().time() >= datetime.time(22, 0) and (datetime.datetime.now() - last_scraped_time).seconds >= 900:
        print("plotting")
        plot_data()
        break  # End the script after plotting or modify as needed
    #print("sleeping for 60 sec")
    time.sleep(60)  # Sleep for a minute before next check
