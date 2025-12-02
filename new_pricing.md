# New Pricing Model & Activities Prompt

You are an expert Python developer and UI designer. Your task is to significantly upgrade the existing `ModernPricingApp` to include cabin types and activity bookings.

## 1. Cabin Types & Pricing
Introduce three distinct cabin types, each with a specific price multiplier relative to the base pricing logic. The user should be able to select the cabin type *before* getting a quote.

*   **Forest Cabin**: The standard option.
    *   Multiplier: **1.0x** (Base cost)
    *   Description: "Cozy cabin nestled in the woods."
*   **Treehouse Cabin**: A premium elevated experience.
    *   Multiplier: **1.8x** the Forest Cabin cost.
    *   Description: "Elevated living with panoramic views."
*   **Lakeview Cabin**: The luxury option.
    *   Multiplier: **2.8x** the Forest Cabin cost.
    *   Description: "Luxury waterfront villa with private dock."

**UI Requirement**: Use a stylish card selection or a segmented control (segmented button) to let the user pick the cabin type. Update the displayed price estimates dynamically if possible, or upon clicking "Get Quote".

## 2. Seasonal Activities
Allow users to book activities in advance. Some activities are only available in specific seasons.

**Activity List & Pricing (Per Person):**
*   **Guided Hiking**: $20 (All Seasons)
*   **Kayaking**: $40 (Spring, Summer, Fall) - *Not available in Winter (Dec, Jan, Feb)*
*   **Bike Rentals**: $30 (Spring, Summer, Fall)
*   **Hunting Tour**: $150 (Fall, Winter)
*   **Bungee Jumping**: $100 (Summer only)
*   **Zipline**: $60 (Spring, Summer, Fall)
*   **Couch Tubing / Banana Boat**: $45 (Summer only)

**UI Requirement**:
*   Display these activities as toggleable cards or checkboxes.
*   Only show activities that are available during the selected date range. If the trip spans multiple seasons, show activities available in *any* of those seasons, or strictly check overlap.
*   Allow selecting the number of participants for each activity (default to number of cabins * 2, or let user specify).

## 3. Implementation Details
*   Update the `calculate_quote` method to apply the cabin multiplier to the room price.
*   Calculate the total activity cost separately and add it to the final total.
*   Display the quote with a clear breakdown:
    *   Room Cost (Nightly breakdown + Cabin Type multiplier)
    *   Activity Cost (List of selected activities)
    *   **Grand Total**

Generate the complete, runnable Python code using `customtkinter` that implements these new features while maintaining the beautiful Apple-style aesthetic.

