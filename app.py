import streamlit as st
import requests
import time
import json
import pandas as pd
from datetime import datetime, timedelta
import openai
import os
import plotly.express as px
from dotenv import load_dotenv
import sqlite3
import re
from dateutil import parser
import numpy as np

# Multi-language support
LANGUAGES = {
    "English": {
        "establishment_name": "Enter Establishment Name",
        "apify_token": "Enter your Apify API token",
        "openai_token": "Enter your OpenAI API key",
        "load_reviews": "Load Reviews",
        "error_apify_token": "Please enter your Apify API token.",
        "error_openai_token": "Please enter your OpenAI API key.",
        "triggering_actor": "Triggering Apify actor for {}...",
        "waiting_run": "Waiting for {} run to finish...",
        "run_failed": "{} run failed or was aborted.",
        "error_details": "Error details: {}",
        "fetching_reviews": "Fetching reviews for {}...",
        "no_reviews_found": "No reviews found for {}. This might indicate an issue with the URL or scraper.",
        "error_fetching": "Error fetching {}: {}",
        "reviews_title": "{} Reviews",
        "last_24_months": "📊 Last 24 Months Average Ratings",
        "filter_reviews": "📅 Filter Reviews",
        "start_date": "Start Date",
        "end_date": "End Date",
        "review_statistics": "Review Statistics",
        "overall": "Overall",
        "reviews": "Reviews",
        "generate_summary": "Generate Summary",
        "report_review": "Report Review",
        "download_csv": "Download CSV",
        "summary_warning": "Summary generation is limited to 1 year of reviews. Please adjust the date range to generate a summary.",
        "review_table": "Review Table",
        "review_text": "Review Text",
        "review_text_help": "Full review text",
        "review_date": "Review Date",
        "rating": "Rating",
        "platform": "Platform",
        "reviewer": "Reviewer",
        "replied": "Replied",
        "ai_summary": "📝 AI Summary",
        "ai_report": "📊 AI Report",
        "reset_button": "Reset and Load New Reviews",
        "url_help": "Enter the {} URL for the establishment",
        "graph_title": "Average Rating by Month (Last 24 Months)",
        "month": "Month",
        "average_rating": "Average Rating",
        "paste_url": "Paste the {} URL",
        "press_enter": "Press enter to apply",
        "months": {
            "January": "January", "February": "February", "March": "March", "April": "April",
            "May": "May", "June": "June", "July": "July", "August": "August",
            "September": "September", "October": "October", "November": "November", "December": "December"
        }
    },
    "Español": {
        "establishment_name": "Ingrese el Nombre del Establecimiento",
        "apify_token": "Ingrese su token de API de Apify",
        "openai_token": "Ingrese su clave de API de OpenAI",
        "load_reviews": "Cargar Reseñas",
        "error_apify_token": "Por favor ingrese su token de API de Apify.",
        "error_openai_token": "Por favor ingrese su clave de API de OpenAI.",
        "triggering_actor": "Activando actor de Apify para {}...",
        "waiting_run": "Esperando que termine la ejecución de {}...",
        "run_failed": "La ejecución de {} falló o fue abortada.",
        "error_details": "Detalles del error: {}",
        "fetching_reviews": "Obteniendo reseñas para {}...",
        "no_reviews_found": "No se encontraron reseñas para {}. Esto podría indicar un problema con la URL o el scraper.",
        "error_fetching": "Error al obtener {}: {}",
        "reviews_title": "Reseñas de {}",
        "last_24_months": "📊 Promedio de Calificaciones de los Últimos 24 Meses",
        "filter_reviews": "📅 Filtrar Reseñas",
        "start_date": "Fecha de Inicio",
        "end_date": "Fecha de Fin",
        "review_statistics": "Estadísticas de Reseñas",
        "overall": "General",
        "reviews": "Reseñas",
        "generate_summary": "Generar Resumen",
        "report_review": "Reportar Reseña",
        "download_csv": "Descargar CSV",
        "summary_warning": "La generación de resumen está limitada a 1 año de reseñas. Por favor ajuste el rango de fechas para generar un resumen.",
        "review_table": "Tabla de Reseñas",
        "review_text": "Texto de la Reseña",
        "review_text_help": "Texto completo de la reseña",
        "review_date": "Fecha de la Reseña",
        "rating": "Calificación",
        "platform": "Plataforma",
        "reviewer": "Reseñador",
        "replied": "Respondido",
        "ai_summary": "📝 Resumen de IA",
        "ai_report": "📊 Reporte de IA",
        "reset_button": "Reiniciar y Cargar Nuevas Reseñas",
        "url_help": "Ingrese la URL de {} para el establecimiento",
        "graph_title": "Calificación Promedio por Mes (Últimos 24 Meses)",
        "month": "Mes",
        "average_rating": "Calificación Promedio",
        "paste_url": "Pegue la URL de {}",
        "press_enter": "Presione enter para aplicar",
        "months": {
            "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
            "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
            "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
        }
    },
    "Français": {
        "establishment_name": "Entrez le Nom de l'Établissement",
        "apify_token": "Entrez votre token API Apify",
        "openai_token": "Entrez votre clé API OpenAI",
        "load_reviews": "Charger les Avis",
        "error_apify_token": "Veuillez entrer votre token API Apify.",
        "error_openai_token": "Veuillez entrer votre clé API OpenAI.",
        "triggering_actor": "Déclenchement de l'acteur Apify pour {}...",
        "waiting_run": "Attente de la fin de l'exécution de {}...",
        "run_failed": "L'exécution de {} a échoué ou a été interrompue.",
        "error_details": "Détails de l'erreur: {}",
        "fetching_reviews": "Récupération des avis pour {}...",
        "no_reviews_found": "Aucun avis trouvé pour {}. Cela pourrait indiquer un problème avec l'URL ou le scraper.",
        "error_fetching": "Erreur lors de la récupération de {}: {}",
        "reviews_title": "Avis de {}",
        "last_24_months": "📊 Notes Moyennes des 24 Derniers Mois",
        "filter_reviews": "📅 Filtrer les Avis",
        "start_date": "Date de Début",
        "end_date": "Date de Fin",
        "review_statistics": "Statistiques des Avis",
        "overall": "Global",
        "reviews": "Avis",
        "generate_summary": "Générer un Résumé",
        "report_review": "Signaler un Avis",
        "download_csv": "Télécharger CSV",
        "summary_warning": "La génération de résumé est limitée à 1 an d'avis. Veuillez ajuster la plage de dates pour générer un résumé.",
        "review_table": "Tableau des Avis",
        "review_text": "Texte de l'Avis",
        "review_text_help": "Texte complet de l'avis",
        "review_date": "Date de l'Avis",
        "rating": "Note",
        "platform": "Plateforme",
        "reviewer": "Auteur",
        "replied": "Répondu",
        "ai_summary": "📝 Résumé IA",
        "ai_report": "📊 Rapport IA",
        "reset_button": "Réinitialiser et Charger de Nouveaux Avis",
        "url_help": "Entrez l'URL de {} pour l'établissement",
        "graph_title": "Note Moyenne par Mois (24 Derniers Mois)",
        "month": "Mois",
        "average_rating": "Note Moyenne",
        "paste_url": "Collez l'URL de {}",
        "press_enter": "Appuyez sur entrée pour appliquer",
        "months": {
            "January": "Janvier", "February": "Février", "March": "Mars", "April": "Avril",
            "May": "Mai", "June": "Juin", "July": "Juillet", "August": "Août",
            "September": "Septembre", "October": "Octobre", "November": "Novembre", "December": "Décembre"
        }
    },
    "Deutsch": {
        "establishment_name": "Name des Unternehmens eingeben",
        "apify_token": "Ihr Apify API-Token eingeben",
        "openai_token": "Ihr OpenAI API-Schlüssel eingeben",
        "load_reviews": "Bewertungen laden",
        "error_apify_token": "Bitte geben Sie Ihren Apify API-Token ein.",
        "error_openai_token": "Bitte geben Sie Ihren OpenAI API-Schlüssel ein.",
        "triggering_actor": "Apify-Aktor für {} wird ausgelöst...",
        "waiting_run": "Warten auf Beendigung des {} Laufs...",
        "run_failed": "{} Lauf fehlgeschlagen oder abgebrochen.",
        "error_details": "Fehlerdetails: {}",
        "fetching_reviews": "Bewertungen für {} werden abgerufen...",
        "no_reviews_found": "Keine Bewertungen für {} gefunden. Dies könnte auf ein Problem mit der URL oder dem Scraper hinweisen.",
        "error_fetching": "Fehler beim Abrufen von {}: {}",
        "reviews_title": "{} Bewertungen",
        "last_24_months": "📊 Durchschnittliche Bewertungen der letzten 24 Monate",
        "filter_reviews": "📅 Bewertungen filtern",
        "start_date": "Startdatum",
        "end_date": "Enddatum",
        "review_statistics": "Bewertungsstatistiken",
        "overall": "Gesamt",
        "reviews": "Bewertungen",
        "generate_summary": "Zusammenfassung generieren",
        "report_review": "Bewertung melden",
        "download_csv": "CSV herunterladen",
        "summary_warning": "Die Zusammenfassungsgenerierung ist auf 1 Jahr Bewertungen beschränkt. Bitte passen Sie den Datumsbereich an, um eine Zusammenfassung zu generieren.",
        "review_table": "Bewertungstabelle",
        "review_text": "Bewertungstext",
        "review_text_help": "Vollständiger Bewertungstext",
        "review_date": "Bewertungsdatum",
        "rating": "Bewertung",
        "platform": "Plattform",
        "reviewer": "Bewerter",
        "replied": "Beantwortet",
        "ai_summary": "📝 KI-Zusammenfassung",
        "ai_report": "📊 KI-Bericht",
        "reset_button": "Zurücksetzen und neue Bewertungen laden",
        "url_help": "Geben Sie die {} URL für das Unternehmen ein",
        "graph_title": "Durchschnittliche Bewertung nach Monat (Letzte 24 Monate)",
        "month": "Monat",
        "average_rating": "Durchschnittliche Bewertung",
        "paste_url": "Fügen Sie die {} URL ein",
        "press_enter": "Drücken Sie Enter zum Anwenden",
        "months": {
            "January": "Januar", "February": "Februar", "March": "März", "April": "April",
            "May": "Mai", "June": "Juni", "July": "Juli", "August": "August",
            "September": "September", "October": "Oktober", "November": "November", "December": "Dezember"
        }
    },
    "Italiano": {
        "establishment_name": "Inserisci il Nome della Struttura",
        "apify_token": "Inserisci il tuo token API Apify",
        "openai_token": "Inserisci la tua chiave API OpenAI",
        "load_reviews": "Carica Recensioni",
        "error_apify_token": "Inserisci il tuo token API Apify.",
        "error_openai_token": "Inserisci la tua chiave API OpenAI.",
        "triggering_actor": "Attivazione attore Apify per {}...",
        "waiting_run": "Attesa del completamento dell'esecuzione di {}...",
        "run_failed": "L'esecuzione di {} è fallita o è stata interrotta.",
        "error_details": "Dettagli errore: {}",
        "fetching_reviews": "Recupero recensioni per {}...",
        "no_reviews_found": "Nessuna recensione trovata per {}. Questo potrebbe indicare un problema con l'URL o lo scraper.",
        "error_fetching": "Errore nel recupero di {}: {}",
        "reviews_title": "Recensioni di {}",
        "last_24_months": "📊 Valutazioni Medie degli Ultimi 24 Mesi",
        "filter_reviews": "📅 Filtra Recensioni",
        "start_date": "Data di Inizio",
        "end_date": "Data di Fine",
        "review_statistics": "Statistiche Recensioni",
        "overall": "Generale",
        "reviews": "Recensioni",
        "generate_summary": "Genera Riepilogo",
        "report_review": "Segnala Recensione",
        "download_csv": "Scarica CSV",
        "summary_warning": "La generazione del riepilogo è limitata a 1 anno di recensioni. Regola l'intervallo di date per generare un riepilogo.",
        "review_table": "Tabella Recensioni",
        "review_text": "Testo Recensione",
        "review_text_help": "Testo completo della recensione",
        "review_date": "Data Recensione",
        "rating": "Valutazione",
        "platform": "Piattaforma",
        "reviewer": "Recensore",
        "replied": "Risposto",
        "ai_summary": "📝 Riepilogo IA",
        "ai_report": "📊 Rapporto IA",
        "reset_button": "Ripristina e Carica Nuove Recensioni",
        "url_help": "Inserisci l'URL di {} per la struttura",
        "graph_title": "Valutazione Media per Mese (Ultimi 24 Mesi)",
        "month": "Mese",
        "average_rating": "Valutazione Media",
        "paste_url": "Incolla l'URL di {}",
        "press_enter": "Premi invio per applicare",
        "months": {
            "January": "Gennaio", "February": "Febbraio", "March": "Marzo", "April": "Aprile",
            "May": "Maggio", "June": "Giugno", "July": "Luglio", "August": "Agosto",
            "September": "Settembre", "October": "Ottobre", "November": "Novembre", "December": "Dicembre"
        }
    },
    "Dansk": {
        "establishment_name": "Indtast Virksomhedens Navn",
        "apify_token": "Indtast din Apify API token",
        "openai_token": "Indtast din OpenAI API nøgle",
        "load_reviews": "Indlæs Anmeldelser",
        "error_apify_token": "Indtast venligst din Apify API token.",
        "error_openai_token": "Indtast venligst din OpenAI API nøgle.",
        "triggering_actor": "Aktiverer Apify actor for {}...",
        "waiting_run": "Venter på at {} kørsel er færdig...",
        "run_failed": "{} kørsel mislykkedes eller blev afbrudt.",
        "error_details": "Fejldetaljer: {}",
        "fetching_reviews": "Henter anmeldelser for {}...",
        "no_reviews_found": "Ingen anmeldelser fundet for {}. Dette kan indikere et problem med URL'en eller scraperen.",
        "error_fetching": "Fejl ved hentning af {}: {}",
        "reviews_title": "{} Anmeldelser",
        "last_24_months": "📊 Gennemsnitlige Bedømmelser for de Sidste 24 Måneder",
        "filter_reviews": "📅 Filtrer Anmeldelser",
        "start_date": "Startdato",
        "end_date": "Slutdato",
        "review_statistics": "Anmeldelses Statistikker",
        "overall": "Samlet",
        "reviews": "Anmeldelser",
        "generate_summary": "Generer Sammenfatning",
        "report_review": "Rapporter Anmeldelse",
        "download_csv": "Download CSV",
        "summary_warning": "Generering af sammenfatning er begrænset til 1 års anmeldelser. Juster venligst datoområdet for at generere en sammenfatning.",
        "review_table": "Anmeldelses Tabel",
        "review_text": "Anmeldelses Tekst",
        "review_text_help": "Fuld anmeldelses tekst",
        "review_date": "Anmeldelses Dato",
        "rating": "Bedømmelse",
        "platform": "Platform",
        "reviewer": "Anmelder",
        "replied": "Besvaret",
        "ai_summary": "📝 AI Sammenfatning",
        "ai_report": "📊 AI Rapport",
        "reset_button": "Nulstil og Indlæs Nye Anmeldelser",
        "url_help": "Indtast {} URL'en for virksomheden",
        "graph_title": "Gennemsnitlig Bedømmelse per Måned (Sidste 24 Måneder)",
        "month": "Måned",
        "average_rating": "Gennemsnitlig Bedømmelse",
        "paste_url": "Indsæt {} URL'en",
        "press_enter": "Tryk enter for at anvende",
        "months": {
            "January": "Januar", "February": "Februar", "March": "Marts", "April": "April",
            "May": "Maj", "June": "Juni", "July": "Juli", "August": "August",
            "September": "September", "October": "Oktober", "November": "November", "December": "December"
        }
    }
}

# Add flag emojis for each language
LANGUAGE_FLAGS = {
    "English": "🇬🇧",
    "Español": "🇪🇸",
    "Français": "🇫🇷",
    "Deutsch": "🇩🇪",
    "Italiano": "🇮🇹",
    "Dansk": "🇩🇰"
}

# Initialize session state variables at the very beginning
if 'language' not in st.session_state:
    st.session_state.language = "English"
if 'establishment_name' not in st.session_state:
    st.session_state.establishment_name = "Snake Catcher"
if 'start_date' not in st.session_state:
    st.session_state.start_date = pd.Timestamp.now() - pd.Timedelta(days=30)
if 'end_date' not in st.session_state:
    st.session_state.end_date = pd.Timestamp.now()
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'report' not in st.session_state:
    st.session_state.report = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = None
# Establishments: list of dicts with name, URLs, and password
ESTABLISHMENTS_FILE = "establishments.json"
def load_establishments():
    if os.path.exists(ESTABLISHMENTS_FILE):
        try:
            with open(ESTABLISHMENTS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_establishments(establishments):
    with open(ESTABLISHMENTS_FILE, "w") as f:
        json.dump(establishments, f, indent=2)

if 'establishments' not in st.session_state:
    # Load from global database instead of local file
    st.session_state.establishments = update_local_establishments_from_global()
if 'selected_establishment_idx' not in st.session_state:
    st.session_state.selected_establishment_idx = None
if 'establishment_access' not in st.session_state:
    st.session_state.establishment_access = {}

# Load environment variables
load_dotenv()

# Get API keys from environment variables or Streamlit secrets
try:
    # Try Streamlit secrets first (for cloud deployment)
    DEFAULT_APIFY_API_TOKEN = st.secrets["APIFY_API_TOKEN"]
    DEFAULT_OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    # Fall back to environment variables (for local development)
    DEFAULT_APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
    DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- Database Helper Functions ---
DB_FILE = 'reviews.db'
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        # Reviews table
        conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            establishment_name TEXT,
            platform TEXT,
            review_date TEXT,
            star_rating REAL,
            review_text TEXT,
            reviewer_name TEXT,
            replied BOOLEAN
        )''')
        
        # Global establishments table
        conn.execute('''CREATE TABLE IF NOT EXISTS global_establishments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            booking_url TEXT,
            expedia_url TEXT,
            tripadvisor_url TEXT,
            google_maps_url TEXT,
            password TEXT,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_public BOOLEAN DEFAULT 1
        )''')

def insert_reviews(establishment_name, reviews):
    with sqlite3.connect(DB_FILE) as conn:
        conn.executemany('''INSERT INTO reviews (
            establishment_name, platform, review_date, star_rating, review_text, reviewer_name, replied
        ) VALUES (?, ?, ?, ?, ?, ?, ?)''', [
            (
                establishment_name,
                r.get('platform', ''),
                str(r.get('review_date', '')),
                r.get('star_rating', None),
                r.get('review_text', ''),
                r.get('reviewer_name', ''),
                int(r.get('replied', False))
            ) for r in reviews
        ])

def fetch_reviews_from_db(establishment_name):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute('''SELECT platform, review_date, star_rating, review_text, reviewer_name, replied FROM reviews WHERE establishment_name = ?''', (establishment_name,))
        rows = cur.fetchall()
        # Return as list of dicts
        return [
            {
                'platform': row[0],
                'review_date': row[1],
                'star_rating': row[2],
                'review_text': row[3],
                'reviewer_name': row[4],
                'replied': bool(row[5])
            } for row in rows
        ]

def delete_reviews(establishment_name):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('DELETE FROM reviews WHERE establishment_name = ?', (establishment_name,))

def insert_global_establishment(name, booking_url, expedia_url, tripadvisor_url, google_maps_url, password, created_by):
    with sqlite3.connect(DB_FILE) as conn:
        try:
            conn.execute('''INSERT INTO global_establishments 
                (name, booking_url, expedia_url, tripadvisor_url, google_maps_url, password, created_by) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                (name, booking_url, expedia_url, tripadvisor_url, google_maps_url, password, created_by))
            return True
        except sqlite3.IntegrityError:
            return False  # Establishment already exists

def fetch_global_establishments():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute('''SELECT name, booking_url, expedia_url, tripadvisor_url, google_maps_url, password, created_by, created_at 
                             FROM global_establishments WHERE is_public = 1 
                             ORDER BY created_at DESC''')
        rows = cur.fetchall()
        return [
            {
                'name': row[0],
                'Booking.com': row[1],
                'Expedia': row[2],
                'TripAdvisor': row[3],
                'Google Maps': row[4],
                'password': row[5],
                'created_by': row[6],
                'created_at': row[7]
            } for row in rows
        ]

def update_local_establishments_from_global():
    """Update local establishments from global database"""
    global_establishments = fetch_global_establishments()
    # Convert to the format expected by the app
    establishments = []
    for est in global_establishments:
        establishments.append({
            'name': est['name'],
            'Booking.com': est['Booking.com'],
            'Expedia': est['Expedia'],
            'TripAdvisor': est['TripAdvisor'],
            'Google Maps': est['Google Maps'],
            'password': est['password']
        })
    return establishments

def update_local_establishments_from_global():
    """Update local establishments from global database"""
    global_establishments = fetch_global_establishments()
    # Convert to the format expected by the app
    establishments = []
    for est in global_establishments:
        establishments.append({
            'name': est['name'],
            'Booking.com': est['Booking.com'],
            'Expedia': est['Expedia'],
            'TripAdvisor': est['TripAdvisor'],
            'Google Maps': est['Google Maps'],
            'password': est['password']
        })
    return establishments

# Initialize DB
init_db()

# Language selector at the top
def get_text(key):
    """Get text in the current language"""
    return LANGUAGES[st.session_state.language].get(key, key)

def translate_month(month_name):
    """Translate month name to current language"""
    months_dict = LANGUAGES[st.session_state.language].get("months", {})
    return months_dict.get(month_name, month_name)

# Set page config with dynamic title
st.set_page_config(
    page_title="RevyUp.io",
    page_icon="📊",
    layout="wide"
)

# Keep-alive mechanism for Streamlit Cloud
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = time.time()
else:
    st.session_state.last_activity = time.time()

# Initialize session state variables
if 'reviews_loaded' not in st.session_state:
    st.session_state.reviews_loaded = False
if 'reviews_df' not in st.session_state:
    st.session_state.reviews_df = None

# Add language selector at the top with flags
col_title, col_lang = st.columns([8, 2])
with col_title:
    st.title("RevyUp.io 📊")
with col_lang:
    language_options = [f"{LANGUAGE_FLAGS.get(lang, '')} {lang}" for lang in LANGUAGES.keys()]
    current_lang_flag = LANGUAGE_FLAGS.get(st.session_state.language, '')
    selected_language = st.selectbox(
        "Language",
        language_options,
        index=list(LANGUAGES.keys()).index(st.session_state.language),
        label_visibility="visible"
    )
    # Extract language name from selection
    selected_language_name = selected_language.split(' ', 1)[1] if ' ' in selected_language else selected_language
    if selected_language_name != st.session_state.language:
        st.session_state.language = selected_language_name
        st.rerun()

def trigger_actor(actor_id, api_token, start_url):
    run_url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={api_token}"
    
    # Platform-specific configurations
    if "booking-reviews-scraper" in actor_id:
        sort_by = "review_score_and_price"  # Valid for Booking.com
    elif "expedia-hotels-com-reviews-scraper" in actor_id:
        sort_by = "Most recent"  # Valid for Expedia
    elif "tripadvisor-reviews" in actor_id:
        sort_by = "Most recent"  # Valid for TripAdvisor
    elif "google-maps-reviews-scraper" in actor_id:
        sort_by = "Most recent"  # Valid for Google Maps
    else:
        sort_by = "Most recent"  # Default for other platforms
    
    # Configure the actor to fetch 2 years of reviews
    payload = {
        "startUrls": [{"url": start_url}],
        "maxReviews": 1000,  # Set a high number to ensure we get all reviews
        "maxReviewsPerPage": 100,  # Maximum reviews per page
        "maxPages": 10,  # Maximum number of pages to scrape
        "minRating": 1,  # Include all ratings
        "maxRating": 5,  # Include all ratings
        "sortBy": sort_by,
        "timeRange": "2y"  # Last 2 years
    }
    
    # Add platform-specific configurations
    if "google-maps-reviews-scraper" in actor_id:
        payload["includeReviewOrigin"] = True  # Ensure we get review origin for Google
    
    resp = requests.post(run_url, json=payload)
    resp.raise_for_status()
    run_data = resp.json()
    run_id = run_data["data"]["id"]
    return run_id

def wait_for_run(run_id, api_token):
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={api_token}"
    while True:
        resp = requests.get(status_url)
        resp.raise_for_status()
        data = resp.json()
        status = data["data"]["status"]
        if status in ["SUCCEEDED", "FAILED", "ABORTED"]:
            # Add detailed status information
            if status != "SUCCEEDED":
                st.error(f"Run status: {status}")
                st.error(f"Run details: {json.dumps(data['data'], indent=2)}")
            return data
        time.sleep(5)

def fetch_reviews_from_apify(dataset_id, api_token):
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={api_token}"
    resp = requests.get(dataset_url)
    resp.raise_for_status()
    return resp.json()

# Normalization functions
def normalize_date(date_str):
    """Helper function to normalize dates across all platforms"""
    if not date_str:
        return None
    try:
        # Try different date formats
        for fmt in ["%Y-%m-%d", "%d %b %Y", "%b %d, %Y", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]:
            try:
                date_obj = pd.to_datetime(date_str, format=fmt)
                return date_obj.strftime("%Y-%m-%d")
            except:
                continue
        # If none of the specific formats work, try pandas' automatic parsing
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime("%Y-%m-%d")
    except:
        return None

def normalize_booking_review(raw):
    rating_10 = raw.get("rating")
    rating_5 = round((rating_10 / 2), 1) if rating_10 is not None else None
    review_title = raw.get("reviewTitle")
    liked = raw.get('likedText', '')
    disliked = raw.get('dislikedText', '')
    
    # Format review text with clear sections
    review_parts = []
    if review_title:
        review_parts.append(f"Title: {review_title}")
    if liked:
        review_parts.append(f"Liked: {liked}")
    if disliked:
        review_parts.append(f"Disliked: {disliked}")
    
    review_text = "\n".join(review_parts)
    
    return {
        "platform": "Booking.com",
        "review_date": normalize_date(raw.get("reviewDate")),
        "reviewer_name": raw.get("userName"),
        "star_rating": rating_5,
        "review_text": review_text,
        "replied": raw.get("propertyResponse") is not None
    }

def normalize_expedia_review(raw):
    label = raw.get("reviewScoreWithDescription", {}).get("label", "")
    try:
        rating_10 = float(label.split(" out of ")[0])
        rating_5 = round(rating_10 / 2, 1)
    except Exception:
        rating_5 = None
    review_title = raw.get("title", "")
    review_text = raw.get("text", "")
    reviewer_name = raw.get("reviewAuthorAttribution", {}).get("text", "")
    replied = bool(raw.get("managementResponses"))
    
    # Format review text with title only if it exists
    if review_title:
        review_text = f"Title: {review_title}\n{review_text}"
    
    # Get and format the date
    date_str = raw.get("submissionTime", {}).get("longDateFormat", "")
    
    return {
        "platform": "Expedia",
        "review_date": normalize_date(date_str),
        "reviewer_name": reviewer_name,
        "star_rating": rating_5,
        "review_text": review_text.strip(),
        "replied": replied
    }

def normalize_tripadvisor_review(raw):
    review_title = raw.get("title", "")
    review_text = raw.get("text", "")
    reviewer_name = raw.get("user", {}).get("name", "")
    replied = raw.get("ownerResponse") is not None
    published_date = raw.get("publishedDate")
    
    # Format review text with title only if it exists
    if review_title:
        review_text = f"Title: {review_title}\n{review_text}"
    
    return {
        "platform": "TripAdvisor",
        "review_date": normalize_date(published_date),
        "reviewer_name": reviewer_name,
        "star_rating": raw.get("rating"),
        "review_text": review_text.strip(),
        "replied": replied
    }

def normalize_google_review(raw):
    # Only process reviews that have "Google" as their origin
    if raw.get("reviewOrigin") != "Google":
        return None
        
    review_title = raw.get("title", "")
    review_text = raw.get("text") or raw.get("textTranslated") or ""
    reviewer_name = raw.get("name", "")
    replied = raw.get("responseFromOwnerText") is not None
    star_rating = raw.get("stars")  # Use stars field directly
    published_date = raw.get("publishedAtDate")
    
    return {
        "platform": "Google",
        "review_date": normalize_date(published_date),
        "reviewer_name": reviewer_name,
        "star_rating": star_rating,
        "review_text": review_text.strip(),  # Remove title/establishment name
        "replied": replied
    }

def generate_summary(filtered_df, start_date, end_date, api_key):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
        return
    
    with st.spinner("Generating summary..."):
        try:
            # Prepare the reviews data for ChatGPT
            reviews_text = []
            
            for _, row in filtered_df.iterrows():
                # Full review text with clear formatting
                review_info = f"Date: {row['review_date'].strftime('%Y-%m-%d')}\n"
                review_info += f"Platform: {row['platform']}\n"
                review_info += f"Rating: {row['star_rating']} stars\n"
                review_info += f"Review: {row['review_text']}\n"
                review_info += f"Replied: {'Yes' if row['replied'] else 'No'}\n"
                review_info += "---\n"
                reviews_text.append(review_info)
            
            # Combine all reviews into a single text
            combined_reviews = "\n".join(reviews_text)
            
            # Get language instruction based on selected language
            language_instruction = {
                "English": "Please respond in English.",
                "Español": "Please respond in Spanish (Español).",
                "Français": "Please respond in French (Français).",
                "Deutsch": "Please respond in German (Deutsch).",
                "Italiano": "Please respond in Italian (Italiano).",
                "Dansk": "Please respond in Danish (Dansk)."
            }.get(st.session_state.language, "Please respond in English.")
            
            # Create the prompt for ChatGPT
            prompt = f"""Analyze these reviews from {start_date} to {end_date} and provide a structured summary with the following sections:

1. Overall Sentiment
2. Positive Highlights
3. Areas for Improvement
4. Actionable Suggestions
5. Unreplied Reviews (if any)

{language_instruction}

Reviews to analyze:
{combined_reviews}

Please provide a professional, concise, and solution-oriented summary that helps managers take efficient actions based on customer feedback insights."""

            # Call ChatGPT API
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a professional business analyst specializing in customer feedback analysis. {language_instruction}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Store the summary in session state
            st.session_state.summary = response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating summary: {str(e)}")

def generate_report(filtered_df, start_date, end_date, api_key):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
        return
    
    with st.spinner("Analyzing reviews for potential violations..."):
        try:
            # Prepare the reviews data for ChatGPT
            reviews_text = []
            
            for _, row in filtered_df.iterrows():
                # Full review text with clear formatting
                review_info = f"Date: {row['review_date'].strftime('%Y-%m-%d')}\n"
                review_info += f"Platform: {row['platform']}\n"
                review_info += f"Rating: {row['star_rating']} stars\n"
                review_info += f"Review: {row['review_text']}\n"
                review_info += f"Replied: {'Yes' if row['replied'] else 'No'}\n"
                review_info += "---\n"
                reviews_text.append(review_info)
            
            # Combine all reviews into a single text
            combined_reviews = "\n".join(reviews_text)
            
            # Get language instruction based on selected language
            language_instruction = {
                "English": "Please respond in English.",
                "Español": "Please respond in Spanish (Español).",
                "Français": "Please respond in French (Français).",
                "Deutsch": "Please respond in German (Deutsch).",
                "Italiano": "Please respond in Italian (Italiano).",
                "Dansk": "Please respond in Danish (Dansk)."
            }.get(st.session_state.language, "Please respond in English.")
            
            # Create the prompt for ChatGPT
            prompt = f"""Analyze these reviews from {start_date} to {end_date} and identify ONLY reviews that have clear, legitimate grounds for removal based on platform policies. For each flagged review, provide:

1. Review Details (date, platform, rating)
2. Specific Violation(s) Identified
3. Evidence from the review text
4. Draft message to the platform requesting removal

IMPORTANT: Only flag reviews that have CLEAR and UNDENIABLE violations. Do not include reviews that are simply negative or critical but legitimate. Focus strictly on identifying:

- Fake or fraudulent reviews (e.g., reviewer never stayed)
- Reviews from non-guests (e.g., competitors, non-customers)
- Offensive language or hate speech
- Personal attacks or threats
- Confidential information exposure
- Reviews for wrong business
- Reviews from canceled bookings/no-shows

{language_instruction}

Reviews to analyze:
{combined_reviews}

Please provide a professional, evidence-based analysis that ONLY includes reviews with clear violations of platform policies. If no reviews meet these strict criteria, state that no reviews were found that could be legitimately challenged."""

            # Call ChatGPT API
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a professional review policy compliance analyst specializing in identifying reviews that violate platform terms and conditions. {language_instruction}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Store the report in session state
            st.session_state.report = response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")


# Main app logic
if not st.session_state.reviews_loaded:
    col_title, col_refresh = st.columns([4, 1])
    with col_title:
        st.title("🌍 Global Establishment Manager")
    with col_refresh:
        if st.button("🔄 Refresh", help="Reload establishments from global database"):
            st.session_state.establishments = update_local_establishments_from_global()
            st.success("✅ Establishments refreshed from global database!")
            st.rerun()
    
    st.info("💡 **All establishments are shared globally!** When you add an establishment, it becomes available for all users to access.")
    # --- Establishment Management UI ---
    if 'edit_establishment_idx' not in st.session_state:
        st.session_state.edit_establishment_idx = None
    to_delete = None
    for idx, est in enumerate(st.session_state.establishments):
        if st.session_state.edit_establishment_idx == idx:
            # Edit mode for this establishment
            with st.form(f"edit_establishment_form_{idx}", clear_on_submit=False):
                new_name = st.text_input("Establishment Name", value=est['name'], key=f"edit_name_{idx}")
                new_booking = st.text_input("Booking.com URL", value=est['Booking.com'], key=f"edit_booking_{idx}")
                new_expedia = st.text_input("Expedia URL", value=est['Expedia'], key=f"edit_expedia_{idx}")
                new_tripadvisor = st.text_input("TripAdvisor URL", value=est['TripAdvisor'], key=f"edit_tripadvisor_{idx}")
                new_google = st.text_input("Google Maps URL", value=est['Google Maps'], key=f"edit_google_{idx}")
                new_password = st.text_input("Dashboard Password", value=est.get('password', ''), type="password", key=f"edit_password_{idx}")
                col_save, col_cancel = st.columns(2)
                with col_save:
                    save = st.form_submit_button("Save")
                with col_cancel:
                    cancel = st.form_submit_button("Cancel")
                if save:
                    st.session_state.establishments[idx] = {
                        'name': new_name,
                        'Booking.com': new_booking,
                        'Expedia': new_expedia,
                        'TripAdvisor': new_tripadvisor,
                        'Google Maps': new_google,
                        'password': new_password
                    }
                    save_establishments(st.session_state.establishments)
                    st.session_state.edit_establishment_idx = None
                    st.success(f"Updated {new_name}")
                    st.rerun()
                if cancel:
                    st.session_state.edit_establishment_idx = None
                    st.rerun()
        else:
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
            with col1:
                st.markdown(f"**{est['name'].strip()}**")
                # Show creator info if available
                if 'created_by' in est and est['created_by']:
                    st.caption(f"👤 Added by: {est['created_by']}")
                elif 'created_at' in est:
                    st.caption(f"📅 Added: {est['created_at']}")
            with col2:
                if st.button("Select", key=f"select_{idx}"):
                    st.session_state.selected_establishment_idx = idx
                    st.session_state.establishment_name = est['name']
                    st.session_state.establishment_urls = est
                    st.rerun()
            with col3:
                if st.button("Edit", key=f"edit_{idx}"):
                    st.session_state.edit_establishment_idx = idx
                    st.rerun()
            with col4:
                if st.button("Delete", key=f"delete_{idx}"):
                    to_delete = idx
    if to_delete is not None:
        del st.session_state.establishments[to_delete]
        save_establishments(st.session_state.establishments)
        if st.session_state.selected_establishment_idx == to_delete:
            st.session_state.selected_establishment_idx = None
            if 'establishment_urls' in st.session_state:
                del st.session_state.establishment_urls
        if st.session_state.edit_establishment_idx == to_delete:
            st.session_state.edit_establishment_idx = None
        st.rerun()
    st.divider()
    # --- Add New Establishment Button and Form ---
    if 'show_add_establishment_form' not in st.session_state:
        st.session_state.show_add_establishment_form = False
    if not st.session_state.show_add_establishment_form:
        if st.button("Add New Establishment", key="show_add_establishment_btn"):
            st.session_state.show_add_establishment_form = True
            st.rerun()
    else:
        with st.form("add_establishment_form", clear_on_submit=True):
            new_name = st.text_input("Establishment Name")
            new_booking = st.text_input("Booking.com URL")
            new_expedia = st.text_input("Expedia URL")
            new_tripadvisor = st.text_input("TripAdvisor URL")
            new_google = st.text_input("Google Maps URL")
            new_password = st.text_input("Dashboard Password", type="password")
            col_add, col_cancel = st.columns(2)
            with col_add:
                submitted = st.form_submit_button("Add Establishment")
            with col_cancel:
                cancel = st.form_submit_button("Cancel")
            if submitted:
                if not new_name:
                    st.warning("Name required.")
                else:
                    # Generate a simple user identifier (you could enhance this)
                    user_id = f"User_{int(time.time()) % 10000}"
                    
                    # Save to global database
                    success = insert_global_establishment(
                        new_name, new_booking, new_expedia, new_tripadvisor, new_google, new_password, user_id
                    )
                    
                    if success:
                        # Refresh establishments from global database
                        st.session_state.establishments = update_local_establishments_from_global()
                        st.success(f"✅ Added '{new_name}' to the global database! It's now available for all users.")
                        st.session_state.show_add_establishment_form = False
                        st.rerun()
                    else:
                        st.error(f"❌ Establishment '{new_name}' already exists in the global database.")
            if cancel:
                st.session_state.show_add_establishment_form = False
                st.rerun()
    st.divider()
    # --- Review Loading UI for Selected Establishment ---
    if st.session_state.selected_establishment_idx is not None:
        est = st.session_state.establishments[st.session_state.selected_establishment_idx]
        st.session_state.establishment_name = est['name']
        st.markdown(f"### Load Reviews for **{est['name'].strip()}**")
        # Check if reviews exist in DB
        db_reviews = fetch_reviews_from_db(est['name'].strip())
        if db_reviews:
            st.info("Loaded historical reviews from database. Use 'Refresh Reviews' to update.")
            df = pd.DataFrame(db_reviews)
            df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
            df = df.sort_values(by='review_date', ascending=False)
            st.session_state.reviews_df = df
            st.session_state.reviews_loaded = True
            st.rerun()
        else:
            st.info("🔑 **Default API credentials are provided!** You can use the app immediately or enter your own API keys if preferred.")
            # Use default credentials silently unless user opts to provide custom ones
            API_TOKEN = DEFAULT_APIFY_API_TOKEN
            st.session_state.openai_api_key = DEFAULT_OPENAI_API_KEY

            with st.expander("Use custom API keys (optional)"):
                col1, col2 = st.columns(2)
                with col1:
                    custom_apify = st.text_input(get_text("apify_token"), type="password", value="", help="Override the default Apify token (optional)")
                with col2:
                    custom_openai = st.text_input(get_text("openai_token"), type="password", value="", help="Override the default OpenAI key (optional)")
                if custom_apify:
                    API_TOKEN = custom_apify
                if custom_openai:
                    st.session_state.openai_api_key = custom_openai
            platforms = [
                ("Booking.com", "voyager~booking-reviews-scraper", normalize_booking_review),
                ("Expedia", "tri_angle~expedia-hotels-com-reviews-scraper", normalize_expedia_review),
                ("TripAdvisor", "maxcopell~tripadvisor-reviews", normalize_tripadvisor_review),
                ("Google Maps", "compass~google-maps-reviews-scraper", normalize_google_review),
            ]
            # Use URLs from selected establishment
            inputs = {name: est.get(name, "") for name, _, _ in platforms}
            if st.button(get_text("load_reviews"), use_container_width=True):
                if not API_TOKEN:
                    st.error(get_text("error_apify_token"))
                elif not st.session_state.openai_api_key:
                    st.error(get_text("error_openai_token"))
                else:
                    all_reviews = []
                    for name, actor_id, normalize_fn in platforms:
                        public_url = inputs[name]
                        if public_url:
                            try:
                                st.write(get_text("triggering_actor").format(name))
                                run_id = trigger_actor(actor_id, API_TOKEN, public_url)
                                st.write(get_text("waiting_run").format(name))
                                run_data = wait_for_run(run_id, API_TOKEN)
                                if run_data["data"]["status"] != "SUCCEEDED":
                                    st.error(get_text("run_failed").format(name))
                                    if "meta" in run_data["data"]:
                                        st.error(get_text("error_details").format(json.dumps(run_data['data']['meta'], indent=2)))
                                    continue
                                dataset_id = run_data["data"]["defaultDatasetId"]
                                st.write(get_text("fetching_reviews").format(name))
                                reviews = fetch_reviews_from_apify(dataset_id, API_TOKEN)
                                if not reviews:
                                    st.warning(get_text("no_reviews_found").format(name))
                                normalized = [r for r in [normalize_fn(r) for r in reviews] if r is not None]
                                all_reviews.extend(normalized)
                            except Exception as e:
                                st.error(get_text("error_fetching").format(name, str(e)))
                                if hasattr(e, 'response'):
                                    try:
                                        error_details = e.response.json()
                                        st.error(get_text("error_details").format(json.dumps(error_details, indent=2)))
                                    except:
                                        st.error(f"Error response: {e.response.text}")
                                else:
                                    st.error(get_text("error_details").format(str(e)))
                    if all_reviews:
                        df = pd.DataFrame(all_reviews)
                        df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
                        df = df.sort_values(by='review_date', ascending=False)
                        st.session_state.reviews_df = df
                        st.session_state.reviews_loaded = True
                        # Save to DB
                        insert_reviews(est['name'].strip(), all_reviews)
                        st.rerun()
    else:
        st.info("Select an establishment to load reviews.")

else:
    # Main review analysis section (dashboard)
    est = st.session_state.establishments[st.session_state.selected_establishment_idx]
    access_key = est['name']
    if not st.session_state.establishment_access.get(access_key, False):
        with st.form(f"password_form_{access_key}"):
            password_input = st.text_input("Enter dashboard password for this establishment", type="password")
            submit_pw = st.form_submit_button("Access Dashboard")
            if submit_pw:
                if password_input == est.get('password', ''):
                    st.session_state.establishment_access[access_key] = True
                    st.success("Access granted.")
                    st.rerun()
                else:
                    st.error("Incorrect password.")
        st.stop()
    df = st.session_state.reviews_df
    
    # --- Dashboard Header with Refresh Button ---
    header_col1, header_col2 = st.columns([6, 1])
    with header_col1:
        st.title(get_text("reviews_title").format(st.session_state.establishment_name))
    with header_col2:
        if st.button('🔄 Refresh', use_container_width=True, key='refresh_top_right'):
            # Get selected establishment
            idx = st.session_state.selected_establishment_idx
            if idx is not None and idx < len(st.session_state.establishments):
                est = st.session_state.establishments[idx]
                st.session_state.establishment_name = est['name']
                
                # Show witty loading message
                with st.spinner("🤖 Tech Guru is finding and analyzing your reviews..."):
                    API_TOKEN = DEFAULT_APIFY_API_TOKEN
                    st.session_state.openai_api_key = DEFAULT_OPENAI_API_KEY
                    platforms = [
                        ("Booking.com", "voyager~booking-reviews-scraper", normalize_booking_review),
                        ("Expedia", "tri_angle~expedia-hotels-com-reviews-scraper", normalize_expedia_review),
                        ("TripAdvisor", "maxcopell~tripadvisor-reviews", normalize_tripadvisor_review),
                        ("Google Maps", "compass~google-maps-reviews-scraper", normalize_google_review),
                    ]
                    inputs = {name: est.get(name, "") for name, _, _ in platforms}
                    all_reviews = []
                    for name, actor_id, normalize_fn in platforms:
                        public_url = inputs[name]
                        if public_url:
                            try:
                                run_id = trigger_actor(actor_id, API_TOKEN, public_url)
                                run_data = wait_for_run(run_id, API_TOKEN)
                                if run_data["data"]["status"] != "SUCCEEDED":
                                    st.error(f"Failed to fetch {name} reviews")
                                    if "meta" in run_data["data"]:
                                        st.error(f"Error details: {json.dumps(run_data['data']['meta'], indent=2)}")
                                    continue
                                dataset_id = run_data["data"]["defaultDatasetId"]
                                reviews = fetch_reviews_from_apify(dataset_id, API_TOKEN)
                                if not reviews:
                                    st.warning(f"No reviews found for {name}")
                                normalized = [r for r in [normalize_fn(r) for r in reviews] if r is not None]
                                all_reviews.extend(normalized)
                            except Exception as e:
                                st.error(f"Error fetching {name}: {str(e)}")
                                if hasattr(e, 'response'):
                                    try:
                                        error_details = e.response.json()
                                        st.error(f"Error details: {json.dumps(error_details, indent=2)}")
                                    except:
                                        st.error(f"Error response: {e.response.text}")
                                else:
                                    st.error(f"Error details: {str(e)}")
                    if all_reviews:
                        df = pd.DataFrame(all_reviews)
                        df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
                        df = df.sort_values(by='review_date', ascending=False)
                        st.session_state.reviews_df = df
                        st.session_state.summary = None
                        st.session_state.report = None
                        st.session_state.filtered_df = None
                        # Delete old reviews and insert new
                        delete_reviews(est['name'].strip())
                        insert_reviews(est['name'].strip(), all_reviews)
                        st.success('✨ Reviews refreshed successfully!')
                        st.rerun()

    # --- Interval Selector for Graph ---
    interval = st.radio(
        'Interval:',
        options=['Month', 'Week'],
        index=0,
        horizontal=True,
        key='graph_interval'
    )

    # Create date range for last 24 months (month) or 6 months (week)
    if interval == 'Week':
        end_date = pd.Timestamp.now()
        start_date = end_date - pd.DateOffset(months=6) + pd.DateOffset(days=1)
    else:
        end_date = pd.Timestamp.now()
        start_date = end_date - pd.DateOffset(months=24) + pd.DateOffset(days=1)

    # Get all reviews for the selected period
    last_period_df = df[
        (df['review_date'] >= start_date) &
        (df['review_date'] <= end_date)
    ]

    # Platform filter for the graph
    all_platforms = sorted(last_period_df['platform'].dropna().unique())
    selected_platforms = st.multiselect(
        'Platforms to include in graph:',
        options=all_platforms,
        default=all_platforms,
        key='graph_platforms'
    )
    filtered_graph_df = last_period_df[last_period_df['platform'].isin(selected_platforms)] if selected_platforms else last_period_df.iloc[0:0]

    # --- Grouping logic for interval ---
    if interval == 'Month':
        grouped = filtered_graph_df.groupby(filtered_graph_df['review_date'].dt.to_period('M'))['star_rating'].mean().reset_index()
        grouped['review_date'] = grouped['review_date'].astype(str)
        # Create a complete dataframe with all 24 months
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')  # Month Start
        complete = pd.DataFrame({
            'review_date': [d.strftime('%Y-%m') for d in date_range],
            'interval_label': [f"{translate_month(d.strftime('%B'))} {d.strftime('%Y')}" for d in date_range]
        })
        merged = complete.merge(grouped, on='review_date', how='left').fillna(0)
        merged['hover'] = merged['interval_label']
    else:  # Week
        grouped = filtered_graph_df.groupby(filtered_graph_df['review_date'].dt.to_period('W'))['star_rating'].mean().reset_index()
        grouped['week_start'] = grouped['review_date'].apply(lambda p: p.start_time)
        grouped['review_date'] = grouped['week_start'].dt.strftime('%Y-%m-%d')
        # Create a complete dataframe with all weeks in the last 6 months
        week_range = pd.date_range(start=start_date, end=end_date, freq='W-MON')  # Weeks start on Monday
        complete = pd.DataFrame({
            'review_date': [d.strftime('%Y-%m-%d') for d in week_range],
            'interval_label': [d.strftime('%Y-%m-%d') for d in week_range],  # Use week start date as label
            'week_start': week_range
        })
        merged = complete.merge(grouped[['review_date', 'star_rating']], on='review_date', how='left')
        merged['star_rating'] = merged['star_rating'].fillna(0)
        merged['hover'] = merged['week_start'].dt.strftime('Week of %Y-%m-%d')

    # Add color based on rating thresholds
    merged['color'] = merged['star_rating'].apply(
        lambda x: 'green' if x >= 4.5 else ('yellow' if x >= 4 else 'red')
    )

    # Create the bar graph
    st.markdown(f"### {get_text('last_24_months')}")
    fig = px.bar(
        merged,
        x='interval_label',  # Use week start date as bar
        y='star_rating',
        color='color',  # Color based on rating thresholds
        color_discrete_map={
            'green': '#2ecc71',  # Green for ≥ 4.5
            'yellow': '#f1c40f',  # Yellow for 4-4.5
            'red': '#e74c3c'  # Red for < 4
        },
        labels={'interval_label': get_text('month'), 'star_rating': get_text('average_rating')},
        title=get_text('graph_title'),
        hover_data={'hover': True, 'star_rating': True, 'interval_label': False, 'color': False}
    )
    # Custom hover template
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Average Rating: %{y:.2f}')

    # Update layout
    fig.update_layout(
        xaxis_title=get_text('month'),
        yaxis_title=get_text('average_rating'),
        yaxis_range=[0, 5],  # Rating scale from 0 to 5
        hovermode='x unified',
        showlegend=False,
        bargap=0.2,  # Add some space between bars
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=merged['interval_label'].tolist(),
            tickangle=45
        ),
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    # Format x-axis to show week start date for each week, or month for month interval
    if interval == 'Week':
        fig.update_xaxes(
            tickmode='array',
            ticktext=merged['interval_label'].tolist(),
            tickvals=merged['interval_label'].tolist()
        )
    else:
        fig.update_xaxes(
            tickmode='array',
            ticktext=merged['interval_label'].tolist(),
            tickvals=merged['interval_label'].tolist()
        )

    # Display the graph
    st.plotly_chart(fig, use_container_width=True)

    # Date range and platform filter for reviews table and stats
    st.markdown(f"### {get_text('filter_reviews')}")
    col1, col2 = st.columns(2)
    with col1:
        new_start_date = st.date_input(get_text("start_date"), value=pd.Timestamp.now() - pd.Timedelta(days=30))
    with col2:
        new_end_date = st.date_input(get_text("end_date"), value=pd.Timestamp.now())
    # Platform filter for table/stats
    def clear_ai_responses():
        if 'summary' in st.session_state:
            del st.session_state.summary
        if 'report' in st.session_state:
            del st.session_state.report
    all_table_platforms = sorted(df['platform'].dropna().unique())
    selected_table_platforms = st.multiselect(
        'Platforms to include in table/stats:',
        options=all_table_platforms,
        default=all_table_platforms,
        key='table_platforms',
        on_change=clear_ai_responses
    )

    # Update session state with new dates only
    st.session_state.start_date = new_start_date
    st.session_state.end_date = new_end_date

    # Filter reviews based on date range and platform
    mask = (
        (df['review_date'].dt.date >= st.session_state.start_date) &
        (df['review_date'].dt.date <= st.session_state.end_date) &
        (df['platform'].isin(selected_table_platforms))
    )
    filtered_df = df.loc[mask]
    st.session_state.filtered_df = filtered_df

    # Calculate and display platform statistics
    st.subheader(get_text("review_statistics"))
    
    # Get unique platforms in the filtered data
    platforms = filtered_df['platform'].unique()
    
    # Create columns for the statistics
    cols = st.columns(len(platforms) + 1)  # +1 for overall stats
    
    # Calculate and display stats for each platform
    platform_stats = {}
    for i, platform in enumerate(platforms):
        platform_df = filtered_df[filtered_df['platform'] == platform]
        avg_rating = platform_df['star_rating'].mean()
        review_count = len(platform_df)
        platform_stats[platform] = {'avg_rating': avg_rating, 'count': review_count}
        
        # Display platform stats with custom styling
        with cols[i]:
            st.markdown(f"### {platform}")
            st.markdown(f"<h2 style='margin: 0;'>{avg_rating:.1f} ⭐</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #666; margin: 0;'>{review_count:,} {get_text('reviews')}</p>", unsafe_allow_html=True)
    
    # Calculate and display overall stats
    if platform_stats:
        overall_avg = sum(stat['avg_rating'] * stat['count'] for stat in platform_stats.values()) / sum(stat['count'] for stat in platform_stats.values())
        total_reviews = sum(stat['count'] for stat in platform_stats.values())
        
        # Display overall stats with custom styling
        with cols[-1]:
            st.markdown(f"### {get_text('overall')}")
            st.markdown(f"<h2 style='margin: 0;'>{overall_avg:.1f} ⭐</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #666; margin: 0;'>{total_reviews:,} {get_text('reviews')}</p>", unsafe_allow_html=True)
    
    # Add a divider for visual separation
    st.divider()
    
    # Action buttons in a row
    col1, col2, col3 = st.columns(3)
    with col1:
        # Check date range only when generating summary
        date_range = st.session_state.end_date - st.session_state.start_date
        if date_range.days > 365:
            st.warning(get_text("summary_warning"))
        if st.button(get_text("generate_summary"), use_container_width=True, disabled=date_range.days > 365):
            generate_summary(filtered_df, st.session_state.start_date, st.session_state.end_date, st.session_state.openai_api_key)
    with col2:
        if st.button(get_text("report_review"), use_container_width=True, disabled=date_range.days > 365):
            generate_report(filtered_df, st.session_state.start_date, st.session_state.end_date, st.session_state.openai_api_key)
    with col3:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label=get_text("download_csv"),
            data=csv,
            file_name="reviews.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Display the filtered reviews
    st.subheader(get_text("review_table"))
    
    st.dataframe(
        filtered_df,
        hide_index=True,
        column_config={
            "review_text": st.column_config.TextColumn(
                get_text("review_text"),
                width="large",
                help=get_text("review_text_help"),
            ),
            "review_date": st.column_config.DateColumn(
                get_text("review_date"),
                format="YYYY-MM-DD",
            ),
            "star_rating": st.column_config.NumberColumn(
                get_text("rating"),
                format="%.1f ⭐",
            ),
            "platform": st.column_config.TextColumn(
                get_text("platform"),
                width="medium",
            ),
            "reviewer_name": st.column_config.TextColumn(
                get_text("reviewer"),
                width="medium",
            ),
            "replied": st.column_config.CheckboxColumn(
                get_text("replied"),
                width="small",
            ),
        },
        use_container_width=True,
    )
    
    # Display summary if available
    if 'summary' in st.session_state and st.session_state.summary:
        st.markdown(f"### {get_text('ai_summary')}")
        st.write(st.session_state.summary)
    
    # Display report if available
    if 'report' in st.session_state and st.session_state.report:
        st.markdown(f"### {get_text('ai_report')}")
        st.write(st.session_state.report)