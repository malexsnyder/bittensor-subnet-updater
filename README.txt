# Bittensor Subnet Updater

This project automatically pulls live subnet data directly from the Bittensor blockchain using the Subtensor SDK, without relying on third-party sources like TaoMarketCap.

## Features

- **Direct Blockchain Access**: Uses Bittensor Subtensor SDK to fetch data directly from the Finney network
- **No Credentials Required**: Works with public blockchain data only - no private keys or authentication needed
- **Modular Design**: Easy to extend with additional features like sentiment analysis or trending alerts
- **Markdown Profiles**: Generates structured profiles for each subnet with placeholders for AI agent enhancement

## Installation

1. Install the required dependencies:
```bash
pip install bittensor requests
```

2. Run the scripts to fetch and generate subnet data:
```bash
python scripts/fetch_subnets_bt.py
python scripts/build_profiles_local.py
```

## Scripts

### `scripts/fetch_subnets_bt.py`
Fetches live subnet data from the Bittensor blockchain and saves it to `data/subnets.json`.

**Features:**
- Connects to Bittensor Finney network
- Fetches all registered subnets (currently 129 subnets)
- Collects basic subnet information including:
  - Subnet ID and existence status
  - Active/inactive status
  - Owner hotkey
  - Current price
  - Hyperparameters (when available)
- Handles errors gracefully and continues processing
- Uses only public blockchain data

### `scripts/build_profiles_local.py`
Generates Markdown profiles for each subnet based on the data from `fetch_subnets_bt.py`.

**Features:**
- Reads subnet data from `data/subnets.json`
- Creates individual Markdown files for each subnet in `data/profiles/`
- Includes placeholders for AI agent enhancement:
  - Primary Function
  - Problem It Solves
  - Target Audience
  - Growth and conviction metrics
  - Trending alerts
- Shows current blockchain metrics and status
- Displays error information when data fetching fails

## Data Structure

### `data/subnets.json`
Contains an array of subnet objects with the following structure:
```json
{
  "subnets": [
    {
      "id": 1,
      "name": "Subnet 1",
      "exists": true,
      "is_active": true,
      "owner_hotkey": "5HCFWvRqzSHWRPecN7q8J6c7aKQnrCZTMHstPv39xL1wgDHh",
      "price": 0.009940307,
      "hyperparameters": null,
      "last_update": 1760822731
    }
  ],
  "total_count": 129,
  "timestamp": 1760822731,
  "network": "finney",
  "source": "bittensor_subtensor_sdk_public"
}
```

### `data/profiles/`
Contains individual Markdown files for each subnet (e.g., `1_subnet-1.md`) with:
- Current blockchain metrics
- Status information
- Placeholders for AI agent enhancement
- Error reporting when data is unavailable

## Usage

1. **Fetch Latest Data**:
   ```bash
   python scripts/fetch_subnets_bt.py
   ```

2. **Generate Profiles**:
   ```bash
   python scripts/build_profiles_local.py
   ```

3. **View Results**:
   - Check `data/subnets.json` for raw subnet data
   - Browse `data/profiles/` for individual subnet profiles

## Extending the System

The modular design makes it easy to add new features:

- **Sentiment Analysis**: Add sentiment scoring based on social media or news
- **Trending Alerts**: Implement alerts for significant price or activity changes
- **Subnet Alpha Integration**: Enhance profiles with descriptions from Subnet Alpha
- **Historical Data**: Track subnet metrics over time
- **Custom Metrics**: Add domain-specific analysis for different subnet types

## Technical Notes

- Uses Bittensor SDK version 9.12.0
- Connects to Finney network (mainnet)
- Handles JSON serialization issues with Bittensor objects
- Graceful error handling for network issues
- No authentication or credentials required

## Troubleshooting

- **Connection Issues**: Ensure stable internet connection
- **SDK Errors**: Update bittensor package: `pip install --upgrade bittensor`
- **Data Issues**: Some historical data may require archive nodes (not implemented in this version)
- **Permission Errors**: Ensure write permissions for `data/` directory