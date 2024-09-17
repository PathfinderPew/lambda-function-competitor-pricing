import requests
from bs4 import BeautifulSoup
import json

def get_competitor_price(url):
    try:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the price using the correct selector
        price_tag = soup.find('p', class_='price_color')  # Update to the correct tag and class

        if price_tag:
            return price_tag.text
        else:
            raise ValueError('Price tag not found on the page')
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request error: {e}")
    except Exception as e:
        raise ValueError(f"General error: {e}")

def lambda_handler(event, context):
    # URL of a competitor's pricing page
    url = 'http://books.toscrape.com/'

    # Try to get the price from the webpage
    try:
        price = get_competitor_price(url)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Success',
                'price': price
            })
        }
    except ValueError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to retrieve the price',
                'error': str(e)
            })
        }

if __name__ == "__main__":
    # Test the lambda_handler function
    print("Testing lambda_handler...")
    result = lambda_handler(None, None)
    body = json.loads(result['body'])
    print(f"Message: {body['message']}")
    print(f"Price: {body['price']}")
