# Importing speech2text from prev definition
from .speech2textv2 import speech2text
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
 # testing with doctor.wav
# print(conversation_array)

# Generating Transcript + Finding Key Words
def transcript_gen():
	"""
	Void function that creates Transcript File
	________________________________
	Args: Conversation Array (2D ex: [["word", speaker_idx]])
	Returns: transcripts.txt file, blood_pressure, heart_rate
	"""

	print("converting to transcript")
	speech = os.path.join("/Users/shubhamkumar/Desktop/git-repos/kronos", "new_doctor.wav")

	conversation_array = speech2text(speech)

	# Final Transcript Intialization
	final = []
	string = ""
	doc_num = conversation_array[0][1]
	#print(len(conversation_array))

	# Determines index of the patient assuming doctor speaks first
	for i in range(len(conversation_array)):
		if(conversation_array[i][1] != doc_num):
			 pat_num = conversation_array[i][1]
	# print(doc_num, pat_num)

	# Creates an array based on speakers
	for i in range(len(conversation_array)):
		# print(conversation_array[i][1])
		if(i == 0):
			string = conversation_array[0][0]
		if(i != 0 and  conversation_array[i][1] == conversation_array[i-1][1]):
			string += " "
			string += conversation_array[i][0]
		if(i != 0 and conversation_array[i][1] != conversation_array[i-1][1]):
			final.append(string)
			string = ""

	# Important comments made by doctor
	log = []

	final.append(string)

	# File Handling
	with open("transcript.txt", 'w') as f:
		#creating transcript
		f.write('TRANSCRIPT')
		f.write('\n___________')

		bloodpres, heartrate = 0, 0

		# Writing the transcript to file
		for i in range(len(final)):
			if(final[i].split(' ')[0] == "log"):
				log.append(final[i])
				if("blood pressure" in str(final[i].lower())):
					bloodpres = re.findall(r'^[-+]?[0-9]+$', str)
				elif("heart rate" in str(final[i].lower())):
					heartrate = re.findall(r'^[-+]?[0-9]+$', str)
			if(i % 2 == 0 ):
				final[i] = "\nDoctor: " + final[i]
				f.write(final[i])
			if(i % 2 == 1):
				final[i] = "\nPatient: " + final[i]
				f.write(final[i])

		# Writing the logs to file
		f.write('\nLOG')
		f.write('\n___________')
		for i in range(len(log)):
			f.write(log[i] + "\n")

	f.close()

	metrics = [bloodpres, heartrate]
	print(metrics)
	return metrics



pswd = open('pswd_IGNORE.txt','r').read().strip().split("\n")
gmail_user = pswd[0]
gmail_psd = pswd[1]
#gmail_password = pswd.readline().strip()

#send email to pharmacy
def send_email():
    #try:
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    server.login(gmail_user, gmail_psd)#gmail_password)
    #except Exception as e:
    #    print(e)

    sent_from = gmail_user
    to = "kumar.shubham5504@gmail.com"
    #name = i[1]+" "+i[2]
    subject = "Prescription from Dr. Kavin"
    #print(data)
    #print(data[name])
    body = 'Dear Pharmacist Shubham,\n\n'+'Please prepare (3 mg of Ibuprofen) for a patient of mine.\nThanks,\n'+'Dr. Kavin'
    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

    try:
        #msg = createMessage(subject, body)
        server.sendmail(sent_from, to, email_text)
        #print('Email sent!')
    except Exception as e:
        print(e)
    server.close()
# Testing

# transcript_gen([['log', 0], ['blood', 0], ['pressure', 0 ], ['80', 0]])
if __name__ == "__main__":
	logs = transcript_gen()
	send_email()
	#print(logs)
