import streamlit as st
import validators
from scrape import (
    scrape_website,
    scrape_website_with_proxy,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_openai

# Streamlit UI
st.title("Web scraping avec l'IA")
url = st.text_input("Entrez l'URL du site web")

# Option to use proxy
use_proxy = st.checkbox("Utiliser un proxy pour le scraping")

# Step 1: Scrape the Website
if st.button("Lancer le scraping"):
    if url:
        if validators.url(url):
            st.write("Le scraping est en cours...")

            # Scrape the website with or without proxy
            dom_content = scrape_website_with_proxy(url) if use_proxy else scrape_website(url)

            if not dom_content:
                st.error("Une erreur s'est produite lors du scraping. Veuillez vérifier l'URL et réessayer.")
            else:
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display the DOM content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
        else:
            st.error("L'URL fournie n'est pas valide. Veuillez entrer une URL correcte.")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Décrivez ce que vous souhaitez extraire.")

    if st.button("Extraire le contenu"):
        if parse_description:
            st.write("Extraction du contenu en cours...")

            # Parse the content with OpenAI
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_openai(dom_chunks, parse_description)
            st.write(parsed_result)
