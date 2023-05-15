import requests
import json
import os

# Grab store data from config file named photograb_config.json
with open("photograb_config.json") as json_data:
    data = json.load(json_data)
    
# Grab the specific item to get pictures for
sku = input("Please enter the SKU of the item you want images for: ")
url = "https://{}.vendhq.com/api/2.0/search?type=products&sku={}".format(data['store_domain'], sku)

headers = {
    "accept": "application/json",
    "authorization": "Bearer {}".format(data['bearer_token'])
}
print("Getting item from LightSpeed...")
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Couldn't retrieve item. HTTP error code: {}".format(response.status_code))
    input("Press enter to close the screen")
    exit()
inv_item = json.loads(response.text)
print("Retrieved {} from inventory...".format(inv_item['data'][0]['name']))

# If the path doesn't exist already, make it
current_path = os.getcwd()
picture_path = os.path.join(current_path, sku)
if not os.path.exists(picture_path):
    os.makedirs(picture_path)
    print("Created new path for SKU {} ...".format(sku))
else:
    print("Path already exists for SKU {} ...".format(sku))

for url in inv_item['data'][0]["images"]:
    img_path = os.path.join(picture_path,url["id"] + ".jpg")
    print("Generating image: {} ...".format(img_path))
    file = requests.get(url["sizes"]["original"])
    if file.status_code == 200:
        with open(img_path, 'wb') as file_handle:
            file_handle.write(file.content)
    else:
        print("Unable to download image. HTTP error code: {}".format(file.status_code))
        
print("Finished! Check the directory {} for your images".format(picture_path))
input("Press enter to close the screen")
exit()