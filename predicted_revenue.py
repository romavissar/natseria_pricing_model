"""
Predicted Revenue Model for Cabin Resort

This model simulates expected revenue based on:
- Cabin inventory: 4 Forest Cabins, 3 Treehouse Cabins, 3 Lakeview Cabins
- Dynamic pricing with seasonality, holidays, and booking windows
- Historical occupancy rate assumptions
- Activity revenue projections

Run this file to generate revenue forecasts for different time periods.
"""

import customtkinter as ctk
from datetime import datetime, timedelta
import random
import calendar

# Configuration
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Cabin Inventory
CABIN_INVENTORY = {
    "forest": {
        "name": "Forest Cabin",
        "count": 4,
        "multiplier": 1.0,
        "icon": "🌲",
        "base_occupancy": 0.65  # 65% average occupancy
    },
    "treehouse": {
        "name": "Treehouse Cabin",
        "count": 3,
        "multiplier": 1.8,
        "icon": "🏡",
        "base_occupancy": 0.55  # 55% average occupancy (premium = slightly lower)
    },
    "lakeview": {
        "name": "Lakeview Cabin",
        "count": 3,
        "multiplier": 2.8,
        "icon": "🏖️",
        "base_occupancy": 0.45  # 45% average occupancy (luxury = lower but higher value)
    }
}

# Seasonal Occupancy Modifiers
SEASONAL_OCCUPANCY = {
    "winter": 0.7,   # Dec, Jan, Feb - lower except holidays
    "spring": 0.85,  # Mar, Apr, May
    "summer": 1.2,   # Jun, Jul, Aug - peak season
    "fall": 0.9      # Sep, Oct, Nov
}

# Holiday Occupancy Boost
HOLIDAY_OCCUPANCY_BOOST = {
    "major": 1.5,    # Dec 24, 25, 31, Jan 1
    "season": 1.3,   # Dec 20-30, Jan 2-3
    "weekend": 1.15  # Fri, Sat, Sun
}

# Activities Configuration (same as main app)
ACTIVITIES = {
    "hiking": {"name": "Guided Hiking", "price": 20, "seasons": ["spring", "summer", "fall", "winter"], "participation_rate": 0.4},
    "kayaking": {"name": "Kayaking", "price": 40, "seasons": ["spring", "summer", "fall"], "participation_rate": 0.35},
    "bike": {"name": "Bike Rentals", "price": 30, "seasons": ["spring", "summer", "fall"], "participation_rate": 0.3},
    "hunting": {"name": "Hunting Tour", "price": 150, "seasons": ["fall", "winter"], "participation_rate": 0.15},
    "bungee": {"name": "Bungee Jumping", "price": 100, "seasons": ["summer"], "participation_rate": 0.1},
    "zipline": {"name": "Zipline", "price": 60, "seasons": ["spring", "summer", "fall"], "participation_rate": 0.25},
    "tubing": {"name": "Couch Tubing / Banana Boat", "price": 45, "seasons": ["summer"], "participation_rate": 0.2}
}

# Pricing Configuration
BASE_PRICE = 100.0
WEIGHTS = {
    'seasonality': 0.3,
    'competitor': 0.25,
    'booking_window': 0.2,
    'external': 0.15,
    'noise': 0.1
}

def get_season(date):
    """Determine season from date"""
    month = date.month
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "fall"
    else:
        return "winter"

def calculate_seasonality(date):
    """Calculate price seasonality factor"""
    month = date.month
    day_of_week = date.weekday()
    
    monthly_factors = {
        1: 0.95, 2: 0.75, 3: 0.85, 4: 0.95, 5: 1.35, 6: 1.85,
        7: 1.95, 8: 1.95, 9: 1.25, 10: 0.95, 11: 0.85, 12: 0.95
    }
    
    weekend_factor = 1.25 if day_of_week >= 4 else 1.0
    
    # Holiday logic
    holiday_factor = 1.0
    if month == 12:
        if date.day in [24, 25, 31]:
            holiday_factor = 5.0
        elif 20 <= date.day <= 30:
            holiday_factor = 3.5
    elif month == 1:
        if date.day == 1:
            holiday_factor = 5.0
        elif date.day == 2:
            holiday_factor = 3.5
        elif date.day == 3:
            holiday_factor = 3.0
            
    return monthly_factors[month] * weekend_factor * holiday_factor

def calculate_base_price(date):
    """Calculate base price for a given date"""
    alpha = BASE_PRICE
    s_t = calculate_seasonality(date)
    u = random.uniform(-0.02, 0.02)  # Smaller noise for predictions
    
    beta = WEIGHTS['seasonality']
    zeta = WEIGHTS['noise']
    
    seasonality_adj = beta * (s_t - 1) * alpha
    noise_adj = zeta * u * alpha
    
    final_price = alpha + seasonality_adj + noise_adj
    return max(final_price, alpha * 0.5)

def calculate_occupancy_rate(date, cabin_type):
    """Calculate expected occupancy rate for a given date and cabin type"""
    base_rate = CABIN_INVENTORY[cabin_type]["base_occupancy"]
    season = get_season(date)
    seasonal_mod = SEASONAL_OCCUPANCY[season]
    
    # Holiday boost
    month, day = date.month, date.day
    day_of_week = date.weekday()
    
    holiday_mod = 1.0
    if month == 12 and day in [24, 25, 31]:
        holiday_mod = HOLIDAY_OCCUPANCY_BOOST["major"]
    elif month == 1 and day == 1:
        holiday_mod = HOLIDAY_OCCUPANCY_BOOST["major"]
    elif (month == 12 and 20 <= day <= 30) or (month == 1 and day in [2, 3]):
        holiday_mod = HOLIDAY_OCCUPANCY_BOOST["season"]
    elif day_of_week >= 4:  # Weekend
        holiday_mod = HOLIDAY_OCCUPANCY_BOOST["weekend"]
    
    # Calculate final rate (capped at 95%)
    final_rate = min(base_rate * seasonal_mod * holiday_mod, 0.95)
    return final_rate

def calculate_activity_revenue(date, occupied_cabins):
    """Calculate expected activity revenue for a given date"""
    season = get_season(date)
    total_guests = occupied_cabins * 2  # Assume 2 guests per cabin
    
    activity_revenue = 0
    for key, activity in ACTIVITIES.items():
        if season in activity["seasons"]:
            participating_guests = total_guests * activity["participation_rate"]
            activity_revenue += participating_guests * activity["price"]
    
    return activity_revenue

def predict_daily_revenue(date):
    """Predict total revenue for a single day"""
    daily_data = {
        "date": date,
        "cabin_revenue": 0,
        "activity_revenue": 0,
        "cabins_occupied": {},
        "total_cabins_occupied": 0
    }
    
    total_occupied = 0
    
    for cabin_type, info in CABIN_INVENTORY.items():
        base_price = calculate_base_price(date)
        cabin_price = base_price * info["multiplier"]
        occupancy_rate = calculate_occupancy_rate(date, cabin_type)
        
        # Expected cabins occupied (can be fractional for averaging)
        expected_occupied = info["count"] * occupancy_rate
        cabin_revenue = expected_occupied * cabin_price
        
        daily_data["cabin_revenue"] += cabin_revenue
        daily_data["cabins_occupied"][cabin_type] = expected_occupied
        total_occupied += expected_occupied
    
    daily_data["total_cabins_occupied"] = total_occupied
    daily_data["activity_revenue"] = calculate_activity_revenue(date, total_occupied)
    daily_data["total_revenue"] = daily_data["cabin_revenue"] + daily_data["activity_revenue"]
    
    return daily_data

def predict_period_revenue(start_date, end_date):
    """Predict revenue for a date range"""
    current = start_date
    period_data = {
        "start_date": start_date,
        "end_date": end_date,
        "days": [],
        "total_cabin_revenue": 0,
        "total_activity_revenue": 0,
        "total_revenue": 0,
        "avg_daily_revenue": 0,
        "avg_occupancy": 0,
        "cabin_breakdown": {k: {"revenue": 0, "nights_sold": 0} for k in CABIN_INVENTORY.keys()}
    }
    
    total_possible_nights = 0
    total_nights_sold = 0
    
    while current < end_date:
        daily = predict_daily_revenue(current)
        period_data["days"].append(daily)
        period_data["total_cabin_revenue"] += daily["cabin_revenue"]
        period_data["total_activity_revenue"] += daily["activity_revenue"]
        period_data["total_revenue"] += daily["total_revenue"]
        
        for cabin_type, occupied in daily["cabins_occupied"].items():
            period_data["cabin_breakdown"][cabin_type]["nights_sold"] += occupied
            base_price = calculate_base_price(current)
            period_data["cabin_breakdown"][cabin_type]["revenue"] += occupied * base_price * CABIN_INVENTORY[cabin_type]["multiplier"]
            total_possible_nights += CABIN_INVENTORY[cabin_type]["count"]
            total_nights_sold += occupied
        
        current += timedelta(days=1)
    
    num_days = len(period_data["days"])
    if num_days > 0:
        period_data["avg_daily_revenue"] = period_data["total_revenue"] / num_days
    if total_possible_nights > 0:
        period_data["avg_occupancy"] = total_nights_sold / total_possible_nights
    
    return period_data


class RevenuePredictionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Revenue Prediction Model")
        self.geometry("1200x900")
        self.resizable(True, True)
        
        self.create_layout()
    
    def create_layout(self):
        # Main scrollable container
        main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_scroll.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header
        header = ctk.CTkFrame(main_scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            header,
            text="📊 Revenue Prediction Model",
            font=("Helvetica Neue", 36, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Forecast revenue based on cabin inventory, pricing, and occupancy projections.",
            font=("Helvetica Neue", 16),
            text_color="#86868b"
        ).pack(anchor="w", pady=(5, 0))
        
        # Inventory Summary
        self.create_inventory_section(main_scroll)
        
        # Prediction Controls
        self.create_controls_section(main_scroll)
        
        # Results Section
        self.results_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        self.create_results_placeholder()
    
    def create_inventory_section(self, parent):
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            section,
            text="Cabin Inventory",
            font=("Helvetica Neue", 20, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w", padx=25, pady=(25, 15))
        
        inventory_frame = ctk.CTkFrame(section, fg_color="transparent")
        inventory_frame.pack(fill="x", padx=25, pady=(0, 25))
        inventory_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, (key, cabin) in enumerate(CABIN_INVENTORY.items()):
            card = ctk.CTkFrame(inventory_frame, fg_color="#F5F5F7", corner_radius=12)
            card.grid(row=0, column=i, sticky="nsew", padx=8, pady=5)
            
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(inner, text=cabin["icon"], font=("Helvetica Neue", 32)).pack()
            ctk.CTkLabel(inner, text=cabin["name"], font=("Helvetica Neue", 16, "bold"), text_color="#1D1D1F").pack(pady=(10, 5))
            ctk.CTkLabel(inner, text=f"{cabin['count']} Units", font=("Helvetica Neue", 14), text_color="#007AFF").pack()
            ctk.CTkLabel(inner, text=f"{cabin['multiplier']}x Rate", font=("Helvetica Neue", 12), text_color="#86868b").pack()
            ctk.CTkLabel(inner, text=f"~{int(cabin['base_occupancy']*100)}% Base Occupancy", font=("Helvetica Neue", 11), text_color="#86868b").pack(pady=(5, 0))
    
    def create_controls_section(self, parent):
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            section,
            text="Forecast Period",
            font=("Helvetica Neue", 20, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w", padx=25, pady=(25, 15))
        
        controls = ctk.CTkFrame(section, fg_color="transparent")
        controls.pack(fill="x", padx=25, pady=(0, 25))
        controls.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Start Date
        start_frame = ctk.CTkFrame(controls, fg_color="transparent")
        start_frame.grid(row=0, column=0, sticky="ew", padx=10)
        
        ctk.CTkLabel(start_frame, text="Start Date", font=("Helvetica Neue", 12), text_color="#86868b").pack(anchor="w")
        self.start_entry = ctk.CTkEntry(start_frame, placeholder_text="YYYY-MM-DD", height=40, font=("Helvetica Neue", 14))
        self.start_entry.pack(fill="x", pady=(5, 0))
        self.start_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # End Date
        end_frame = ctk.CTkFrame(controls, fg_color="transparent")
        end_frame.grid(row=0, column=1, sticky="ew", padx=10)
        
        ctk.CTkLabel(end_frame, text="End Date", font=("Helvetica Neue", 12), text_color="#86868b").pack(anchor="w")
        self.end_entry = ctk.CTkEntry(end_frame, placeholder_text="YYYY-MM-DD", height=40, font=("Helvetica Neue", 14))
        self.end_entry.pack(fill="x", pady=(5, 0))
        # Default to 1 year from now
        one_year = datetime.now() + timedelta(days=365)
        self.end_entry.insert(0, one_year.strftime("%Y-%m-%d"))
        
        # Quick Select Buttons
        quick_frame = ctk.CTkFrame(controls, fg_color="transparent")
        quick_frame.grid(row=0, column=2, sticky="ew", padx=10)
        
        ctk.CTkLabel(quick_frame, text="Quick Select", font=("Helvetica Neue", 12), text_color="#86868b").pack(anchor="w")
        
        btn_row = ctk.CTkFrame(quick_frame, fg_color="transparent")
        btn_row.pack(fill="x", pady=(5, 0))
        
        ctk.CTkButton(btn_row, text="1 Month", width=70, height=35, fg_color="#F5F5F7", text_color="#007AFF", hover_color="#E5E5E5",
                     command=lambda: self.set_period(30)).pack(side="left", padx=2)
        ctk.CTkButton(btn_row, text="3 Months", width=70, height=35, fg_color="#F5F5F7", text_color="#007AFF", hover_color="#E5E5E5",
                     command=lambda: self.set_period(90)).pack(side="left", padx=2)
        ctk.CTkButton(btn_row, text="1 Year", width=70, height=35, fg_color="#F5F5F7", text_color="#007AFF", hover_color="#E5E5E5",
                     command=lambda: self.set_period(365)).pack(side="left", padx=2)
        
        # Calculate Button
        calc_frame = ctk.CTkFrame(controls, fg_color="transparent")
        calc_frame.grid(row=0, column=3, sticky="ew", padx=10)
        
        ctk.CTkLabel(calc_frame, text=" ", font=("Helvetica Neue", 12)).pack(anchor="w")
        ctk.CTkButton(
            calc_frame,
            text="Generate Forecast",
            height=40,
            font=("Helvetica Neue", 14, "bold"),
            fg_color="#007AFF",
            hover_color="#0062CC",
            command=self.generate_forecast
        ).pack(fill="x", pady=(5, 0))
    
    def set_period(self, days):
        start = datetime.now()
        end = start + timedelta(days=days)
        
        self.start_entry.delete(0, "end")
        self.start_entry.insert(0, start.strftime("%Y-%m-%d"))
        
        self.end_entry.delete(0, "end")
        self.end_entry.insert(0, end.strftime("%Y-%m-%d"))
    
    def create_results_placeholder(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        placeholder = ctk.CTkFrame(self.results_frame, fg_color="#FFFFFF", corner_radius=15)
        placeholder.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            placeholder,
            text="📈",
            font=("Helvetica Neue", 64)
        ).pack(pady=(80, 10))
        
        ctk.CTkLabel(
            placeholder,
            text="Revenue Forecast",
            font=("Helvetica Neue", 24, "bold"),
            text_color="#1D1D1F"
        ).pack()
        
        ctk.CTkLabel(
            placeholder,
            text="Select a date range and click 'Generate Forecast'\nto see predicted revenue.",
            font=("Helvetica Neue", 14),
            text_color="#86868b",
            justify="center"
        ).pack(pady=(10, 80))
    
    def generate_forecast(self):
        try:
            start_str = self.start_entry.get().strip()
            end_str = self.end_entry.get().strip()
            
            start_date = datetime.strptime(start_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_str, "%Y-%m-%d")
            
            if end_date <= start_date:
                ctk.CTkInputDialog(text="End date must be after start date.", title="Error")
                return
            
            # Generate prediction
            prediction = predict_period_revenue(start_date, end_date)
            
            # Display results
            self.display_results(prediction)
            
        except ValueError:
            ctk.CTkInputDialog(text="Please use YYYY-MM-DD format.", title="Format Error")
        except Exception as e:
            print(f"Error: {e}")
    
    def display_results(self, data):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Summary Cards Row
        summary_row = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        summary_row.pack(fill="x", pady=(0, 20))
        summary_row.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Total Revenue Card
        self.create_metric_card(summary_row, 0, "Total Revenue", f"${data['total_revenue']:,.0f}", "#007AFF", "💰")
        
        # Avg Daily Revenue
        self.create_metric_card(summary_row, 1, "Avg Daily Revenue", f"${data['avg_daily_revenue']:,.0f}", "#34C759", "📊")
        
        # Avg Occupancy
        self.create_metric_card(summary_row, 2, "Avg Occupancy", f"{data['avg_occupancy']*100:.1f}%", "#FF9500", "🛏️")
        
        # Days Forecast
        num_days = len(data['days'])
        self.create_metric_card(summary_row, 3, "Days Forecast", f"{num_days}", "#5856D6", "📅")
        
        # Revenue Breakdown
        breakdown_section = ctk.CTkFrame(self.results_frame, fg_color="#FFFFFF", corner_radius=15)
        breakdown_section.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            breakdown_section,
            text="Revenue Breakdown",
            font=("Helvetica Neue", 20, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w", padx=25, pady=(25, 15))
        
        breakdown_content = ctk.CTkFrame(breakdown_section, fg_color="transparent")
        breakdown_content.pack(fill="x", padx=25, pady=(0, 25))
        breakdown_content.grid_columnconfigure((0, 1), weight=1)
        
        # Cabin Revenue
        cabin_frame = ctk.CTkFrame(breakdown_content, fg_color="#F5F5F7", corner_radius=12)
        cabin_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
        
        ctk.CTkLabel(cabin_frame, text="🏠 Accommodation Revenue", font=("Helvetica Neue", 16, "bold"), text_color="#1D1D1F").pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(cabin_frame, text=f"${data['total_cabin_revenue']:,.0f}", font=("Helvetica Neue", 28, "bold"), text_color="#007AFF").pack(anchor="w", padx=20)
        
        for cabin_type, breakdown in data['cabin_breakdown'].items():
            info = CABIN_INVENTORY[cabin_type]
            row = ctk.CTkFrame(cabin_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(row, text=f"{info['icon']} {info['name']}", font=("Helvetica Neue", 13), text_color="#1D1D1F").pack(side="left")
            ctk.CTkLabel(row, text=f"${breakdown['revenue']:,.0f} ({breakdown['nights_sold']:.0f} nights)", font=("Helvetica Neue", 13), text_color="#86868b").pack(side="right")
        
        ctk.CTkLabel(cabin_frame, text="").pack(pady=5)  # Spacer
        
        # Activity Revenue
        activity_frame = ctk.CTkFrame(breakdown_content, fg_color="#F5F5F7", corner_radius=12)
        activity_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)
        
        ctk.CTkLabel(activity_frame, text="🎯 Activity Revenue", font=("Helvetica Neue", 16, "bold"), text_color="#1D1D1F").pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(activity_frame, text=f"${data['total_activity_revenue']:,.0f}", font=("Helvetica Neue", 28, "bold"), text_color="#34C759").pack(anchor="w", padx=20)
        
        activity_pct = (data['total_activity_revenue'] / data['total_revenue'] * 100) if data['total_revenue'] > 0 else 0
        ctk.CTkLabel(activity_frame, text=f"{activity_pct:.1f}% of total revenue", font=("Helvetica Neue", 13), text_color="#86868b").pack(anchor="w", padx=20, pady=(5, 20))
        
        # Monthly Breakdown (if period is long enough)
        if len(data['days']) > 30:
            self.create_monthly_breakdown(data)
    
    def create_metric_card(self, parent, col, title, value, color, icon):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        card.grid(row=0, column=col, sticky="nsew", padx=8, pady=5)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x")
        
        ctk.CTkLabel(header, text=icon, font=("Helvetica Neue", 24)).pack(side="left")
        ctk.CTkLabel(header, text=title, font=("Helvetica Neue", 12), text_color="#86868b").pack(side="left", padx=(10, 0))
        
        ctk.CTkLabel(inner, text=value, font=("Helvetica Neue", 28, "bold"), text_color=color).pack(anchor="w", pady=(10, 0))
    
    def create_monthly_breakdown(self, data):
        section = ctk.CTkFrame(self.results_frame, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            section,
            text="Monthly Forecast",
            font=("Helvetica Neue", 20, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w", padx=25, pady=(25, 15))
        
        # Aggregate by month
        monthly_data = {}
        for day in data['days']:
            month_key = day['date'].strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {"revenue": 0, "days": 0}
            monthly_data[month_key]["revenue"] += day['total_revenue']
            monthly_data[month_key]["days"] += 1
        
        months_frame = ctk.CTkFrame(section, fg_color="transparent")
        months_frame.pack(fill="x", padx=25, pady=(0, 25))
        
        for month_key, month_data in monthly_data.items():
            row = ctk.CTkFrame(months_frame, fg_color="#F5F5F7", corner_radius=8)
            row.pack(fill="x", pady=3)
            
            inner = ctk.CTkFrame(row, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=10)
            
            # Parse month for display
            year, month = month_key.split("-")
            month_name = calendar.month_name[int(month)]
            
            ctk.CTkLabel(inner, text=f"{month_name} {year}", font=("Helvetica Neue", 14, "bold"), text_color="#1D1D1F").pack(side="left")
            ctk.CTkLabel(inner, text=f"${month_data['revenue']:,.0f}", font=("Helvetica Neue", 14, "bold"), text_color="#007AFF").pack(side="right")


if __name__ == "__main__":
    try:
        app = RevenuePredictionApp()
        app.mainloop()
    except ImportError:
        print("Error: customtkinter is not installed.")
        print("Please run: pip install customtkinter")

