import requests
import time

def make_request():
    try:
        response = requests.get("http://10.109.126.114:32216/api/ping", timeout=0.1)
        response.raise_for_status()
          
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def main():
    serviceIsDown = 0
    while True:
        result = make_request()
        print("result: ",result )            
        if  result is None and serviceIsDown == 0: 
            start_time = time.time()
            serviceIsDown = 1
            print("Service Is Down")
        elif  result == "pong" and serviceIsDown == 1: 
            end_time = time.time()
            serviceIsDown = 0
            print("Service Is Up")
            print("Time Service Was Down for : ", end_time - start_time," seconds", " from: ", start_time, " to: ", end_time)
        time.sleep(1)
    
if __name__ == "__main__":
    main()
