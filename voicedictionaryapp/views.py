import requests
from django.shortcuts import render
from django.http import HttpRequest
import logging

logging.basicConfig(level=logging.INFO)

DICTIONARY_API_BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def home(request):
    word = request.GET.get('wordinput', '').strip().lower()

    context = {'word': word, 'word_data': None} 

    if not word:
        return render(request, 'home.html', context)

    try:
        api_url = f"{DICTIONARY_API_BASE_URL}{word}"
        response = requests.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        
        if isinstance(data, list) and data:
            entry = data[0]
            
            phonetics_text = entry.get('phonetic', 'N/A')
            
            structured_meanings = []
            
            for meaning in entry.get('meanings', []):
                part_of_speech = meaning.get('partOfSpeech', 'N/A')
                definitions_list = []
                
                
                for definition_data in meaning.get('definitions', []):
                    definitions_list.append({
                        'definition': definition_data.get('definition', 'Definition not available.'),

                        'example': definition_data.get('example', None) 
                    })

                
                if definitions_list:
                    structured_meanings.append({
                        'part_of_speech': part_of_speech,
                        'definitions': definitions_list 
                    })

            
            context['word_data'] = { 
                'word': word,
                'phonetics': phonetics_text,
                'meanings': structured_meanings 
            }
            logging.info(f"Successfully processed {len(structured_meanings)} meanings for word: {word}")

        elif isinstance(data, dict) and data.get('title') == 'No Definitions Found':
            context['word_data'] = {'error': f"Sorry, we couldn't find the word '{word}'. Please check the spelling or try another word."}
            logging.warning(f"No definitions found for word: {word}")

        else:
             context['word_data'] = {'error': f"An unexpected API response structure was received for '{word}'."}
             logging.error(f"Unexpected API response structure for word: {word}")

    except requests.exceptions.HTTPError as e:
        context['word_data'] = {'error': f"HTTP Error: Could not retrieve definitions for '{word}'. Status Code: {e.response.status_code}"}
        logging.error(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError:
        context['word_data'] = {'error': "Connection Error: Could not reach the dictionary service. Check your internet connection."}
        logging.error("Connection Error during API call.")
    except Exception as e:
        context['word_data'] = {'error': f"An unknown error occurred while processing the request for '{word}'. Error: {e}"}
        logging.error(f"Unknown error: {e}", exc_info=True)

    return render(request, 'home.html', context)
