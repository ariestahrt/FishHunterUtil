import whois
import tldextract
from datetime import datetime
import time

def convert_date(date_str):
    rtr = None
    # "2023-01-27T04:29:33.0Z"
    dateformat = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S.%f%z",
        "%Y-%m-%d %H:%M:%S.%f%Z",
    ]

    for f in dateformat:
        try:
            rtr = datetime.strptime(date_str, f)
            break
        except:
            pass
    
    return rtr

def get_whois(url):
    extracted = tldextract.extract(url)
    apex_domain = extracted.registered_domain
    print(">> Apex domain: " + apex_domain)
    w = None
    try:
        w = whois.whois(apex_domain)
    except Exception as e:
        print(">> Error getting whois for: ", apex_domain)
        print(">> Error: ", e)

        if "Your connection limit exceeded" in str(e):
            time.sleep(10)
            return get_whois(url)

        return {}
    print(w)

    registrar = w.registrar

    expiration_date = str(w.expiration_date)
    creation_date = str(w.creation_date)
    updated_date = str(w.updated_date)

    if type(w.expiration_date) == list:
        expiration_date = str(w.expiration_date[-1])
    
    if type(w.creation_date) == list:
        creation_date = str(w.creation_date[-1])
    
    if type(w.updated_date) == list:
        updated_date = str(w.updated_date[-1])
    
    raw_data = w.text

    registrar_url = None
    if "Registrar URL:" in raw_data:
        registrar_url = raw_data.split("Registrar URL:")[1].split("\n")[0].strip()

    # convert to datetime
    expiration_date = convert_date(expiration_date)
    creation_date = convert_date(creation_date)
    updated_date = convert_date(updated_date)

    print(">> Registrar: ", registrar)
    print(">> Created at: ", creation_date)
    print(">> Updated at: ", updated_date)
    print(">> Expires at: ", expiration_date)
    print(">> Registrar URL: ", registrar_url)

    return {
        "domain_name": apex_domain,
        "registrar_name": registrar,
        "created_date": expiration_date,
        "updated_date": creation_date,
        "expires_date": updated_date,
        "registrar_url": registrar_url,
        "raw_data": raw_data
    }

if __name__ == "__main__":
    print(get_whois("https://something.freenom.ga/"))