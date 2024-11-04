# Prioritizing Vociemail using Sentiment and Emotional Analysis

In modern communication systems, voicemail serves as a vital tool for leaving messages when direct communication is not possible. However, the conventional method of voicemail prioritization often leads to critical messages being buried under non-urgent ones, potentially causing delays in addressing emergencies. This problem becomes even more pronounced when the volume of voicemails increases, resulting in a backlog that impedes timely response to urgent matters.

Problem Statement - 
The existing voicemail system lacks the capability to differentiate between urgent and non-urgent messages, leading to delays in addressing critical issues. Messages are typically processed in a first-in-first-out (FIFO) manner, meaning that even if an emergency voicemail arrives later, it may remain unattended at the bottom of the queue until all preceding messages are addressed. This delay can have serious consequences, especially in situations where immediate action is required, and another solution is through NLP and Audio signal processing by reading the transcription of the voicemail and then applying algorithms to understand the seriousness of the voicemail and then assign priority. 

Proposed Solution - 
We have implemented a system that automatically analyzes incoming voicemails for emotional and sentiment indicators. 
By leveraging advanced natural language processing (NLP) and machine learning techniques, the system can identify voicemails that convey urgency, frustration, or other critical emotions.
Once a critical voicemail is detected, the system will immediately send a targeted email notification to the relevant recipient.

![image](https://github.com/user-attachments/assets/63b46012-bd0e-428b-a338-305426a1724b)

#Tech stack and Libraries
Python
Whisper
Hugging face – Transformers
Joblib
Librosa -> MFCC 
Numpy , Pandas
SMTPLib -> Email Services

#Benefits
Timely response
Improved customer satisfaction 
Increased efficiency
Reduced risk

DATA SET - RAVDESS (Ryerson Audio-Visual Database of Emotional Speech and Song)
![image](https://github.com/user-attachments/assets/2c2006a5-5507-4c98-bcbe-d84d7c707968)
