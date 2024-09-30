import os
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import requests
import spacy
from textblob import TextBlob

# Load Spotify API credentials from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=20)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

#moods and situations
moods = {
    'happy': ['happy', 'joyful', 'excited', 'fun', 'cheerful', 'upbeat'],
    'sad': ['sad', 'depressed', 'unhappy', 'melancholy', 'gloomy'],
    'calm': ['calm', 'relaxed', 'peaceful', 'serene', 'tranquil'],
    'energetic': ['energetic', 'lively', 'dynamic'],
    'romantic': ['romantic', 'love', 'passionate', 'affectionate'],
    'angry': ['angry', 'frustrated', 'furious', 'rage'],
    'nostalgic': ['nostalgic', 'reminiscent', 'sentimental'],
    'anxious': ['anxious', 'nervous', 'tense'],
    'bored': ['bored', 'disinterested', 'apathetic'],
    'motivated': ['motivated', 'inspired', 'driven']
}

situations = {
    'party': ['party', 'celebration', 'festive'],
    'workout': ['workout', 'exercise', 'fitness', 'gym'],
    'study': ['study', 'focus', 'concentration', 'work'],
    'sleep': ['sleep', 'bedtime', 'lullaby'],
    'travel': ['travel', 'journey', 'road trip'],
    'breakup': ['breakup', 'heartbreak', 'separation'],
    'wedding': ['wedding', 'marriage', 'ceremony'],
    'rainy day': ['rainy', 'rain', 'cloudy', 'storm'],
    'beach': ['beach', 'summer', 'sunny', 'ocean'],
    'spiritual': ['spiritual', 'meditation', 'yoga']
}

# Function to get recommendations based on mood, situation, and language
def get_recommendations(query):
    # Comprehensive list of language codes
    language_codes = {
        'Hindi': 'hi',
        'Telugu': 'te',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Chinese': 'zh',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Russian': 'ru',
        'Arabic': 'ar',
        'Turkish': 'tr',
        'Dutch': 'nl',
        'Swedish': 'sv',
        'Danish': 'da',
        'Norwegian': 'no',
        'Finnish': 'fi',
        'Greek': 'el',
        'Hebrew': 'he',
        'Thai': 'th',
        'Vietnamese': 'vi',
        'Indonesian': 'id',
        'Malay': 'ms',
        'Bengali': 'bn',
        'Punjabi': 'pa',
        'Marathi': 'mr',
        'Gujarati': 'gu',
        'Kannada': 'kn',
        'Tamil': 'ta',
        'Urdu': 'ur',
        'Swahili': 'sw',
        'Filipino': 'tl',
        'Hungarian': 'hu',
        'Czech': 'cs',
        'Polish': 'pl',
        'Romanian': 'ro',
        'Ukrainian': 'uk'
    }

    doc = nlp(query)
    mood = ''
    language = ''
    love_related = False
    situation = ''

    # Extract mood, situation, and language information from the query
    for token in doc:
        # Check for moods
        for mood_key, mood_values in moods.items():
            if token.lemma_ in mood_values:
                mood = mood_key
                break

        # Check for situations
        for situation_key, situation_values in situations.items():
            if token.lemma_ in situation_values:
                situation = situation_key
                break

        # Check for love-related terms
        if token.lemma_ in ['love', 'loving']:
            love_related = True

        # Check for language
        for lang_name, lang_code in language_codes.items():
            if token.lemma_ in [lang_name.lower(), lang_name.lower()]:
                language = lang_code
                break

    # Use TextBlob for sentiment analysis as a backup
    if not mood:
        sentiment = TextBlob(query).sentiment.polarity
        
        if sentiment > 0.6:
            mood = 'happy'
        elif 0.4 < sentiment <= 0.6:
            mood = 'energetic'
        elif 0.2 < sentiment <= 0.4:
            mood = 'calm'
        elif -0.2 < sentiment <= 0.2:
            mood = 'neutral'
        elif -0.4 < sentiment <= -0.2:
            mood = 'anxious'
        elif -0.6 < sentiment <= -0.4:
            mood = 'sad'
        elif sentiment <= -0.6:
            mood = 'angry'
        else:
            mood = 'unknown'  # Fallback for any undefined ranges

    # Construct search query
    search_query = query
    if language:
        search_query += f' language:{language}'

    # Handle specific situations
    if situation == 'party':
        results = sp.search(q=f'party {search_query}', type='track', limit=10)
    elif situation == 'workout':
        results = sp.search(q=f'workout {search_query}', type='track', limit=10)
    elif situation == 'study':
        results = sp.search(q=f'study music {search_query}', type='track', limit=10)
    elif situation == 'sleep':
        results = sp.search(q=f'sleep music {search_query}', type='track', limit=10)
    elif situation == 'travel':
        results = sp.search(q=f'travel music {search_query}', type='track', limit=10)
    elif situation == 'breakup':
        results = sp.search(q=f'breakup songs {search_query}', type='track', limit=10)
    elif situation == 'wedding':
        results = sp.search(q=f'wedding music {search_query}', type='track', limit=10)
    elif situation == 'rainy day':
        results = sp.search(q=f'rainy day music {search_query}', type='track', limit=10)
    elif situation == 'beach':
        results = sp.search(q=f'beach music {search_query}', type='track', limit=10)
    elif situation == 'spiritual':
        results = sp.search(q=f'spiritual music {search_query}', type='track', limit=10)
    elif mood:
        results = sp.search(q=f'{mood} {search_query}', type='track', limit=10)
    else:
        results = sp.search(q=search_query, type='track', limit=10)
    
    return results['tracks']['items']


# Streamlit interface
st.markdown(
    """
    <style>
    *{
        color: white;
    }
    .main {
        color: black;
        background-image: url("https://images.pexels.com/photos/3721941/pexels-photo-3721941.jpeg?cs=srgb&dl=pexels-daniel-reche-718241-3721941.jpg&fm=jpg");
        background-size: cover;
        background-position: center;
    }
    .title {
        color: white;
        font-size: 3em;
        text-align: center;
        padding-top: 50px;
        padding-bottom: 20px;
        font-family: 'Times New Roman', sans-serif;
    }
    .subtitle {
        color: white;
        font-size: 1.5em;
        text-align: center;
        padding-bottom: 20px;
        font-family: 'Georgia';
    }
    .input-box {
        text-align: center;
        margin-bottom: 20px;
    }
    .input-box input {
        width: 80%;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #cccccc;
        font-size: 1em;
        margin-top: 10px;
    }

    .input-box button {
        width: 80%;
        padding: 10px;
        border-radius: 10px;
        background-color: #1DB954;
        border: none;
        color: #ffffff;
        font-size: 1em;
        margin-top: 10px;
    }
    .results {
        color: #ffffff;
        margin-top: 20px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    iframe {
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">Melobot: Your Music Recommendation Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask me to suggest you some songs!</div>', unsafe_allow_html=True)

query = st.text_input('Enter your request:', key='input_query')

if st.button('Get Recommendations'):
    if query:
        try:
            recommendations = get_recommendations(query)
            if recommendations:
                st.markdown('<div class="results">Here are some songs for you:</div>', unsafe_allow_html=True)
                for track in recommendations:
                    track_name = track['name']
                    artist_names = ", ".join([artist['name'] for artist in track['artists']])
                    track_url = track['external_urls']['spotify']
                    st.markdown(f'<div class="results">- {track_name} by {artist_names}</div>', unsafe_allow_html=True)
                    st.markdown(f'<iframe src="https://open.spotify.com/embed/track/{track["id"]}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="results">No recommendations found. Please try a different query.</div>', unsafe_allow_html=True)
        except requests.exceptions.ReadTimeout:
            st.markdown('<div class="results">The request timed out. Please try again.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="results">Please enter a query.</div>', unsafe_allow_html=True)
