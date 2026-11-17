import streamlit as st
from datetime import date, time

st.set_page_config(page_title="Campus Connect", page_icon="🚗", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp { background: #f6f8f6; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .hero {
        background: linear-gradient(120deg, #173c35, #285d50);
        padding: 2rem 2.2rem; border-radius: 18px; color: white;
        margin-bottom: 1.2rem;
    }
    .hero h1 { color: white; margin: 0; font-size: 2.3rem; }
    .hero p { color: #e0eee7; margin-bottom: 0; }
    .small-muted { color: #66736d; font-size: .9rem; }
    div[data-testid="stMetric"] {
        background: white; padding: 14px; border-radius: 12px;
        border: 1px solid #e4eae5;
    }
    .notice {
        background: #edf4ef; border-left: 4px solid #2b6655;
        padding: 12px 15px; border-radius: 8px; color: #25483c;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sample data and session state ----------
if "rides" not in st.session_state:
    st.session_state.rides = [
        {"driver":"Rahul K.", "route":"Woxsen University → Gachibowli",
         "date":str(date.today()), "time":"5:15 PM", "vehicle":"Sedan",
         "seats":2, "cost":120, "note":"Can pick up near the main gate."},
        {"driver":"Aarav M.", "route":"Woxsen University → Kondapur",
         "date":str(date.today()), "time":"5:30 PM", "vehicle":"Hatchback",
         "seats":3, "cost":100, "note":"Leaving after classes."},
        {"driver":"Meghana R.", "route":"Woxsen University → Miyapur",
         "date":str(date.today()), "time":"6:00 PM", "vehicle":"SUV",
         "seats":2, "cost":140, "note":"Two seats available."},
    ]
if "requests" not in st.session_state:
    st.session_state.requests = []
if "messages" not in st.session_state:
    st.session_state.messages = {
        "Rahul K.": [
            ("Rahul K.", "Hey! Are you looking for a ride to Gachibowli?"),
            ("You", "Yes, what time are you leaving?"),
            ("Rahul K.", "Around 5:15 PM. We can coordinate the pickup point.")
        ],
        "Aarav M.": [("Aarav M.", "Hi! I have seats available for the evening.")],
        "Meghana R.": [("Meghana R.", "Let me know if you want to share the ride.")]
    }

# ---------- Sidebar profile ----------
with st.sidebar:
    st.markdown("## 🚗 Campus Connect")
    st.caption("Woxsen University · Student Carpooling")
    st.divider()
    student_name = st.text_input("Your name", value="Saanvi")
    student_email = st.text_input("College email (demo)", placeholder="name@woxsen.edu.in")
    st.info("Prototype mode: identity details are not verified by a university server.")
    st.divider()
    st.caption("Project team")
    st.write("Saanvi · Meghana · Varsha · Owais")
    st.caption("Faculty: Dr. Ram Soorat")

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <h1>Campus Connect</h1>
  <p>Your journey, shared. Affordable rides. Trusted students. Better journeys.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="notice">A student-focused carpooling concept for finding shared rides, offering empty seats and coordinating with ride partners.</div>', unsafe_allow_html=True)
st.write("")

# Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Available demo rides", len(st.session_state.rides))
c2.metric("Your ride requests", len(st.session_state.requests))
c3.metric("Project modules", "4")

tabs = st.tabs(["🔎 Find a Ride", "🚘 Offer a Ride", "🧾 My Rides", "💬 Chatbox"])

# ---------- Find a Ride ----------
with tabs[0]:
    st.subheader("Find a ride")
    st.write("Search available student rides by destination, date or travel budget.")
    with st.form("search_form"):
        a, b = st.columns(2)
        with a:
            origin = st.text_input("Pickup location", "Woxsen University")
            destination = st.text_input("Destination", "Gachibowli")
        with b:
            travel_date = st.date_input("Travel date", value=date.today())
            max_cost = st.number_input("Maximum contribution per passenger (₹)", min_value=0, value=150, step=10)
        submitted = st.form_submit_button("Search available rides", type="primary", use_container_width=True)

    if submitted:
        st.session_state.search_filter = {
            "origin": origin.strip().lower(),
            "destination": destination.strip().lower(),
            "date": str(travel_date),
            "max_cost": max_cost
        }

    f = st.session_state.get("search_filter")
    rides = st.session_state.rides
    if f:
        # Demo matching: match destination text and cost. The origin is shown as the requested pickup;
        # route similarity in a production version would use geocoding/GPS.
        matches = [r for r in rides if f["destination"] in r["route"].lower()
                   and r["date"] == f["date"] and r["cost"] <= f["max_cost"]]
        st.caption(f"Showing sample matches for {origin if 'origin' in locals() else 'your pickup'} → {f['destination'].title()}.")
    else:
        matches = rides
        st.caption("Showing all sample rides. Enter your journey above to filter the listings.")

    if not matches:
        st.warning("No matching sample rides found. Try another destination, date or budget.")
    for idx, ride in enumerate(matches):
        with st.container(border=True):
            left, right = st.columns([3, 1])
            with left:
                st.markdown(f"### {ride['driver']}  ·  <span style='color:#287451;font-size:0.8em'>● Demo profile</span>", unsafe_allow_html=True)
                st.write(f"**{ride['route']}**")
                st.caption(f"{ride['date']} · {ride['time']} · {ride['vehicle']} · {ride['seats']} seats available")
                st.write(ride["note"])
            with right:
                st.metric("Contribution", f"₹{ride['cost']}")
                if st.button("Request to join", key=f"request_{idx}_{ride['driver']}", use_container_width=True):
                    item = {"driver": ride["driver"], "route": ride["route"],
                            "date": ride["date"], "time": ride["time"], "status": "Pending (demo)"}
                    if item not in st.session_state.requests:
                        st.session_state.requests.append(item)
                    st.success("Demo ride request added to My Rides.")

# ---------- Offer a Ride ----------
with tabs[1]:
    st.subheader("Offer a ride")
    st.write("Have an empty seat? Share your journey with fellow students.")
    with st.form("offer_form"):
        a, b = st.columns(2)
        with a:
            driver = st.text_input("Driver name", value=student_name or "Student")
            offer_origin = st.text_input("Pickup location", "Woxsen University")
            offer_destination = st.text_input("Destination", "Gachibowli")
            offer_date = st.date_input("Travel date", value=date.today(), key="offer_date")
        with b:
            offer_time = st.selectbox("Departure time", ["8:00 AM", "10:00 AM", "1:00 PM", "5:00 PM", "6:00 PM", "7:00 PM"])
            vehicle = st.selectbox("Vehicle type", ["Car", "SUV", "Hatchback", "Bike"])
            seats = st.selectbox("Available seats", [1, 2, 3, 4])
            contribution = st.number_input("Suggested contribution per passenger (₹)", min_value=0, value=120, step=10)
        note = st.text_area("Additional details (optional)", placeholder="Pickup point, luggage space, or other useful details.")
        publish = st.form_submit_button("Publish demo ride", type="primary", use_container_width=True)
    if publish:
        if not offer_origin.strip() or not offer_destination.strip() or not driver.strip():
            st.error("Please enter your name, pickup location and destination.")
        else:
            st.session_state.rides.append({
                "driver": driver.strip(), "route": f"{offer_origin.strip()} → {offer_destination.strip()}",
                "date": str(offer_date), "time": offer_time, "vehicle": vehicle,
                "seats": seats, "cost": int(contribution), "note": note.strip() or "No additional details."
            })
            st.success("Your ride has been added to the prototype listings.")
            st.info("This listing is stored only in the current app session. It is not published to a real student network.")

# ---------- My Rides ----------
with tabs[2]:
    st.subheader("My rides")
    st.write("Review the ride requests you have made during this demo.")
    if not st.session_state.requests:
        st.info("You have no ride requests yet. Visit Find a Ride and request to join a listing.")
    else:
        for i, req in enumerate(st.session_state.requests):
            with st.container(border=True):
                st.markdown(f"**Ride with {req['driver']}**")
                st.write(req["route"])
                st.caption(f"{req['date']} · {req['time']}")
                st.warning(req["status"])
                if st.button("Remove request", key=f"remove_{i}"):
                    st.session_state.requests.pop(i)
                    st.rerun()
    st.divider()
    st.caption(f"Currently listed sample and user-created rides: {len(st.session_state.rides)}")

# ---------- Chatbox ----------
with tabs[3]:
    st.subheader("Chatbox")
    st.write("Coordinate pickup points, departure times and ride details with other students.")
    names = list(st.session_state.messages.keys())
    selected = st.selectbox("Choose a conversation", names)
    conversation = st.session_state.messages[selected]
    chat_area = st.container(height=300, border=True)
    with chat_area:
        for sender, message in conversation:
            if sender == "You":
                st.chat_message("user").write(message)
            else:
                st.chat_message("assistant", avatar="🧑‍🎓").write(f"**{sender}**  \n{message}")
    with st.form("chat_form", clear_on_submit=True):
        message_text = st.text_input("Message", placeholder="Type a message...")
        send = st.form_submit_button("Send message", type="primary")
    if send:
        if message_text.strip():
            st.session_state.messages[selected].append(("You", message_text.strip()))
            st.success("Message added to this demo conversation.")
            st.rerun()
        else:
            st.warning("Type a message before sending.")

st.divider()
st.caption("Campus Connect · Design Thinking Project · Woxsen University")
st.caption("Created by Saanvi, Meghana, Varsha and Owais · Faculty: Dr. Ram Soorat")
st.caption("Prototype disclaimer: all rides, profiles, verification labels and messages are illustrative sample data. No real bookings, payments, identity checks, GPS tracking or external messages occur.")
