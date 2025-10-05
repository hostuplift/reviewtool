# ReviewTool

A comprehensive multi-platform review management system with AI-powered analysis capabilities.

## Features

- **Multi-Platform Support**: Scrape reviews from Booking.com, Expedia, TripAdvisor, and Google Maps
- **AI-Powered Analysis**: Generate intelligent summaries and violation reports using OpenAI
- **Interactive Dashboards**: Visualize review trends with interactive charts
- **Multi-Language Support**: Available in English, Spanish, French, German, Italian, and Danish
- **Establishment Management**: Manage multiple businesses with password protection
- **Data Export**: Download filtered review data as CSV files
- **Review Filtering**: Filter reviews by date range and platform

## Setup

### Prerequisites

- Python 3.7+
- Apify API token
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hostuplift/reviewtool.git
cd reviewtool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```bash
APIFY_API_TOKEN=your_apify_api_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Usage

1. **Add Establishment**: Create a new establishment with platform URLs
2. **Load Reviews**: Scrape reviews from all configured platforms
3. **Analyze Data**: View interactive charts and statistics
4. **Generate Reports**: Create AI-powered summaries and violation reports
5. **Export Data**: Download filtered reviews as CSV

## Configuration

### Platform URLs

For each establishment, you need to provide the following URLs:
- **Booking.com**: Hotel/accommodation page URL
- **Expedia**: Hotel listing URL
- **TripAdvisor**: Business page URL
- **Google Maps**: Business listing URL

### API Keys

- **Apify Token**: Get from [Apify Console](https://console.apify.com/account/integrations)
- **OpenAI Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)

## Security

- All API keys are stored securely in environment variables
- Establishment dashboards are password-protected
- Sensitive data is excluded from version control

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue on GitHub.