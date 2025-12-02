# UI Redesign Prompt

You are an expert UI/UX designer and Python developer specializing in modern, clean interfaces using `customtkinter` (a modern wrapper for tkinter that provides rounded corners, modern themes, and high-DPI support).

Your task is to completely rewrite the existing hotel pricing calculator application to create a stunning, Apple-style interface. The goal is to make it look like a native macOS application with a clean, minimal aesthetic.

## Requirements

### 1. Visual Design (Apple/Modern Style)
- **Framework**: Use `customtkinter` instead of standard `tkinter` for native rounded corners and modern widgets.
- **Color Palette**: 
  - Background: Clean white (`#FFFFFF`) or very light grey (`#F5F5F7`)
  - Cards/Panels: White with subtle drop shadows
  - Accents: Apple blue (`#007AFF`) for primary actions
  - Text: San Francisco style font (use "Helvetica Neue" or "Segoe UI" as fallback), dark grey (`#1D1D1F`) for headings
- **Layout**:
  - Clean, centered card layout
  - Generous padding and whitespace
  - Rounded corners on everything (buttons, inputs, frames)
  - Subtle animations on hover

### 2. User Input Section
The user needs to provide only three inputs in a beautifully designed form:
1. **Start Date**: A modern date picker or clean text input
2. **End Date**: A modern date picker or clean text input
3. **Number of Cabins**: A stylish counter or dropdown (1-10)

### 3. Results Display
The results should appear elegantly below the inputs or in a new "quote" card:
- **Price per Night**: Displayed clearly with date breakdown
- **Total Price**: Large, bold, and prominent
- **Breakdown**: A clean list or table showing the price for each night
- **Quote Style**: Looks like a professional invoice or booking summary

### 4. functionality
- Keep the existing pricing logic (seasonality, holiday multipliers, etc.)
- Ensure the window is responsive and looks good on all screen sizes
- Add input validation with clean, non-intrusive error messages

## Implementation Steps
1. Install `customtkinter` (if not present, provide instructions)
2. Create a new `ModernPricingApp` class
3. Design the main window with a modern theme
4. Implement the date selection and cabin count inputs using modern widgets
5. Style the "Get Quote" button to look premium (rounded, blue, shadow)
6. Display the results in a clean, structured format

## Example Code Structure
```python
import customtkinter as ctk
from datetime import datetime, timedelta

# Set theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class ModernPricingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cabin Booking Quote")
        self.geometry("900x700")
        
        # Use rounded corners for everything
        # ... implementation ...
```

Generate the complete, runnable code for this new UI.

