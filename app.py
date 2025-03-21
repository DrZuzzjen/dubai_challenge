import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from data.destinations import destinations
from data.packages import packages
from data.accommodations import accommodations

# Page configuration
st.set_page_config(
    page_title="Dubai to the Stars 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0a1128;
        color: #e0e0e0;
    }
    .stButton>button {
        background-color: #ffd700;
        color: #0a1128;
        font-weight: bold;
    }
    .css-10trblm {
        color: #ffd700;
    }
    .st-bw {
        background-color: #1a2980;
    }
    .css-1d391kg {
        background-color: #1a2980;
    }
    .sidebar .sidebar-content {
        background-color: #1a2980;
    }
</style>
""", unsafe_allow_html=True)

# Main navigation
def navigation():
    st.sidebar.title("Dubai Space Travel 🚀")
    
    # Add Dubai skyline image to sidebar
    st.sidebar.image("https://i.imgur.com/XO5fpwa.jpg", use_column_width=True)
    
    menu = st.sidebar.radio(
        "Navigation",
        ["Home", "Book a Trip", "Pricing & Packages", "Accommodations", "User Dashboard"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("Dubai to the Stars - The Ultimate Space Travel Experience")
    
    return menu

# Home page
def home():
    st.title("Dubai to the Stars 🚀")
    st.subheader("The Ultimate Space Travel Experience")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to the Future of Travel!
        
        Dubai is revolutionizing space travel with the world's first commercial 
        spaceport for civilian travel. Browse our selection of destinations
        from lunar resorts to orbital hotels and Mars expeditions.
        
        ### Why Choose Dubai Space Travel?
        - **Luxury Experience:** The gold standard in space tourism
        - **Cutting-Edge Technology:** The safest vessels in the industry
        - **Unforgettable Destinations:** From orbital hotels to Martian landscapes
        
        Book your journey to the stars today!
        """)
        
        if st.button("Book Now!", type="primary", use_container_width=True):
            st.session_state.menu = "Book a Trip"
            st.experimental_rerun()
    
    with col2:
        st.image("https://i.imgur.com/AY5Wp2t.jpg", caption="Dubai Starliner")
        
        # Upcoming launches counter
        st.markdown("### Next Launch:")
        next_launch = datetime(2025, 4, 15, 10, 30)
        current_date = datetime(2025, 3, 21)  # Hardcoded current date from context
        days_remaining = (next_launch - current_date).days
        
        st.markdown(f"**{days_remaining} days remaining**")
        st.progress(1 - days_remaining/30)  # Assuming 30 day countdown

# Trip Booking
def book_trip():
    st.title("Book Your Space Adventure 🚀")
    
    # Step 1: Choose Destination
    st.header("Step 1: Choose Your Destination")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_distance = st.selectbox(
            "Filter by Travel Distance:",
            ["All", "Near Earth (< 1000 km)", "Moon Distance", "Deep Space"]
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Popularity", "Travel Time", "Rating"]
        )
    
    # Display destinations as cards
    destinations_per_row = 3
    filtered_destinations = destinations  # Apply filters here in a real app
    
    # Create rows of destinations
    for i in range(0, len(filtered_destinations), destinations_per_row):
        row_destinations = filtered_destinations[i:i+destinations_per_row]
        cols = st.columns(destinations_per_row)
        
        for j, destination in enumerate(row_destinations):
            with cols[j]:
                st.subheader(destination["name"])
                st.image("https://i.imgur.com/QxogqE2.jpg", caption=destination["type"])  # Placeholder image
                st.write(f"**Distance:** {destination['distance']}")
                st.write(f"**Travel Time:** {destination['travel_time']}")
                st.write(destination["description"])
                
                if st.button(f"Select {destination['name']}", key=f"dest_{destination['id']}"):
                    st.session_state.selected_destination = destination
                    st.success(f"You selected {destination['name']}!")
    
    # Step 2: Choose Date
    st.header("Step 2: Choose Your Travel Date")
    
    col1, col2 = st.columns(2)
    with col1:
        departure_date = st.date_input(
            "Departure Date",
            min_value=datetime(2025, 3, 22).date(),
            max_value=datetime(2026, 12, 31).date()
        )
    
    with col2:
        num_travelers = st.slider("Number of Travelers", 1, 10, 2)
    
    # Step 3: Select Package
    st.header("Step 3: Select Your Travel Package")
    
    for package in packages:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(package["name"])
            st.write(package["description"])
            
            # List features
            features_html = "<ul>"
            for feature in package["features"][:3]:  # Show first 3 features
                features_html += f"<li>{feature}</li>"
            features_html += "</ul>"
            
            st.markdown(features_html, unsafe_allow_html=True)
            
            if len(package["features"]) > 3:
                with st.expander("View all features"):
                    for feature in package["features"]:
                        st.write(f"• {feature}")
        
        with col2:
            st.write(f"**Price:** {package['price']:,} {package['currency']}")
            st.write(f"**Duration:** {package['duration']}")
            
            if st.button(f"Select {package['name']}", key=f"pkg_{package['id']}"):
                st.session_state.selected_package = package
                st.success(f"You selected {package['name']}!")
    
    # Booking Summary
    if st.button("Continue to Booking Summary", type="primary", use_container_width=True):
        if 'selected_destination' not in st.session_state or 'selected_package' not in st.session_state:
            st.error("Please select both a destination and a package to continue.")
        else:
            # In a real app, you would save this information and proceed
            st.success("Booking information saved! Proceeding to accommodation selection.")
            st.session_state.menu = "Accommodations"
            st.experimental_rerun()

# Pricing & Packages
def pricing_packages():
    st.title("Pricing & Packages 💎")
    
    # Filtering options
    col1, col2 = st.columns(2)
    with col1:
        price_range = st.slider(
            "Price Range (AED)",
            min_value=100000,
            max_value=6000000,
            value=(100000, 6000000),
            step=100000
        )
    
    with col2:
        sort_option = st.selectbox(
            "Sort by:",
            ["Price (Low to High)", "Price (High to Low)", "Popularity"]
        )
    
    # Display package comparison
    st.header("Package Comparison")
    
    # Create DataFrame for comparison
    df_packages = pd.DataFrame([
        {
            "Package": p["name"],
            "Price (AED)": f"{p['price']:,}",
            "Features": len(p["features"]),
            "Best For": "Luxury Travelers" if p["price"] > 1000000 else "Budget Travelers",
            "Popularity": "⭐⭐⭐⭐⭐" if p["popular"] else "⭐⭐⭐"
        } for p in packages
    ])
    
    st.dataframe(df_packages, use_container_width=True)
    
    # Detailed package cards
    st.header("Detailed Package Information")
    
    for package in packages:
        if package["price"] >= price_range[0] and package["price"] <= price_range[1]:
            with st.expander(f"{package['name']} - {package['price']:,} {package['currency']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(package["description"])
                    
                    st.subheader("Included Features:")
                    for feature in package["features"]:
                        st.write(f"✓ {feature}")
                
                with col2:
                    st.image("https://i.imgur.com/VQVCOsE.jpg", caption=package["name"])  # Placeholder image
                    
                    if st.button(f"Book {package['name']}", key=f"book_pkg_{package['id']}"):
                        st.session_state.selected_package = package
                        st.session_state.menu = "Book a Trip"
                        st.experimental_rerun()
    
    # VIP Experience highlight
    st.header("VIP Zero-Gravity Experiences")
    
    vip_experiences = [
        {
            "name": "Space Walk Adventure",
            "price": 750000,
            "description": "Experience the thrill of floating in space with a guided space walk."
        },
        {
            "name": "Zero-G Fine Dining",
            "price": 250000,
            "description": "Enjoy a 7-course meal prepared by Michelin-starred chefs in zero gravity."
        },
        {
            "name": "Orbital Photography Masterclass",
            "price": 350000,
            "description": "Learn to capture Earth and space in stunning detail with professional equipment."
        }
    ]
    
    cols = st.columns(3)
    for i, exp in enumerate(vip_experiences):
        with cols[i]:
            st.subheader(exp["name"])
            st.write(f"**Price:** {exp['price']:,} AED")
            st.write(exp["description"])
            st.button(f"Add to Booking", key=f"vip_{i}")

# Accommodations
def accommodations_page():
    st.title("Space Accommodations 🏨")
    
    # Filtering options
    col1, col2 = st.columns(2)
    with col1:
        location_filter = st.selectbox(
            "Filter by Location:",
            ["All Locations"] + list(set(acc["location"] for acc in accommodations))
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Price (Low to High)", "Price (High to Low)", "Rating"]
        )
    
    # Apply filters
    filtered_accommodations = accommodations
    if location_filter != "All Locations":
        filtered_accommodations = [acc for acc in accommodations if acc["location"] == location_filter]
    
    # Sort accommodations
    if sort_by == "Price (Low to High)":
        filtered_accommodations = sorted(filtered_accommodations, key=lambda x: x["price_per_night"])
    elif sort_by == "Price (High to Low)":
        filtered_accommodations = sorted(filtered_accommodations, key=lambda x: x["price_per_night"], reverse=True)
    elif sort_by == "Rating":
        filtered_accommodations = sorted(filtered_accommodations, key=lambda x: x["rating"], reverse=True)
    
    # Display accommodations
    for acc in filtered_accommodations:
        if not acc["available"]:
            continue  # Skip unavailable accommodations
            
        st.markdown(f"### {acc['name']}")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Location:** {acc['location']}")
            st.write(f"**Type:** {acc['type']}")
            st.write(f"**Rating:** {'⭐' * int(acc['rating'])}")
            st.write(acc["description"])
            
            # Amenities
            st.markdown("#### Amenities")
            amenities_per_row = 2
            for i in range(0, len(acc["amenities"]), amenities_per_row):
                row_amenities = acc["amenities"][i:i+amenities_per_row]
                cols = st.columns(amenities_per_row)
                
                for j, amenity in enumerate(row_amenities):
                    if j < len(cols):
                        cols[j].write(f"✓ {amenity}")
        
        with col2:
            st.image("https://i.imgur.com/7JL3wML.jpg", caption=acc["name"])  # Placeholder image
            st.write(f"**Price per night:** {acc['price_per_night']:,} {acc['currency']}")
            
            # Booking widget
            check_in = st.date_input(
                "Check-in Date",
                min_value=datetime(2025, 3, 22).date(),
                max_value=datetime(2026, 12, 31).date(),
                key=f"check_in_{acc['id']}"
            )
            
            nights = st.slider(
                "Number of Nights",
                min_value=1,
                max_value=30,
                value=3,
                key=f"nights_{acc['id']}"
            )
            
            total_price = acc["price_per_night"] * nights
            st.write(f"**Total Price:** {total_price:,} {acc['currency']}")
            
            if st.button(f"Book {acc['name']}", key=f"book_acc_{acc['id']}"):
                st.session_state.selected_accommodation = acc
                st.session_state.accommodation_nights = nights
                st.session_state.check_in_date = check_in
                st.success(f"You selected {acc['name']} for {nights} nights!")
        
        st.markdown("---")
    
    # AI Recommendation System
    st.header("AI Accommodation Recommendations")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        budget = st.slider(
            "Your Budget per Night (AED)",
            min_value=50000,
            max_value=500000,
            value=100000,
            step=10000
        )
    
    with col2:
        preference = st.selectbox(
            "Your Preference",
            ["Luxury", "Views", "Activities", "Technology", "Privacy"]
        )
    
    with col3:
        location_pref = st.selectbox(
            "Preferred Location",
            ["Any"] + list(set(acc["location"] for acc in accommodations))
        )
    
    if st.button("Get Personalized Recommendations", type="primary"):
        # In a real app, you would use ML here. For the MVP, we'll fake it
        recommended = random.sample([a for a in accommodations if a["available"]], k=min(2, len(accommodations)))
        
        st.subheader("Based on Your Preferences")
        for rec in recommended:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"#### {rec['name']}")
                st.write(f"**Location:** {rec['location']}")
                st.write(f"**Why we recommend this:** This {rec['type']} perfectly matches your {preference} preference!")
                st.write(rec["description"])
            
            with col2:
                st.image("https://i.imgur.com/7JL3wML.jpg", caption=rec["name"])  # Placeholder image
                st.write(f"**Price per night:** {rec['price_per_night']:,} {rec['currency']}")
                if st.button(f"Book Now", key=f"rec_book_{rec['id']}"):
                    st.session_state.selected_accommodation = rec
                    st.success(f"You selected {rec['name']}!")

# User Dashboard
def user_dashboard():
    st.title("User Dashboard 👨‍🚀")
    
    # User profile
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://i.imgur.com/xptBmZs.jpg", caption="John Smith")  # Placeholder astronaut image
    
    with col2:
        st.header("John Smith")
        st.write("**Member Since:** January 15, 2025")
        st.write("**Space Traveler Status:** Silver")
        st.write("**Total Space Miles:** 384,400")
        
        # Progress to next tier
        st.write("**Progress to Gold Status:**")
        st.progress(0.7)
        st.write("*115,600 more Space Miles needed for Gold Status*")
    
    # Upcoming trips
    st.header("Your Upcoming Space Adventures")
    
    # Mock booking data
    if 'selected_destination' in st.session_state and 'selected_package' in st.session_state:
        upcoming_trips = [
            {
                "destination": st.session_state.selected_destination["name"],
                "package": st.session_state.selected_package["name"],
                "departure_date": "April 15, 2025",
                "status": "Confirmed",
                "countdown": 25  # days
            }
        ]
    else:
        # Default trip if none selected
        upcoming_trips = [
            {
                "destination": "Lunar Dubai Resort",
                "package": "Business Class Voyage",
                "departure_date": "April 15, 2025",
                "status": "Confirmed",
                "countdown": 25  # days
            }
        ]
    
    for trip in upcoming_trips:
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.subheader(trip["destination"])
            st.write(f"**Package:** {trip['package']}")
            st.write(f"**Departure:** {trip['departure_date']}")
        
        with col2:
            st.write("**Countdown to Launch:**")
            st.write(f"**{trip['countdown']} days remaining**")
            st.progress(1 - trip['countdown']/30)
        
        with col3:
            st.write(f"**Status:** {trip['status']}")
            
            if st.button("View Details", key=f"trip_details_{upcoming_trips.index(trip)}"):
                st.session_state.viewing_trip = trip
    
    # Trip details if selected
    if 'viewing_trip' in st.session_state:
        with st.expander("Trip Details", expanded=True):
            trip = st.session_state.viewing_trip
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"Your Journey to {trip['destination']}")
                st.write(f"**Departure Date:** {trip['departure_date']}")
                st.write(f"**Package:** {trip['package']}")
                st.write(f"**Status:** {trip['status']}")
                
                # Checklist
                st.markdown("#### Pre-flight Checklist")
                st.checkbox("Complete Medical Examination", value=True)
                st.checkbox("Attend Zero-G Training", value=True)
                st.checkbox("Submit Dietary Requirements", value=False)
                st.checkbox("Finalize Space Suit Fitting", value=False)
            
            with col2:
                st.subheader("Launch Schedule")
                st.info("""
                **April 15, 2025**
                - 06:00 - Arrival at Dubai Spaceport
                - 07:30 - Final Medical Check
                - 08:45 - Boarding Begins
                - 10:30 - Launch
                
                **Expected Arrival at Destination**
                - April 18, 2025, 16:45 Dubai Time
                """)
    
    # AI Travel Assistant
    st.header("AI Space Travel Assistant")
    
    user_question = st.text_input("Ask a question about your upcoming trip...")
    
    if user_question:
        # Simulate AI responses
        ai_responses = {
            "what should i pack": "For your trip to the Lunar Dubai Resort, we recommend packing light as most essentials are provided. Personal items, comfortable earth clothes, and any prescription medications are all you need. Your custom space suit will be provided at the resort.",
            "is wifi available": "Yes, all our space destinations feature high-speed quantum entanglement communication systems, allowing real-time video calls with Earth without delay.",
            "how long is the trip": "Your journey to the Lunar Dubai Resort will take approximately 3 days each way using our advanced fusion propulsion system.",
            "is food included": "Yes, your Business Class Voyage package includes gourmet meals prepared by our space-certified chefs. Special dietary requirements are accommodated if submitted 7 days before departure."
        }
        
        # Find the most relevant response
        best_match = None
        best_score = 0
        
        for key in ai_responses:
            # Very simple matching algorithm - in a real app, use NLP
            score = sum(word in user_question.lower() for word in key.split())
            if score > best_score:
                best_score = score
                best_match = key
        
        if best_score > 0:
            st.info(f"**AI Assistant:** {ai_responses[best_match]}")
        else:
            st.info("**AI Assistant:** I don't have specific information about that yet. Please contact our customer service for more details.")
    
    # Previous trips and reviews
    st.header("Your Travel History")
    
    previous_trips = [
        {
            "destination": "Dubai Space Elevator Station",
            "date": "February 10, 2025",
            "rating": 5,
            "review": "Amazing weekend getaway with spectacular Earth views!"
        }
    ]
    
    if previous_trips:
        for trip in previous_trips:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(trip["destination"])
                st.write(f"**Date:** {trip['date']}")
                st.write(f"**Rating:** {'⭐' * trip['rating']}")
                st.write(f"**Review:** {trip['review']}")
            
            with col2:
                st.image("https://i.imgur.com/N1amLdi.jpg", caption="Trip Photo")  # Placeholder image
    else:
        st.write("No previous trips yet. Your space adventure is just beginning!")

# Main app logic
def main():
    # Initialize session state for navigation
    if 'menu' not in st.session_state:
        st.session_state.menu = "Home"
    
    # Get menu from navigation or session state
    menu = navigation()
    
    # Override menu if set in session state
    if st.session_state.menu != menu:
        menu = st.session_state.menu
    
    # Display selected page
    if menu == "Home":
        home()
    elif menu == "Book a Trip":
        book_trip()
    elif menu == "Pricing & Packages":
        pricing_packages()
    elif menu == "Accommodations":
        accommodations_page()
    elif menu == "User Dashboard":
        user_dashboard()

if __name__ == "__main__":
    main()