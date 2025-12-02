# Hotel Room Dynamic Pricing Calculator

A Python application that calculates dynamic hotel room pricing based on multiple factors.

## Formula

The dynamic pricing formula includes:

- **α** - Base Price
- **Sₜ** - Seasonality at time t
- **Cₜ** - Competitor Pricing
- **Bₜ** - Booking Window
- **Wₜ** - Weather/Events/External Factors
- **u** - Noise/Error Term
- **β, γ, δ, ε, ζ** - Weight parameters

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python dynamic_pricing.py
```

## Features

- Interactive date picker for selecting check-in date
- Real-time calculation of days until check-in
- Adjustable weight parameters for each factor
- Visual sliders for easy parameter adjustment
- Detailed calculation results display

## How It Works

1. Select a check-in date using the date picker
2. Adjust base price and competitor price
3. Set weight parameters (β, γ, δ, ε, ζ) using sliders
4. Adjust external factors (weather and events)
5. Click "Calculate Dynamic Price" to see results

The application calculates the dynamic price using an additive model that considers all factors and their respective weights.

