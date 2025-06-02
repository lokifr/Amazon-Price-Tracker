import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv


#loadinf env variables
load_dotenv()
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"path_of_env_file\.env")


#headers
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}

my_email = os.getenv("EMAIL")
passwd = os.getenv("PASSWORD")
url = "https://appbrewery.github.io/instant_pot/" # the example webite that i used
response = requests.get(url, headers=header)
html = response.text
soup = BeautifulSoup(html, "html.parser")
price = soup.find(class_="aok-offscreen").text
price_wo_currency = price.split("₹")[1]
price_as_float = float(price_wo_currency)
print(type(price_as_float))
p_name = soup.find(id="productTitle").get_text().strip()
print(f"Email: {my_email}, Password set: {passwd is not None}")


#sending mail
if price_as_float < 100:
    message = f"{p_name} is on sale for {price}!"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection: 
        connection.starttls()
        connection.login(user=my_email, password=passwd)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="to_email",
            msg="Subject:Price Alert\n\nThe price has dropped!"
        )
