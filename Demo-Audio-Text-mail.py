import ftplib
import os
import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from transformers import pipeline # For Sentiment Analysis

# Email details
sender_email = "ABCD@gmail.com" # Add sender's email
receiver_email = "XYZ@gmail.com" # Add Receiver's email
password = "XXXXXXXXXXX" # Give your password

#function for predicting emotion - Chandan
def predict_emotion(file_path, model_filename="emotion_svm_model.joblib"):
    # Load the saved model
    model = joblib.load(model_filename)
    features = extract_features(file_path)  # Extract features
    features = features.reshape(1, -1)      # Reshape for prediction
    prediction = model.predict(features)     # Predict emotion
    return prediction[0]                     # Return the predicted emotion

#function for detecting final result
def classify_emotion_sentiment(emotion, sentiment):
    # Defining the conditions for each classification
    if emotion == 'angry' and sentiment == 'negative':
        return 'very critical'
    elif emotion == 'angry' and sentiment == 'neutral':
        return 'critical'
    elif emotion == 'angry' and sentiment == 'positive':
        return 'moderately critical'
    elif emotion == 'neutral' and sentiment == 'negative':
        return 'somewhat critical'
    elif emotion == 'neutral' and sentiment == 'neutral':
        return 'neutral'
    elif emotion == 'neutral' and sentiment == 'positive':
        return 'mildly positive'
    elif emotion == 'happy' and sentiment == 'negative':
        return 'conflicting but calm'
    elif emotion == 'happy' and sentiment == 'neutral':
        return 'positive but reserved'
    elif emotion == 'happy' and sentiment == 'positive':
        return 'neutral'
    else:
        return 'unknown'

def send_urgent_email(sender_email, receiver_email, password, file_path):
    subject = "Urgent mail notification"
    body = ''
    
    # Read the email body from the file
    with open(file_path, 'r') as file:
        body = file.read()

    # Clean up the email body by removing text between square brackets
    flag = 1
    result = ''
    for ch in body:
        if ch == '[':
            flag = 0
        elif ch == ']':
            flag = 1
        elif flag:
            result += ch

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add the cleaned body to the email
    message.attach(MIMEText(result, "plain"))

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        print(f"Sending mail to: {receiver_email}")
        print(f"e-mail: {result}")
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

while True:

    print("FTP: Login")
    ftp = ftplib.FTP("111.111.111.111") # Add your voicemail server IP
    ftp.login("admin", "Password") # Add your username and password for voicemail server
    #ftp.cwd('/home/mivo400/voice/vm/mbox13')
    ftp.cwd('/home/mivo400/voice/vm/mbox21') # Add Path to your voiemail files
    filenames = ftp.nlst()

    for filename in filenames:
        #print('Enter: for loop !!!!')
        #print(filename)

        # removing the unwanted spaces from the file name
        filename = filename.replace(" ", "")
        #print("file:",filename)
        #print("dir:",os.getcwd())
        time.sleep(20)

        with open( filename, 'wb' ) as file :
            ftp.retrbinary('RETR %s' % filename, file.write)
            ftp.cwd('/home/mivo400/voice/vm/mbox21')

            #convert wave file to 16-bit, 16-khz format
            os.chdir('/home/miteladmin/')
            cmd = 'ffmpeg -i '
            cmd += filename
            cmd += ' -acodec pcm_s16le -ar 16000 '
            cmd += '/home/miteladmin/whisper.cpp/samples/'
            cmd += filename

            print("dir:", os.getcwd())
            print("File:", filename)
            #print(cmd)
            os.system(cmd)


            os.chdir('/home/miteladmin/whisper.cpp/')
            #print(os.getcwd())

            #convert wave file to text file
            speechtotext = './main -f '
            speechtotext += 'samples/'
            speechtotext += filename
            speechtotext += ' > '
            speechtotext += '/home/miteladmin/sendmail.txt'

            #sentiment detection - Chandan

            sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            sentiment_pipeline = pipeline("sentiment-analysis", model=sentiment_model_name)
            
            content = read_file_content('/home/miteladmin/sendmail.txt')

            result = sentiment_pipeline(content)

            print(result[0]['label'])

            predicted_sentiment = result[0]['label']

            #Emotion detection - Chandan

            voicemail_audio_file = r'/home/mivo400/voice/vm/mbox21'  # Replace with your proper audio file path
            predicted_emotion = predict_emotion(voicemail_audio_file)
            print(f'The predicted emotion is: {predicted_emotion}')

            classification = classify_emotion_sentiment(predicted_emotion, predicted_sentiment)

            #print(speechtotext)
            os.system(speechtotext)

            #Not sure what is happening between 176 to 185 -- Do we really need
            os.chdir('/home/miteladmin/whisper.cpp/samples/')
            #print("dir:", os.getcwd())
            #print("Deleting file:", filename)
            os.remove(filename)

            os.chdir('/home/miteladmin/')
            #print("dir:", os.getcwd())
            #print("Deleting file:", filename)
            os.remove(filename)

            if classification in ['critical', 'very critical']:
                sender_email = "ABCD@gmail.com"
                receiver_email = "XYZ80@gmail.com"
                password = "Password"
                file_path = '/home/miteladmin/sendmail.txt'
                send_urgent_email(sender_email, receiver_email, password, file_path)


        #print('Exit: for loop !!!!')

    time.sleep(5)
    #print("FTP: Logout")
    ftp.quit()
