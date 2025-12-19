# Allter Product Stock Checker

A Python script that monitors product stock on letsallter.com and sends WhatsApp notifications when items are back in stock.

## Features

- Monitors multiple products simultaneously
- Sends WhatsApp notifications when items are in stock
- Configurable check intervals
- Easy setup with environment variables
- Runs on GitHub Actions (no need for a dedicated server)

## Prerequisites

- Python 3.8+
- A [Twilio](https://www.twilio.com/) account
- A [GitHub](https://github.com/) account

## Setup Instructions

### 1. Fork this Repository

Click the "Fork" button at the top right of this page to create your own copy of the repository.

### 2. Set Up Configuration

1. Go to your repository's **Settings** > **Environments**
2. Click **New environment** and name it `Environment`
3. In the environment settings, add the following:

   **Environment variables**:
   - `INTERESTED_ITEMS`: Semicolon-separated list of product names to monitor (e.g., `Product 1;Product 2;Product 3`)

   **Environment secrets**:
   - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
   - `YOUR_WHATSAPP_NUMBER`: Your WhatsApp number in the format `whatsapp:+1234567890`

### 3. Configure Check Frequency (Optional)

By default, the script checks stock every hour. To change this, edit the cron schedule in [.github/workflows/scraper.yml](.github/workflows/scraper.yml).

```yaml
on:
  schedule:
    - cron: '0 */1 * * *'  # Runs at minute 0 of every hour
```

## Running Locally

1. Clone your forked repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/windsurf-project.git
   cd windsurf-project
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```bash
   # On Windows
   set TWILIO_ACCOUNT_SID=your_account_sid
   set TWILIO_AUTH_TOKEN=your_auth_token
   set YOUR_WHATSAPP_NUMBER=whatsapp:+1234567890
   set INTERESTED_ITEMS="Product 1;Product 2"
   
   # On macOS/Linux
   export TWILIO_ACCOUNT_SID=your_account_sid
   export TWILIO_AUTH_TOKEN=your_auth_token
   export YOUR_WHATSAPP_NUMBER=whatsapp:+1234567890
   export INTERESTED_ITEMS="Product 1;Product 2"
   ```

5. Run the script:
   ```bash
   python letsallter_scraper.py
   ```

## How It Works

1. The script scrapes letsallter.com for the specified products
2. It checks if any of the monitored products are in stock
3. If a product is in stock, it sends a WhatsApp notification with the product details
4. The script runs on a schedule using GitHub Actions

## Customization

### Adding More Products

Add more product names to the `INTERESTED_ITEMS` environment variable, separated by semicolons.

### Changing Notification Message

Edit the `send_whatsapp_notification` method in [letsallter_scraper.py](letsallter_scraper.py) to customize the notification message.

## Troubleshooting

- **No notifications received**: Check your Twilio account to ensure you have sufficient credits and the WhatsApp sandbox is properly set up.
- **Script not running on schedule**: Make sure GitHub Actions are enabled for your repository and the cron syntax is correct.
- **Products not being detected**: The website structure might have changed. Update the CSS selectors in the `extract_product_info` method.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Twilio](https://www.twilio.com/) for the WhatsApp API
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping
- [GitHub Actions](https://github.com/features/actions) for automation