import httpx
import asyncio
import os

# define the zenrow API key
zenrow_apikey = "your_zenrow_apikey_here"

async def fetch_data(request_count, id_value, print_id_value):
    for i in range(request_count):
        # zenrow setup
        proxies = {
            "http://": f"http://{zenrow_apikey}@proxy.zenrows.com:8001",
            "https://": f"http://{zenrow_apikey}@proxy.zenrows.com:8001",
        }

        # headers setup
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'it',
            'Apollographql-Client-Version': 'v2.99.1',
            'Authorization': '',
            'Client-Uid': '1337',
            'Content-Type': 'application/json',
            'Origin': 'https://www.printables.com',
            'Referer': 'https://www.printables.com/',
            'Sec-Ch-Ua': '""',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '""',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }

        # data
        data = {
            "operationName": "GetDownloadLink",
            "variables": {
                "id": id_value, # input from the user
                "fileType": "pack",
                "printId": print_id_value, # input from the user
                "source": "model_detail"
            },
            "query": """mutation GetDownloadLink($id: ID!, $printId: ID!, $fileType: DownloadFileTypeEnum!, $source: DownloadSourceEnum!) {
          getDownloadLink(
            id: $id
            printId: $printId
            fileType: $fileType
            source: $source
          ) {
            ok
            errors {
              field
              messages
              __typename
            }
            output {
              link
              count
              ttl
              __typename
            }
            __typename
          }
        }"""
        }

        # making the POST request using httpx
        async with httpx.AsyncClient(proxies=proxies, verify=False) as client:  # verify=False for SSL certificate issues
            response = await client.post(
                'https://api.printables.com/graphql/',
                headers=headers,
                json=data,
            )

        # saving the binary response content to a file
        filename = f'binary_{i}.gz'
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Request {i+1} successful.")

        # deleting the saved file
        os.remove(filename)
        #print(f"File {filename} deleted")

if __name__ == "__main__":
    request_count = int(input("Enter the number of requests to send: "))
    id_value = input("Enter the 'id' of the model: ")
    print_id_value = input("Enter the 'printId' of the model: ")
    asyncio.run(fetch_data(request_count, id_value, print_id_value))
