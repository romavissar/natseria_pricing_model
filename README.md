# Cabin Resort Pricing & Revenue Prediction Model

A comprehensive Python application suite for dynamic cabin pricing and revenue forecasting. This project includes two main applications: a **Cabin Booking Quote Calculator** for customers and a **Revenue Prediction Model** for business planning.

## 📋 Project Overview

This project provides:
1. **Dynamic Pricing Calculator** (`dynamic_pricing.py`) - A modern, Apple-style UI for generating instant booking quotes with cabin selection and activity add-ons
2. **Revenue Prediction Model** (`predicted_revenue.py`) - A forecasting tool that predicts expected revenue based on cabin inventory, occupancy rates, and seasonal factors

## 🏗️ Project Structure

```
Business Presentation Pricing Model/
├── dynamic_pricing.py      # Main booking quote application
├── predicted_revenue.py     # Revenue forecasting application
├── requirements.txt         # Python dependencies
├── ui.md                    # UI design specifications
├── new_pricing.md          # Feature specifications for cabin types & activities
└── README.md               # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- `customtkinter` - Modern UI framework with rounded corners and Apple-style design

2. Run the applications:
```bash
# Booking Quote Calculator
python3 dynamic_pricing.py

# Revenue Prediction Model
python3 predicted_revenue.py
```

## 💰 Dynamic Pricing Calculation

### Base Formula

The pricing model uses an **additive pricing formula**:

```
Price = α + β(Sₜ - 1)α + γ(Cₜ - α) + δ(Bₜ - 1)α + ε(Wₜ - 1)α + ζuα
```

Where:
- **α (Alpha)** = Base Price = $100.00
- **Sₜ** = Seasonality factor at time t
- **Cₜ** = Competitor price = $100.00
- **Bₜ** = Booking window factor
- **Wₜ** = External factors (weather × events) = 1.0
- **u** = Random noise term (-5% to +5%)
- **β, γ, δ, ε, ζ** = Weight parameters (fixed values)

### Weight Parameters (Fixed)

| Parameter | Symbol | Value | Description |
|-----------|--------|-------|-------------|
| Seasonality | β | 0.3 | Impact of seasonal demand |
| Competitor | γ | 0.25 | Impact of competitor pricing |
| Booking Window | δ | 0.2 | Impact of advance booking timing |
| External Factors | ε | 0.15 | Impact of weather/events |
| Noise | ζ | 0.1 | Random market variation |

### Seasonality Factor (Sₜ)

The seasonality factor combines three components:

#### 1. Monthly Base Factors
| Month | Factor | Season |
|-------|--------|--------|
| January | 0.95 | Winter |
| February | 0.75 | Winter |
| March | 0.85 | Spring |
| April | 0.95 | Spring |
| May | 1.35 | Spring |
| June | 1.85 | Summer |
| July | 1.95 | Summer (Peak) |
| August | 1.95 | Summer (Peak) |
| September | 1.25 | Fall |
| October | 0.95 | Fall |
| November | 0.85 | Fall |
| December | 0.95 | Winter |

#### 2. Weekend Premium
- **Friday, Saturday, Sunday**: 1.25x multiplier
- **Monday - Thursday**: 1.0x multiplier

#### 3. Holiday Multipliers
| Date | Multiplier | Description |
|------|------------|-------------|
| Dec 24, 25, 31 | **5.0x** | Major holidays (Christmas Eve, Christmas, New Year's Eve) |
| Jan 1 | **5.0x** | New Year's Day |
| Dec 20-30 (other days) | **3.5x** | Holiday season |
| Jan 2 | **3.5x** | Day after New Year |
| Jan 3 | **3.0x** | Post-holiday period |

**Example**: A Saturday in July with no holidays:
```
Sₜ = 1.95 (July) × 1.25 (Weekend) × 1.0 (No Holiday) = 2.44
```

**Example**: Christmas Day (Dec 25):
```
Sₜ = 0.95 (December) × 1.25 (Weekend) × 5.0 (Holiday) = 5.94
```

### Booking Window Factor (Bₜ)

Based on days until check-in:
| Days Until | Factor | Description |
|------------|--------|-------------|
| 30+ days | 0.85 | Early booking discount |
| 14-29 days | 0.90 | Standard advance booking |
| 7-13 days | 0.95 | Short-term booking |
| 3-6 days | 1.0 | Normal rate |
| 1-2 days | 1.15 | Last-minute premium |
| Same day | 1.25 | Same-day premium |

### Cabin Type Multipliers

After calculating the base dynamic price, cabin type multipliers are applied:

| Cabin Type | Multiplier | Base Price Example | Final Price Example |
|------------|------------|-------------------|---------------------|
| **Forest Cabin** | 1.0x | $150 | $150 |
| **Treehouse Cabin** | 1.8x | $150 | $270 |
| **Lakeview Cabin** | 2.8x | $150 | $420 |

### Complete Pricing Example

**Scenario**: Treehouse Cabin, Saturday July 15, booked 5 days in advance

1. Base Price: $100
2. Seasonality: 1.95 (July) × 1.25 (Weekend) = 2.44
3. Booking Window: 0.95 (5 days advance)
4. Calculation:
   - Seasonality adjustment: 0.3 × (2.44 - 1) × $100 = $43.20
   - Booking adjustment: 0.2 × (0.95 - 1) × $100 = -$1.00
   - Noise: 0.1 × 0.02 × $100 = $0.20
   - Base price: $100 + $43.20 - $1.00 + $0.20 = **$142.40**
5. Apply Treehouse multiplier: $142.40 × 1.8 = **$256.32 per night**

## 📊 Revenue Prediction Model

### Overview

The revenue prediction model forecasts expected revenue based on:
- Cabin inventory and occupancy rates
- Dynamic pricing (same as booking calculator)
- Seasonal demand patterns
- Activity participation rates

### Cabin Inventory

| Cabin Type | Count | Base Occupancy | Multiplier |
|------------|-------|----------------|------------|
| Forest Cabin | 4 | 65% | 1.0x |
| Treehouse Cabin | 3 | 55% | 1.8x |
| Lakeview Cabin | 3 | 45% | 2.8x |

**Total Capacity**: 10 cabins

### Occupancy Rate Calculation

The model calculates expected occupancy using:

```
Occupancy Rate = Base Occupancy × Seasonal Modifier × Holiday/Weekend Boost
```

#### Base Occupancy Rates
- **Forest Cabin**: 65% (most popular, affordable)
- **Treehouse Cabin**: 55% (premium, slightly lower demand)
- **Lakeview Cabin**: 45% (luxury, lower demand but higher value)

#### Seasonal Occupancy Modifiers
| Season | Modifier | Months |
|--------|----------|--------|
| Summer | 1.2x | June, July, August |
| Spring | 0.85x | March, April, May |
| Fall | 0.9x | September, October, November |
| Winter | 0.7x | December, January, February |

#### Holiday/Weekend Boosts
| Period | Boost | Dates |
|--------|-------|-------|
| Major Holidays | 1.5x | Dec 24, 25, 31; Jan 1 |
| Holiday Season | 1.3x | Dec 20-30; Jan 2-3 |
| Weekends | 1.15x | Friday, Saturday, Sunday |

**Maximum Occupancy**: Capped at 95%

### Example Occupancy Calculation

**Scenario**: Forest Cabin on a summer Saturday (July 15)

1. Base occupancy: 65%
2. Seasonal modifier: 1.2x (Summer)
3. Weekend boost: 1.15x
4. Calculation: 65% × 1.2 × 1.15 = **89.7%**
5. Expected cabins occupied: 4 × 0.897 = **3.59 cabins**

### Daily Revenue Calculation

For each day, the model calculates:

#### 1. Cabin Revenue
```
For each cabin type:
  Base Price = Calculate using dynamic pricing formula
  Cabin Price = Base Price × Cabin Multiplier
  Expected Occupied = Cabin Count × Occupancy Rate
  Cabin Revenue = Expected Occupied × Cabin Price

Total Cabin Revenue = Sum of all cabin types
```

#### 2. Activity Revenue
```
Total Guests = Total Occupied Cabins × 2 (assumes 2 guests per cabin)

For each activity (if available in season):
  Participating Guests = Total Guests × Participation Rate
  Activity Revenue = Participating Guests × Activity Price

Total Activity Revenue = Sum of all activities
```

#### Activity Participation Rates
| Activity | Price | Participation Rate | Available Seasons |
|----------|-------|-------------------|-------------------|
| Guided Hiking | $20 | 40% | All year |
| Kayaking | $40 | 35% | Spring, Summer, Fall |
| Bike Rentals | $30 | 30% | Spring, Summer, Fall |
| Zipline | $60 | 25% | Spring, Summer, Fall |
| Couch Tubing | $45 | 20% | Summer only |
| Hunting Tour | $150 | 15% | Fall, Winter |
| Bungee Jumping | $100 | 10% | Summer only |

### Complete Revenue Example

**Scenario**: Summer Saturday (July 15)

**Cabin Revenue:**
- Forest: 3.59 cabins × $142.40 = $511
- Treehouse: 2.28 cabins × $256.32 = $584
- Lakeview: 1.86 cabins × $398.72 = $742
- **Total Cabin Revenue: $1,837**

**Activity Revenue:**
- Total guests: (3.59 + 2.28 + 1.86) × 2 = 15.46 guests
- Hiking: 15.46 × 0.4 × $20 = $124
- Kayaking: 15.46 × 0.35 × $40 = $216
- Bike: 15.46 × 0.3 × $30 = $139
- Zipline: 15.46 × 0.25 × $60 = $232
- Couch Tubing: 15.46 × 0.2 × $45 = $139
- Bungee: 15.46 × 0.1 × $100 = $155
- **Total Activity Revenue: $1,005**

**Daily Total Revenue: $2,842**

## 🎯 Key Assumptions

### Pricing Assumptions
1. **Base Price**: $100 per night (Forest Cabin baseline)
2. **Competitor Price**: $100 (assumed market rate)
3. **External Factors**: Neutral (1.0) - weather and events don't significantly impact pricing in this model
4. **Noise Term**: Random variation between -5% and +5% to simulate market fluctuations

### Occupancy Assumptions
1. **Base Occupancy Rates**: 
   - Higher occupancy for affordable cabins (Forest)
   - Lower occupancy for luxury cabins (Lakeview) but higher revenue per cabin
2. **Guest Capacity**: 2 guests per cabin (standard assumption)
3. **Maximum Occupancy**: 95% cap to account for maintenance and buffer

### Activity Assumptions
1. **Participation Rates**: Based on typical resort activity engagement
   - Higher for accessible activities (hiking, kayaking)
   - Lower for specialized activities (bungee jumping, hunting)
2. **Seasonal Availability**: Activities only available in appropriate seasons
3. **Per-Person Pricing**: All activities priced per guest

### Revenue Model Assumptions
1. **Expected Value Approach**: Uses fractional cabins (e.g., 3.59 cabins) rather than discrete bookings for smoother forecasts
2. **No Booking Conflicts**: Assumes all cabins can be booked independently
3. **Activity Participation**: Assumes guests participate in multiple activities per day
4. **Consistent Demand**: Model doesn't account for external shocks or market changes

## 🖥️ Application Features

### Booking Quote Calculator (`dynamic_pricing.py`)

**Features:**
- Modern Apple-style UI with rounded corners
- Cabin type selection (Forest, Treehouse, Lakeview)
- Date range selection (check-in and check-out)
- Number of cabins selector
- Seasonal activity booking with guest counts
- Real-time quote generation with detailed breakdown
- Nightly price breakdown showing holiday/weekend indicators

**Usage:**
1. Select cabin type
2. Enter check-in and check-out dates
3. Select number of cabins
4. Choose activities (automatically filtered by season)
5. Click "Get Quote" to see pricing breakdown

### Revenue Prediction Model (`predicted_revenue.py`)

**Features:**
- Cabin inventory overview
- Custom date range selection
- Quick select buttons (1 month, 3 months, 1 year)
- Revenue forecast dashboard
- Monthly breakdown for longer periods
- Cabin vs. activity revenue split
- Average occupancy rate calculation

**Usage:**
1. Select forecast period (or use quick select)
2. Click "Generate Forecast"
3. View total revenue, daily averages, and occupancy metrics
4. Review monthly breakdowns for longer periods

## 📈 Model Limitations

1. **Deterministic Pricing**: Uses expected values rather than simulating individual bookings
2. **No Competition Effects**: Doesn't model competitor responses to pricing
3. **Fixed Participation Rates**: Activity participation doesn't vary by cabin type or guest demographics
4. **No Capacity Constraints**: Assumes activities can accommodate all participants
5. **Simplified Seasonality**: Monthly factors are fixed and don't account for year-over-year trends
6. **No Cancellation Model**: Doesn't account for booking cancellations or no-shows

## 🔧 Technical Details

### Dependencies
- **customtkinter**: Modern UI framework providing Apple-style widgets
- **datetime**: Date handling and calculations
- **random**: Noise generation for pricing variation

### Code Structure
- **Modular Design**: Separate functions for pricing, occupancy, and revenue calculations
- **Reusable Components**: Shared pricing logic between booking and revenue models
- **Clean Separation**: UI logic separated from business logic

## 📝 Future Enhancements

Potential improvements:
- Historical booking data integration
- Machine learning for demand forecasting
- Real-time competitor price monitoring
- Guest demographic-based activity participation
- Cancellation and no-show modeling
- Multi-year trend analysis
- Export functionality (CSV, PDF reports)

## 📄 License

This project is for educational and business presentation purposes.

## 👤 Author

Created for business presentation and pricing strategy analysis.
