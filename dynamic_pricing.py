import customtkinter as ctk
from datetime import datetime, timedelta
import random
from tkinter import messagebox

# Configuration
ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernPricingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Cabin Booking Quote")
        self.geometry("900x700")
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
        
        self.create_layout()

    def create_layout(self):
        # Main grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header Section ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=40, pady=(40, 20), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Cabin Booking Quote", 
            font=("Helvetica Neue", 32, "bold"),
            text_color="#1D1D1F"
        )
        self.title_label.pack(side="left")

        # --- Content Section ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, padx=40, pady=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=2) # Results take more space if side-by-side
        
        # Input Card
        self.input_card = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=15)
        self.input_card.grid(row=0, column=0, sticky="new", padx=(0, 20), ipady=20)
        self.input_card.grid_columnconfigure(0, weight=1)
        
        self.create_inputs(self.input_card)
        
        # Results Card
        self.results_card = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=15)
        self.results_card.grid(row=0, column=1, sticky="nsew", ipady=20)
        self.results_card.grid_columnconfigure(0, weight=1)
        self.results_card.grid_rowconfigure(1, weight=1) # Content expands
        
        self.create_results_placeholder(self.results_card)

    def create_inputs(self, parent):
        # Input Title
        ctk.CTkLabel(parent, text="Trip Details", font=("Helvetica Neue", 20, "bold"), text_color="#1D1D1F").pack(pady=(20, 25), padx=20, anchor="w")
        
        # Start Date
        ctk.CTkLabel(parent, text="Check-in Date", font=("Helvetica Neue", 14, "bold"), text_color="#86868b").pack(padx=20, anchor="w")
        self.start_date_entry = ctk.CTkEntry(
            parent, 
            placeholder_text="YYYY-MM-DD",
            height=40,
            font=("Helvetica Neue", 14),
            border_color="#E5E5E5",
            fg_color="#F5F5F7",
            text_color="#1D1D1F"
        )
        self.start_date_entry.pack(padx=20, pady=(5, 20), fill="x")
        self.start_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # End Date
        ctk.CTkLabel(parent, text="Check-out Date", font=("Helvetica Neue", 14, "bold"), text_color="#86868b").pack(padx=20, anchor="w")
        self.end_date_entry = ctk.CTkEntry(
            parent,
            placeholder_text="YYYY-MM-DD", 
            height=40,
            font=("Helvetica Neue", 14),
            border_color="#E5E5E5",
            fg_color="#F5F5F7",
            text_color="#1D1D1F"
        )
        self.end_date_entry.pack(padx=20, pady=(5, 20), fill="x")
        tomorrow = datetime.now() + timedelta(days=1)
        self.end_date_entry.insert(0, tomorrow.strftime("%Y-%m-%d"))

        # Cabins
        ctk.CTkLabel(parent, text="Number of Cabins", font=("Helvetica Neue", 14, "bold"), text_color="#86868b").pack(padx=20, anchor="w")
        
        self.cabins_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.cabins_frame.pack(padx=20, pady=(5, 30), fill="x")
        
        self.cabins_var = ctk.IntVar(value=1)
        
        self.cabin_minus = ctk.CTkButton(
            self.cabins_frame, 
            text="-", 
            width=40, 
            height=40,
            fg_color="#F5F5F7", 
            text_color="#1D1D1F",
            hover_color="#E5E5E5",
            command=self.decrement_cabins
        )
        self.cabin_minus.pack(side="left")
        
        self.cabin_label = ctk.CTkLabel(
            self.cabins_frame, 
            textvariable=self.cabins_var, 
            font=("Helvetica Neue", 18, "bold"),
            width=50,
            text_color="#1D1D1F"
        )
        self.cabin_label.pack(side="left", padx=10)
        
        self.cabin_plus = ctk.CTkButton(
            self.cabins_frame, 
            text="+", 
            width=40, 
            height=40,
            fg_color="#F5F5F7", 
            text_color="#1D1D1F",
            hover_color="#E5E5E5",
            command=self.increment_cabins
        )
        self.cabin_plus.pack(side="left")

        # Calculate Button
        self.calc_btn = ctk.CTkButton(
            parent,
            text="Get Quote",
            font=("Helvetica Neue", 16, "bold"),
            height=50,
            corner_radius=25,
            fg_color="#007AFF",
            hover_color="#0062CC",
            command=self.calculate_quote
        )
        self.calc_btn.pack(padx=20, pady=(10, 20), fill="x", side="bottom")

    def create_results_placeholder(self, parent):
        self.results_content = ctk.CTkFrame(parent, fg_color="transparent")
        self.results_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            self.results_content, 
            text="Ready to Book?", 
            font=("Helvetica Neue", 24, "bold"),
            text_color="#1D1D1F"
        ).pack(pady=(50, 10))
        
        ctk.CTkLabel(
            self.results_content, 
            text="Enter your trip details to get an instant quote.", 
            font=("Helvetica Neue", 16),
            text_color="#86868b"
        ).pack()

    def show_results(self, nightly_data, total_price, avg_price, nights, cabin_count):
        # Clear previous results
        for widget in self.results_card.winfo_children():
            widget.destroy()
            
        content = ctk.CTkFrame(self.results_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header, 
            text="Quote Summary", 
            font=("Helvetica Neue", 20, "bold"),
            text_color="#1D1D1F"
        ).pack(side="left")
        
        # Total Price Display
        total_frame = ctk.CTkFrame(content, fg_color="#F5F5F7", corner_radius=10)
        total_frame.pack(fill="x", pady=(0, 20), ipady=15)
        
        ctk.CTkLabel(
            total_frame, 
            text="Total Price", 
            font=("Helvetica Neue", 14),
            text_color="#86868b"
        ).pack(pady=(5, 0))
        
        ctk.CTkLabel(
            total_frame, 
            text=f"${total_price:,.2f}", 
            font=("Helvetica Neue", 36, "bold"),
            text_color="#007AFF"
        ).pack()
        
        subtext = f"{nights} Night{'s' if nights != 1 else ''} • {cabin_count} Cabin{'s' if cabin_count != 1 else ''}"
        ctk.CTkLabel(
            total_frame, 
            text=subtext, 
            font=("Helvetica Neue", 14),
            text_color="#1D1D1F"
        ).pack(pady=(5, 0))

        # Breakdown List
        ctk.CTkLabel(content, text="Price Breakdown", font=("Helvetica Neue", 16, "bold"), text_color="#1D1D1F", anchor="w").pack(fill="x", pady=(10, 10))
        
        scroll_frame = ctk.CTkScrollableFrame(content, fg_color="transparent", label_text="")
        scroll_frame.pack(fill="both", expand=True)
        
        for i, data in enumerate(nightly_data):
            row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            # Date
            date_frame = ctk.CTkFrame(row, fg_color="transparent")
            date_frame.pack(side="left")
            ctk.CTkLabel(
                date_frame, 
                text=data['date'].strftime("%a, %b %d"), 
                font=("Helvetica Neue", 14, "bold"),
                text_color="#1D1D1F"
            ).pack(anchor="w")
            
            # Tags (Holiday/Weekend)
            tags = []
            if data['is_holiday']: tags.append("Holiday")
            elif data['is_weekend']: tags.append("Weekend")
            
            if tags:
                ctk.CTkLabel(
                    date_frame,
                    text=" • ".join(tags),
                    font=("Helvetica Neue", 12),
                    text_color="#FF3B30" if data['is_holiday'] else "#86868b"
                ).pack(anchor="w")

            # Price
            price_text = f"${data['price']:,.2f}"
            if cabin_count > 1:
                price_text += f" × {cabin_count}"
                
            ctk.CTkLabel(
                row, 
                text=price_text, 
                font=("Helvetica Neue", 14, "bold"),
                text_color="#1D1D1F"
            ).pack(side="right")
            
            # Separator line (visual only)
            if i < len(nightly_data) - 1:
                ctk.CTkFrame(scroll_frame, height=1, fg_color="#E5E5E5").pack(fill="x", pady=2)

    # --- Logic Methods ---

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
            if 20 <= date.day <= 30:
                if date.day in [23, 24, 25]:
                    holiday_factor = 5.0
                else:
                    holiday_factor = 2.0
            elif date.day == 31:
                holiday_factor = 5.0
        elif month == 1:
            if date.day in [1, 2]:
                holiday_factor = 5.0
            elif date.day == 3:
                holiday_factor = 2.5
                
        return monthly_factors[month] * weekend_factor * holiday_factor

    def calculate_booking_window(self, days_until):
        if days_until >= 30: return 0.85
        elif days_until >= 14: return 0.90
        elif days_until >= 7: return 0.95
        elif days_until >= 3: return 1.0
        elif days_until >= 1: return 1.15
        else: return 1.25

    def calculate_price_for_date(self, date, days_until_checkin):
        # Base & Competitor
        alpha = self.base_price
        c_t = self.competitor_price
        
        # Factors
        s_t = self.calculate_seasonality(date)
        b_t = self.calculate_booking_window(days_until_checkin)
        w_t = self.external_factors['weather'] * self.external_factors['event']
        u = random.uniform(-0.05, 0.05)
        
        # Weights
        beta = self.weights['seasonality']
        gamma = self.weights['competitor']
        delta = self.weights['booking_window']
        epsilon = self.weights['external']
        zeta = self.weights['noise']
        
        # Formula
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
            days_until_checkin = (start_date - datetime.now()).days
            
            nightly_data = []
            total_price = 0
            
            for i in range(nights):
                current_date = start_date + timedelta(days=i)
                price_per_night = self.calculate_price_for_date(current_date, days_until_checkin)
                
                # Metadata for display
                is_weekend = current_date.weekday() >= 4
                # Simple holiday check for tag (logic repeated from calc but simplified for boolean)
                m, d = current_date.month, current_date.day
                is_holiday = (m == 12 and d >= 20) or (m == 1 and d <= 3)
                
                nightly_data.append({
                    'date': current_date,
                    'price': price_per_night,
                    'is_weekend': is_weekend,
                    'is_holiday': is_holiday
                })
                total_price += price_per_night
            
            # Apply cabin multiplier
            final_total = total_price * cabin_count
            avg_price = total_price / nights
            
            self.show_results(nightly_data, final_total, avg_price, nights, cabin_count)
            
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
