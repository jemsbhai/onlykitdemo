from supabase import create_client, Client
from ttslib import speakout
from sttlib import transcribe_audio, record_audio
import spacy
import re

# Supabase configuration
# Supabase credentials
SUPABASE_URL = "https://kncehtefkgupllwygfxx.supabase.co/"
SUPABASE_KEY = "KEYHERE"  # Replace with your actual key
##insecure

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)




# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

import re

def extract_tag(text: str) -> str:
    """
    Extracts a license plate/tag number from a transcribed sentence.
    This version merges separated alphanumeric segments like '7 ABC 100'.
    """

    # Clean and tokenize
    tokens = re.findall(r'[A-Za-z0-9]+', text.upper())

    # Remove common command words
    skip_words = {"CHECK", "TAG", "LOOKUP", "FIND", "PLATE"}
    filtered_tokens = [t for t in tokens if t not in skip_words]

    # Try to join adjacent parts into a plate-like string
    combined = ''.join(filtered_tokens)

    # Match something that looks like a license plate (5–8 alphanumerics)
    match = re.match(r'^[A-Z0-9]{5,8}$', combined)
    if match:
        return combined

    # Fallback: scan for partial match in sequence
    for i in range(len(filtered_tokens)):
        for j in range(i+1, len(filtered_tokens)+1):
            candidate = ''.join(filtered_tokens[i:j])
            if 5 <= len(candidate) <= 8:
                return candidate

    return ""


def get_vehicle_info_by_plate(plate_number: str) -> str:
    try:
        response = (
            supabase.table("Sample_Plates_All_Fake_Data")
            .select("plate, year, make, model, status")
            .eq("plate", plate_number)
            .execute()
        )

        if response.data:
            data = response.data[0]
            return f"The requested tag is a {data['year']} {data['make']} {data['model']}, currently marked as {data['status']}."
        else:
            return f"The requested tag '{plate_number}' was not found in the database."

    except Exception as e:
        return f"An error occurred while retrieving the tag: {str(e)}"

if __name__ == "__main__":
    print("🎙️ Listening for tag...")
    audio_file = record_audio(duration=5)
    transcribed_text = transcribe_audio(audio_file)
    print("Transcribed Text:", transcribed_text)

    tag = extract_tag(transcribed_text)
    if tag:
        print("Detected Tag:", tag)
        vehicle_description = get_vehicle_info_by_plate(tag)
    else:
        vehicle_description = "I couldn't understand the tag number clearly. Please try again."

    print("Speaking:", vehicle_description)
    speakout(vehicle_description)
