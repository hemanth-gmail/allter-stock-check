import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import os
from twilio.rest import Client

class LetsAllterScraper:
    def __init__(self):
        self.base_url = "https://letsallter.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.data_dir = 'scraped_data'
        self.interested_items = {'Organic Bamboo Diapers- Large Size (8-12 kgs)', 'Organic Bamboo Diapers- Medium Size (5-8 kgs)'}
        self.create_data_directory()
        
        # Load credentials from environment variables
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp_from = 'whatsapp:+14155238886'  # Twilio's WhatsApp sandbox number
        self.your_whatsapp_number = os.getenv('YOUR_WHATSAPP_NUMBER')
        
        # Validate required environment variables
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.your_whatsapp_number]):
            raise ValueError("Missing required environment variables. Please check your configuration.")

    def create_data_directory(self):
        """Create directory to store scraped data if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_soup(self, url):
        """Get BeautifulSoup object from URL using html.parser"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_product_info(self, product):
        """Extract product information from product element"""
        try:
            # Try different possible selectors for title
            title_elem = (product.find('h3', class_='card__heading') or 
                         product.find('a', class_='card-information__text')
                         )
            
            # Find price element
            price_elem = (product.find('span', class_='price-item--regular') or 
                         product.find('span', class_='price-item price-item--sale'))
            
            # Find product link
            link_elem = (product.find('a', class_='full-unstyled-link') or 
                        product.find('a', class_='card-wrapper__link'))
            
            # Check if product is in stock
            sold_out_elem = product.find('span', string='Sold out')
            in_stock = 'No' if sold_out_elem else 'Yes'
            
            # Extract text content safely
            title = title_elem.get_text(strip=True) if title_elem else 'N/A'
            price = price_elem.get_text(strip=True) if price_elem else 'N/A'
            product_url = (self.base_url + link_elem['href']) if link_elem and 'href' in link_elem.attrs else 'N/A'
            
            return {
                'title': title,
                'price': price,
                'in_stock': in_stock,
                'product_url': product_url,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"Error extracting product info: {e}")
            return None

    def get_all_products(self):
        """Get all products from the website"""
        products = []
        page = 1
        
        while True:
            url = f"{self.base_url}/collections/all?page={page}"
            print(f"Scraping page {page}...")
            
            soup = self.get_soup(url)
            if not soup:
                break
                
            # Find product grid
            product_grid = soup.find('div', class_='collection')
            if not product_grid:
                break
                
            product_cards = product_grid.find_all('div', class_='card-wrapper')
            if not product_cards:
                break
                
            for card in product_cards:
                product_info = self.extract_product_info(card)
                if product_info:
                    products.append(product_info)
            
            # Check for next page
            next_button = soup.find('a', string='→')
            if not next_button or 'disabled' in next_button.get('class', []):
                break
                
            page += 1
            time.sleep(2)  # Be nice to the server
            
        return products

    def save_to_csv(self, data):
        """Save scraped data to CSV file"""
        if not data:
            print("No data to save.")
            return
            
        filename = f"{self.data_dir}/letsallter_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['title', 'price', 'in_stock', 'product_url', 'scraped_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for product in data:
                    writer.writerow(product)
                    
            print(f"Data saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return None

    def send_whatsapp_notification(self, product):
        """Send WhatsApp notification using Twilio"""
        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            message = (
                f"🚀 *Product In Stock!* 🚀\n\n"
                f"*{product['title']}*\n"
                f"💰 Price: {product['price']}\n"
                f"🛒 Status: {'In Stock' if product['in_stock'] == 'Yes' else 'Out of Stock'}\n"
                f"🔗 {product['product_url']}"
            )
            
            client.messages.create(
                body=message,
                from_=self.twilio_whatsapp_from,
                to=self.your_whatsapp_number
            )
            print(f"WhatsApp notification sent for {product['title']}")
            return True
        except Exception as e:
            print(f"Error sending WhatsApp notification: {e}")
            return False

    def run(self):
        """Main method to run the scraper"""
        print("Starting LetsAllter scraper...")
        products = self.get_all_products()
        interested_products = [product for product in products if product['title'] in self.interested_items]
        
        if not interested_products:
            print("No interested products found.")
            return
            
        print(f"Found {len(interested_products)} interested products.")
            
        # Check stock and send notifications
        for product in interested_products:
            if product.get('in_stock') == 'Yes':
                print(f"{product['title']} is in stock! Sending notification...")
                self.send_whatsapp_notification(product)
            else:
                print(f"{product['title']} is out of stock.")


if __name__ == "__main__":
    scraper = LetsAllterScraper()
    scraper.run()
