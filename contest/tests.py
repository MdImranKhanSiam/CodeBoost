import requests

base_hex = "69f25b32e1a743ddd429"
start = int("93ca", 16)  # starting suffix in hex

i = start

while True:
    # Convert number back to 4-digit hex
    suffix = format(i, "04x")

    # Full generated ID
    generated_id = base_hex + suffix

    print(generated_id)

    url = f"https://your-api-url.com/{generated_id}"  # Replace with actual API

    # response = requests.get(url)

    # print(f"Trying: {generated_id} -> {response.status_code}")

    # if response.status_code == 200:
    #     print("Found valid ID:", generated_id)
    #     break

    i += 1