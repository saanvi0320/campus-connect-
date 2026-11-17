# Campus Connect — Student Carpooling Prototype

A Python + Streamlit interactive prototype for the Woxsen University Design Thinking project.

## Included modules
- Find a Ride: filter sample rides by destination, date and contribution budget.
- Offer a Ride: add a sample ride listing.
- My Rides: view and remove demo ride requests.
- Chatbox: switch between sample conversations and send demo messages.

## Run locally (no HTML files required)

1. Install Python 3.9 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Start the app:

   `streamlit run app.py`

5. Open the local URL shown in the terminal (usually http://localhost:8501).

## Optional: publish a shareable link

1. Upload `app.py`` and `requirements.txt` to a GitHub repository.
2. Sign in to Streamlit Community Cloud.
3. Choose **Create app**, select your repository and `app.py`.
4. Deploy and share the generated app URL with your professor.

## Important prototype limitations

This is a demonstration, not a production ride-sharing service. Sample student profiles, rides and conversations are illustrative. Data is held in the app session and may reset. There is no real university identity verification, live GPS/route matching, persistent database, payment handling, or real-time messaging. Do not use it to arrange actual rides until those safety and backend features are implemented and tested.

## Project details

- Institution: Woxsen University
- Team: Saanvi, Meghana, Varsha and Owais
- Faculty: Dr. Ram Soorat
