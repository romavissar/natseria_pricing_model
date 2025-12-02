import customtkinter as ctk
from datetime import datetime, timedelta
import random
from tkinter import messagebox

# Configuration
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Cabin Types Configuration
CABIN_TYPES = {
    "forest": {
        "name": "Forest Cabin",
        "multiplier": 1.0,
        "description": "Cozy cabin nestled in the woods.",
        "icon": "🌲"
    },
    "treehouse": {
        "name": "Treehouse Cabin", 
        "multiplier": 1.8,
        "description": "Elevated living with panoramic views.",
        "icon": "🏡"
    },
    "lakeview": {
        "name": "Lakeview Cabin",
        "multiplier": 2.8,
        "description": "Luxury waterfront villa with private dock.",
        "icon": "🏖️"
    }
}

# Activities Configuration
ACTIVITIES = {
    "hiking": {
        "name": "Guided Hiking",
        "price": 20,
        "seasons": ["spring", "summer", "fall", "winter"],
        "icon": "🥾"
    },
    "kayaking": {
        "name": "Kayaking",
        "price": 40,
        "seasons": ["spring", "summer", "fall"],
        "icon": "🛶"
    },
    "bike": {
        "name": "Bike Rentals",
        "price": 30,
        "seasons": ["spring", "summer", "fall"],
        "icon": "🚴"
    },
    "hunting": {
        "name": "Hunting Tour",
        "price": 150,
        "seasons": ["fall", "winter"],
        "icon": "🎯"
    },
    "bungee": {
        "name": "Bungee Jumping",
        "price": 100,
        "seasons": ["summer"],
        "icon": "🪂"
    },
    "zipline": {
        "name": "Zipline",
        "price": 60,
        "seasons": ["spring", "summer", "fall"],
        "icon": "🎿"
    },
    "tubing": {
        "name": "Couch Tubing / Banana Boat",
        "price": 45,
        "seasons": ["summer"],
        "icon": "🍌"
    }
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

def get_seasons_in_range(start_date, end_date):
    """Get all seasons covered by a date range"""
    seasons = set()
    current = start_date
    while current < end_date:
        seasons.add(get_season(current))
        current += timedelta(days=1)
    return seasons

class ModernPricingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Cabin Booking Quote")
        self.geometry("1100x850")
        self.resizable(True, True)
        
        # Pricing State
        self.base_price = 100.0
        self.competitor_price = 100.0
        self.weights = {
            'seasonality': 0.3,
            'competitor': 0.25,
            'booking_window': 0.2,
            'external': 0.15,
            'noise': 0.1
        }
        self.external_factors = {'weather': 1.0, 'event': 1.0}
        
        # Selection State
        self.selected_cabin = ctk.StringVar(value="forest")
        self.activity_vars = {}
        self.activity_counts = {}
        self.available_activities = []
        
        self.create_layout()

    def create_layout(self):
        # Main scrollable container
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header
        header = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            header, 
            text="Cabin Booking Quote", 
            font=("Helvetica Neue", 36, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header, 
            text="Select your cabin, dates, and activities to get an instant quote.", 
            font=("Helvetica Neue", 16),
            text_color="#86868b"
        ).pack(anchor="w", pady=(5, 0))

        # Content Grid
        content = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        
        # Left Column - Inputs
        left_col = ctk.CTkFrame(content, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        self.create_cabin_selector(left_col)
        self.create_date_inputs(left_col)
        self.create_cabin_count(left_col)
        self.create_activities_section(left_col)
        
        # Right Column - Results
        self.results_card = ctk.CTkFrame(content, fg_color="#FFFFFF", corner_radius=15)
        self.results_card.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        self.create_results_placeholder()
        
        # Calculate Button at bottom
        self.calc_btn = ctk.CTkButton(
            self.main_scroll,
            text="Get Quote",
            font=("Helvetica Neue", 18, "bold"),
            height=55,
            corner_radius=27,
            fg_color="#007AFF",
            hover_color="#0062CC",
            command=self.calculate_quote
        )
        self.calc_btn.pack(fill="x", pady=(30, 0))

    def create_cabin_selector(self, parent):
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            section, 
            text="Select Cabin Type", 
            font=("Helvetica Neue", 18, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        cabins_frame = ctk.CTkFrame(section, fg_color="transparent")
        cabins_frame.pack(fill="x", padx=20, pady=(0, 20))
        cabins_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, (key, cabin) in enumerate(CABIN_TYPES.items()):
            self.create_cabin_card(cabins_frame, key, cabin, i)

    def create_cabin_card(self, parent, key, cabin, col):
        def select():
            self.selected_cabin.set(key)
            self.update_cabin_selection()
        
        card = ctk.CTkFrame(
            parent, 
            fg_color="#F5F5F7" if self.selected_cabin.get() != key else "#E8F4FD",
            corner_radius=12,
            border_width=2,
            border_color="#E5E5E5" if self.selected_cabin.get() != key else "#007AFF"
        )
        card.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)
        
        # Make entire card clickable
        card.bind("<Button-1>", lambda e: select())
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=15)
        inner.bind("<Button-1>", lambda e: select())
        
        # Icon
        icon_label = ctk.CTkLabel(inner, text=cabin["icon"], font=("Helvetica Neue", 28))
        icon_label.pack()
        icon_label.bind("<Button-1>", lambda e: select())
        
        # Name
        name_label = ctk.CTkLabel(
            inner, 
            text=cabin["name"], 
            font=("Helvetica Neue", 14, "bold"),
            text_color="#1D1D1F"
        )
        name_label.pack(pady=(8, 2))
        name_label.bind("<Button-1>", lambda e: select())
        
        # Multiplier
        mult_text = "Base Price" if cabin["multiplier"] == 1.0 else f"{cabin['multiplier']}x"
        mult_label = ctk.CTkLabel(
            inner, 
            text=mult_text, 
            font=("Helvetica Neue", 12),
            text_color="#007AFF" if cabin["multiplier"] > 1 else "#86868b"
        )
        mult_label.pack()
        mult_label.bind("<Button-1>", lambda e: select())
        
        # Store reference for updating
        if not hasattr(self, 'cabin_cards'):
            self.cabin_cards = {}
        self.cabin_cards[key] = card

    def update_cabin_selection(self):
        for key, card in self.cabin_cards.items():
            if key == self.selected_cabin.get():
                card.configure(fg_color="#E8F4FD", border_color="#007AFF")
            else:
                card.configure(fg_color="#F5F5F7", border_color="#E5E5E5")

    def create_date_inputs(self, parent):
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            section, 
            text="Trip Dates", 
            font=("Helvetica Neue", 18, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        dates_frame = ctk.CTkFrame(section, fg_color="transparent")
        dates_frame.pack(fill="x", padx=20, pady=(0, 20))
        dates_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Start Date
        start_frame = ctk.CTkFrame(dates_frame, fg_color="transparent")
        start_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ctk.CTkLabel(start_frame, text="Check-in", font=("Helvetica Neue", 12), text_color="#86868b").pack(anchor="w")
        self.start_date_entry = ctk.CTkEntry(
            start_frame,
            placeholder_text="YYYY-MM-DD",
            height=45,
            font=("Helvetica Neue", 14),
            border_color="#E5E5E5",
            fg_color="#F5F5F7"
        )
        self.start_date_entry.pack(fill="x", pady=(5, 0))
        self.start_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.start_date_entry.bind("<FocusOut>", lambda e: self.update_available_activities())
        self.start_date_entry.bind("<Return>", lambda e: self.update_available_activities())
        
        # End Date
        end_frame = ctk.CTkFrame(dates_frame, fg_color="transparent")
        end_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        ctk.CTkLabel(end_frame, text="Check-out", font=("Helvetica Neue", 12), text_color="#86868b").pack(anchor="w")
        self.end_date_entry = ctk.CTkEntry(
            end_frame,
            placeholder_text="YYYY-MM-DD",
            height=45,
            font=("Helvetica Neue", 14),
            border_color="#E5E5E5",
            fg_color="#F5F5F7"
        )
        self.end_date_entry.pack(fill="x", pady=(5, 0))
        tomorrow = datetime.now() + timedelta(days=1)
        self.end_date_entry.insert(0, tomorrow.strftime("%Y-%m-%d"))
        self.end_date_entry.bind("<FocusOut>", lambda e: self.update_available_activities())
        self.end_date_entry.bind("<Return>", lambda e: self.update_available_activities())
        
        # Update Activities Button
        ctk.CTkButton(
            section,
            text="↻ Update Activities",
            font=("Helvetica Neue", 12),
            height=35,
            corner_radius=8,
            fg_color="#F5F5F7",
            text_color="#007AFF",
            hover_color="#E5E5E5",
            command=self.update_available_activities
        ).pack(padx=20, pady=(10, 20), anchor="e")

    def create_cabin_count(self, parent):
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            inner, 
            text="Number of Cabins", 
            font=("Helvetica Neue", 18, "bold"),
            text_color="#1D1D1F"
        ).pack(side="left")
        
        # Counter
        counter_frame = ctk.CTkFrame(inner, fg_color="#F5F5F7", corner_radius=10)
        counter_frame.pack(side="right")
        
        self.cabins_var = ctk.IntVar(value=1)
        
        ctk.CTkButton(
            counter_frame, 
            text="-", 
            width=40, 
            height=40,
            fg_color="transparent", 
            text_color="#1D1D1F",
            hover_color="#E5E5E5",
            command=self.decrement_cabins
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            counter_frame, 
            textvariable=self.cabins_var, 
            font=("Helvetica Neue", 18, "bold"),
            width=40,
            text_color="#1D1D1F"
        ).pack(side="left")
        
        ctk.CTkButton(
            counter_frame, 
            text="+", 
            width=40, 
            height=40,
            fg_color="transparent", 
            text_color="#1D1D1F",
            hover_color="#E5E5E5",
            command=self.increment_cabins
        ).pack(side="left", padx=5)

    def create_activities_section(self, parent):
        self.activities_section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        self.activities_section.pack(fill="x", pady=(0, 20))
        
        header = ctk.CTkFrame(self.activities_section, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            header, 
            text="Activities", 
            font=("Helvetica Neue", 18, "bold"),
            text_color="#1D1D1F"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Optional add-ons", 
            font=("Helvetica Neue", 12),
            text_color="#86868b"
        ).pack(side="right")
        
        self.activities_container = ctk.CTkFrame(self.activities_section, fg_color="transparent")
        self.activities_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Initial load
        self.update_available_activities()

    def update_available_activities(self):
        # Clear existing
        for widget in self.activities_container.winfo_children():
            widget.destroy()
        
        self.activity_vars = {}
        self.activity_counts = {}
        
        # Get seasons for date range
        try:
            start = datetime.strptime(self.start_date_entry.get().strip(), "%Y-%m-%d")
            end = datetime.strptime(self.end_date_entry.get().strip(), "%Y-%m-%d")
            if end > start:
                self.current_seasons = get_seasons_in_range(start, end)
            else:
                self.current_seasons = {get_season(datetime.now())}
        except:
            self.current_seasons = {get_season(datetime.now())}
        
        # Show ALL activities, but mark unavailable ones
        self.available_activities = []
        self.unavailable_activities = []
        
        for key, activity in ACTIVITIES.items():
            if any(s in activity["seasons"] for s in self.current_seasons):
                self.available_activities.append(key)
            else:
                self.unavailable_activities.append(key)
        
        # Create activity cards for available activities
        if self.available_activities:
            ctk.CTkLabel(
                self.activities_container,
                text="Available for your dates",
                font=("Helvetica Neue", 12, "bold"),
                text_color="#34C759"
            ).pack(anchor="w", pady=(0, 5))
            
            for key in self.available_activities:
                self.create_activity_card(key, ACTIVITIES[key], available=True)
        
        # Show unavailable activities (greyed out)
        if self.unavailable_activities:
            ctk.CTkLabel(
                self.activities_container,
                text="Not available for selected dates",
                font=("Helvetica Neue", 12, "bold"),
                text_color="#86868b"
            ).pack(anchor="w", pady=(15, 5))
            
            for key in self.unavailable_activities:
                self.create_activity_card(key, ACTIVITIES[key], available=False)

    def create_activity_card(self, key, activity, available=True):
        # Card styling based on availability
        card_color = "#F5F5F7" if available else "#FAFAFA"
        text_color = "#1D1D1F" if available else "#AAAAAA"
        
        card = ctk.CTkFrame(self.activities_container, fg_color=card_color, corner_radius=10)
        card.pack(fill="x", pady=5)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=12)
        
        # Left side - checkbox and info
        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        
        if available:
            self.activity_vars[key] = ctk.BooleanVar(value=False)
            
            checkbox = ctk.CTkCheckBox(
                left,
                text=f"{activity['icon']} {activity['name']}",
                variable=self.activity_vars[key],
                font=("Helvetica Neue", 14),
                text_color=text_color,
                fg_color="#007AFF",
                hover_color="#0062CC"
            )
            checkbox.pack(side="left")
        else:
            # Just a label for unavailable activities
            ctk.CTkLabel(
                left,
                text=f"{activity['icon']} {activity['name']}",
                font=("Helvetica Neue", 14),
                text_color=text_color
            ).pack(side="left")
        
        # Price and season info
        price_text = f"${activity['price']}/person"
        if not available:
            season_names = [s.capitalize() for s in activity['seasons']]
            price_text += f" • {', '.join(season_names)} only"
        
        ctk.CTkLabel(
            left,
            text=price_text,
            font=("Helvetica Neue", 12),
            text_color="#86868b" if available else "#BBBBBB"
        ).pack(side="left", padx=(15, 0))
        
        # Right side - participant count (only for available activities)
        if available:
            right = ctk.CTkFrame(inner, fg_color="transparent")
            right.pack(side="right")
            
            self.activity_counts[key] = ctk.IntVar(value=2)
            
            ctk.CTkLabel(right, text="Guests:", font=("Helvetica Neue", 12), text_color="#86868b").pack(side="left", padx=(0, 10))
            
            count_frame = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=8)
            count_frame.pack(side="left")
            
            ctk.CTkButton(
                count_frame, text="-", width=30, height=30,
                fg_color="transparent", text_color="#1D1D1F", hover_color="#E5E5E5",
                command=lambda k=key: self.decrement_activity(k)
            ).pack(side="left")
            
            ctk.CTkLabel(
                count_frame, 
                textvariable=self.activity_counts[key],
                font=("Helvetica Neue", 14, "bold"),
                width=30
            ).pack(side="left")
            
            ctk.CTkButton(
                count_frame, text="+", width=30, height=30,
                fg_color="transparent", text_color="#1D1D1F", hover_color="#E5E5E5",
                command=lambda k=key: self.increment_activity(k)
            ).pack(side="left")

    def increment_activity(self, key):
        if self.activity_counts[key].get() < 20:
            self.activity_counts[key].set(self.activity_counts[key].get() + 1)

    def decrement_activity(self, key):
        if self.activity_counts[key].get() > 1:
            self.activity_counts[key].set(self.activity_counts[key].get() - 1)

    def create_results_placeholder(self):
        content = ctk.CTkFrame(self.results_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            content, 
            text="📋", 
            font=("Helvetica Neue", 48)
        ).pack(pady=(80, 10))
        
        ctk.CTkLabel(
            content, 
            text="Your Quote", 
            font=("Helvetica Neue", 24, "bold"),
            text_color="#1D1D1F"
        ).pack()
        
        ctk.CTkLabel(
            content, 
            text="Fill in your trip details and\nclick 'Get Quote' to see pricing.", 
            font=("Helvetica Neue", 14),
            text_color="#86868b",
            justify="center"
        ).pack(pady=(10, 0))

    def show_results(self, data):
        # Clear previous
        for widget in self.results_card.winfo_children():
            widget.destroy()
        
        content = ctk.CTkScrollableFrame(self.results_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header
        ctk.CTkLabel(
            content, 
            text="Quote Summary", 
            font=("Helvetica Neue", 22, "bold"),
            text_color="#1D1D1F"
        ).pack(anchor="w", pady=(0, 20))
        
        # Grand Total
        total_frame = ctk.CTkFrame(content, fg_color="#007AFF", corner_radius=12)
        total_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            total_frame, 
            text="Grand Total", 
            font=("Helvetica Neue", 14),
            text_color="#FFFFFF"
        ).pack(pady=(15, 0))
        
        ctk.CTkLabel(
            total_frame, 
            text=f"${data['grand_total']:,.2f}", 
            font=("Helvetica Neue", 36, "bold"),
            text_color="#FFFFFF"
        ).pack()
        
        summary_text = f"{data['nights']} Night{'s' if data['nights'] != 1 else ''} • {data['cabin_count']} {data['cabin_name']}"
        ctk.CTkLabel(
            total_frame, 
            text=summary_text, 
            font=("Helvetica Neue", 12),
            text_color="#FFFFFF"
        ).pack(pady=(5, 15))
        
        # Room Cost Section
        self.create_section_header(content, "🏠 Accommodation", f"${data['room_total']:,.2f}")
        
        room_details = ctk.CTkFrame(content, fg_color="#F5F5F7", corner_radius=10)
        room_details.pack(fill="x", pady=(5, 15))
        
        for night in data['nightly_data']:
            row = ctk.CTkFrame(room_details, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=8)
            
            date_text = night['date'].strftime("%a, %b %d")
            tags = []
            if night['is_holiday']: tags.append("🎄")
            elif night['is_weekend']: tags.append("📅")
            
            ctk.CTkLabel(
                row,
                text=f"{date_text} {' '.join(tags)}",
                font=("Helvetica Neue", 13),
                text_color="#1D1D1F"
            ).pack(side="left")
            
            price_text = f"${night['price'] * data['cabin_multiplier']:,.2f}"
            if data['cabin_count'] > 1:
                price_text += f" × {data['cabin_count']}"
            
            ctk.CTkLabel(
                row,
                text=price_text,
                font=("Helvetica Neue", 13, "bold"),
                text_color="#1D1D1F"
            ).pack(side="right")
        
        # Cabin multiplier note
        if data['cabin_multiplier'] > 1:
            ctk.CTkLabel(
                room_details,
                text=f"Includes {data['cabin_multiplier']}x {data['cabin_name']} rate",
                font=("Helvetica Neue", 11),
                text_color="#86868b"
            ).pack(pady=(0, 10))
        
        # Activities Section
        if data['activities_total'] > 0:
            self.create_section_header(content, "🎯 Activities", f"${data['activities_total']:,.2f}")
            
            activities_details = ctk.CTkFrame(content, fg_color="#F5F5F7", corner_radius=10)
            activities_details.pack(fill="x", pady=(5, 15))
            
            for activity in data['selected_activities']:
                row = ctk.CTkFrame(activities_details, fg_color="transparent")
                row.pack(fill="x", padx=15, pady=8)
                
                ctk.CTkLabel(
                    row,
                    text=f"{activity['icon']} {activity['name']} × {activity['count']}",
                    font=("Helvetica Neue", 13),
                    text_color="#1D1D1F"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row,
                    text=f"${activity['total']:,.2f}",
                    font=("Helvetica Neue", 13, "bold"),
                    text_color="#1D1D1F"
                ).pack(side="right")

    def create_section_header(self, parent, title, amount):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text=title,
            font=("Helvetica Neue", 16, "bold"),
            text_color="#1D1D1F"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=amount,
            font=("Helvetica Neue", 16, "bold"),
            text_color="#007AFF"
        ).pack(side="right")

    # --- Pricing Logic ---

    def increment_cabins(self):
        if self.cabins_var.get() < 10:
            self.cabins_var.set(self.cabins_var.get() + 1)

    def decrement_cabins(self):
        if self.cabins_var.get() > 1:
            self.cabins_var.set(self.cabins_var.get() - 1)

    def calculate_seasonality(self, date):
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
            if date.day == 24 or date.day == 25 or date.day == 31:
                holiday_factor = 5.0  # Major holidays
            elif 20 <= date.day <= 30:
                holiday_factor = 3.5  # Holiday season
        elif month == 1:
            if date.day == 1:
                holiday_factor = 5.0  # New Year's Day
            elif date.day == 2:
                holiday_factor = 3.5  # Day after New Year
            elif date.day == 3:
                holiday_factor = 3.0  # Post New Year
                
        return monthly_factors[month] * weekend_factor * holiday_factor

    def calculate_booking_window(self, days_until):
        if days_until >= 30: return 0.85
        elif days_until >= 14: return 0.90
        elif days_until >= 7: return 0.95
        elif days_until >= 3: return 1.0
        elif days_until >= 1: return 1.15
        else: return 1.25

    def calculate_price_for_date(self, date, days_until_checkin):
        alpha = self.base_price
        c_t = self.competitor_price
        
        s_t = self.calculate_seasonality(date)
        b_t = self.calculate_booking_window(days_until_checkin)
        w_t = self.external_factors['weather'] * self.external_factors['event']
        u = random.uniform(-0.05, 0.05)
        
        beta = self.weights['seasonality']
        gamma = self.weights['competitor']
        delta = self.weights['booking_window']
        epsilon = self.weights['external']
        zeta = self.weights['noise']
        
        seasonality_adj = beta * (s_t - 1) * alpha
        competitor_adj = gamma * (c_t - alpha)
        booking_adj = delta * (b_t - 1) * alpha
        external_adj = epsilon * (w_t - 1) * alpha
        noise_adj = zeta * u * alpha
        
        final_price = alpha + seasonality_adj + competitor_adj + booking_adj + external_adj + noise_adj
        return max(final_price, alpha * 0.5)

    def calculate_quote(self):
        try:
            start_str = self.start_date_entry.get().strip()
            end_str = self.end_date_entry.get().strip()
            
            if not start_str or not end_str:
                messagebox.showwarning("Missing Info", "Please enter both check-in and check-out dates.")
                return
                
            start_date = datetime.strptime(start_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_str, "%Y-%m-%d")
            
            if start_date.date() < datetime.now().date():
                messagebox.showerror("Invalid Date", "Check-in date cannot be in the past.")
                return
                
            if end_date <= start_date:
                messagebox.showerror("Invalid Date", "Check-out date must be after check-in date.")
                return
            
            nights = (end_date - start_date).days
            cabin_count = self.cabins_var.get()
            cabin_key = self.selected_cabin.get()
            cabin_info = CABIN_TYPES[cabin_key]
            cabin_multiplier = cabin_info["multiplier"]
            days_until_checkin = (start_date - datetime.now()).days
            
            # Calculate nightly room prices
            nightly_data = []
            base_room_total = 0
            
            for i in range(nights):
                current_date = start_date + timedelta(days=i)
                price_per_night = self.calculate_price_for_date(current_date, days_until_checkin)
                
                m, d = current_date.month, current_date.day
                is_weekend = current_date.weekday() >= 4
                is_holiday = (m == 12 and d >= 20) or (m == 1 and d <= 3)
                
                nightly_data.append({
                    'date': current_date,
                    'price': price_per_night,
                    'is_weekend': is_weekend,
                    'is_holiday': is_holiday
                })
                base_room_total += price_per_night
            
            # Apply cabin multiplier and count
            room_total = base_room_total * cabin_multiplier * cabin_count
            
            # Calculate activities
            selected_activities = []
            activities_total = 0
            
            for key in self.available_activities:
                if key in self.activity_vars and self.activity_vars[key].get():
                    activity = ACTIVITIES[key]
                    count = self.activity_counts[key].get()
                    total = activity['price'] * count
                    
                    selected_activities.append({
                        'name': activity['name'],
                        'icon': activity['icon'],
                        'price': activity['price'],
                        'count': count,
                        'total': total
                    })
                    activities_total += total
            
            grand_total = room_total + activities_total
            
            # Show results
            self.show_results({
                'grand_total': grand_total,
                'room_total': room_total,
                'activities_total': activities_total,
                'nights': nights,
                'cabin_count': cabin_count,
                'cabin_name': cabin_info['name'],
                'cabin_multiplier': cabin_multiplier,
                'nightly_data': nightly_data,
                'selected_activities': selected_activities
            })
            
        except ValueError:
            messagebox.showerror("Format Error", "Please use YYYY-MM-DD format for dates.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        app = ModernPricingApp()
        app.mainloop()
    except ImportError:
        print("Error: customtkinter is not installed.")
        print("Please run: pip install customtkinter")
