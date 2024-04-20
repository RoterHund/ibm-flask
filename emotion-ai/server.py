"""
Flask application for sentiment analysis.

Executing this function initiates the application of sentiment
analysis to be executed over the Flask channel and deployed on
localhost:5000.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def sent_analyzer():
    '''
    This code receives the text from the HTML interface and 
    runs dominant emotion analysis over it using emotion_detector()
    function. The output returned shows the emotion scores and the
    dominant emotion.
    '''
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)
    dominant_emotion = response['dominant_emotion']
    if dominant_emotion is None:
        return "Invalid text! Please try again."

    # Extract emotion scores
    emotion_scores = response.copy()
    del emotion_scores['dominant_emotion']
    emotion_scores_str = ', '.join([f"'{k}': {v}" for k, v in emotion_scores.items()])

    # Format the response
    return f"For the given statement, the system response is {emotion_scores_str}. The dominant emotion is {dominant_emotion}."


@app.route("/")
def render_index_page():
    '''
    This function initiates the rendering of the main application
    page over the Flask channel.
    '''
    return render_template('index.html')

if __name__ == "__main__":
    # Execute the Flask app and deploy it on localhost:5000.
    app.run(host="0.0.0.0", port=5000)
