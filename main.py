import smtplib
import requests
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText

load_dotenv()
tm_api_key = os.environ.get("TM_API_KEY")
email = os.environ.get("EMAIL")
email_password = os.environ.get("EMAIL_PASSWORD")

artists = ["system of a down", "sam fender", "dadi freyr", "feu chatterton", "asaf avidan", "greta van fleet", "saez", "the strokes"]

msg = ""
for artist in artists:

    parameters = {
        "apikey": tm_api_key,
        "keyword": artist,
        "countryCode": "PL,DE,FR,CZ,NL,BE",
        "classificationName": "music"
    }

    response = requests.get(
        "https://app.ticketmaster.com/discovery/v2/events.json", params=parameters
    )


    if response.status_code != 200:
        msg += f"Error {response.status_code} with fetching data for {artist}\n"
        continue

    concert_data = response.json()
    if "_embedded" not in concert_data:
        msg += f"------------------------------\n{artist.upper()}:🎤🎸🎹\nNo concerts at the moment\n"
        continue

    list_of_events = concert_data["_embedded"]["events"]
    one_artist = []


    for data in list_of_events:
        data_name  = data["name"].split("|")[0].strip()
        event = {
            "Event name": data_name,
            "City" : data["_embedded"]["venues"][0]["city"]["name"],
            "Date" : data["dates"]["start"]["localDate"],
            "Concert venue" : data["_embedded"]["venues"][0].get("address", {}).get("line1", "Venue address unknown"),
            "Concert hour" : data["dates"]["start"].get("localTime", "Concert hour unknown"),
            "Link to tickets": data["url"]
        }
        one_artist.append(event)
    seen = []

    msg += f"------------------------------\n{artist.upper()}:🎤🎸🎹\n"

    for concert in one_artist:
        if (concert["City"], concert["Date"]) not in seen:
            seen.append((concert["City"], concert["Date"]))
            msg += f'Where: {concert["City"]}, {concert["Concert venue"]},\nWhen: {concert["Date"]}, {concert["Concert hour"]},\nTickets: {concert["Link to tickets"]}\n\n'
print(msg)

msg_code = MIMEText(msg, "plain", "utf-8")
msg_code["Subject"] = "Concert notif"
msg_code["From"] = email
msg_code["To"] = "angelaqwer@yahoo.com"



with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.ehlo()
    connection.starttls()
    connection.login(user=email, password=email_password)
    connection.sendmail(
        from_addr=email,
        to_addrs="angelaqwer@yahoo.com",
        msg=msg_code.as_string()
    )






