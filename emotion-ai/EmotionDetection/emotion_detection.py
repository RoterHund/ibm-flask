import requests
import json

def extract_emotion_scores(formatted_response):
    if formatted_response.status_code == 200:
        emotion_predictions = formatted_response.json()['emotionPredictions'][0]['emotion']
        return {
            'anger': emotion_predictions.get('anger', None),
            'disgust': emotion_predictions.get('disgust', None),
            'fear': emotion_predictions.get('fear', None),
            'joy': emotion_predictions.get('joy', None),
            'sadness': emotion_predictions.get('sadness', None)
        }
    else:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None
        }

def calculate_dominant_emotion(emotion_scores):
    valid_emotion_scores = {k: v for k, v in emotion_scores.items() if v is not None}
    if valid_emotion_scores:
        return max(valid_emotion_scores, key=lambda k: valid_emotion_scores[k])
    else:
        return None

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = {"raw_document": {"text": text_to_analyze}}
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    response = requests.post(url, json=myobj, headers=header)
    
    if not text_to_analyze or response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    formatted_response = json.loads(response.text)
    if response.status_code == 200:
        emotion_predictions = formatted_response.get('emotionPredictions', [])
        if emotion_predictions:
            dominant_emotion = max(emotion_predictions[0].get('emotion', {}), key=emotion_predictions[0].get('emotion', {}).get)
            return {
                'anger': emotion_predictions[0]['emotion'].get('anger'),
                'disgust': emotion_predictions[0]['emotion'].get('disgust'),
                'fear': emotion_predictions[0]['emotion'].get('fear'),
                'joy': emotion_predictions[0]['emotion'].get('joy'),
                'sadness': emotion_predictions[0]['emotion'].get('sadness'),
                'dominant_emotion': dominant_emotion
            }

    return {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }


# Example usage
# print(emotion_detector("I love this new technology"))
