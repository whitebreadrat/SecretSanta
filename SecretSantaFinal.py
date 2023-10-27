import smtplib
import random
import pandas as pd


# Enter your email and password for the sender's email account
sender_email = "sending email address"
password = "email password"

# Read participant data from the CSV file

df=pd.read_csv('secret_santa.csv')
participants = list(df.columns.values)
fb1 = df.loc[0,:].tolist() #list of last years partner, no repeats
fb2 = df.loc[1,:].tolist() #list of husband/wife, etc for removal
email = df.loc[2,:].tolist() #list of email addresses

receivers = []
for i in range(0, len(participants)):
    p1 = participants.copy()
    del p1[i]
    p1.remove(fb1[i])
    p2 = fb2[i] 
    if p2 in p1:
        p1.remove(fb2[i])
    p1
    receivers.append(p1)

taken = []                      # For keeping track of who has been assigned to a 'giver'.
pairings = {}                   # Dictionary for giver-to-receiver pairings.
 
start = random.choice(receivers[0])
taken.append(start)
pairings[participants[0]] = start
 
while len(taken) < len(participants):
    for i in range(1,len(participants)):
        possible = receivers[i]
        try:
            possible = [x for x in possible if x not in taken]
            chosen = random.choice(possible)
            taken.append(chosen)
            pairings[participants[i]] = chosen
        except:
            taken = [taken[0]]
            break
 
#for k,v in pairings.items():
#    print('%s gives a gift to %s.' % (k,v)) #Hey, don't peek!
# Send email to each participant with their assigned pick

n=0    #an incrementer for the email
for giver in pairings:
    giver_name = giver
    receiver_name = pairings[giver]
    email_address = email[n]
    message = f"Subject: Secret Santa Selection \n\nHello {giver_name}!\n\nYou are assigned to be the Secret Santa for {receiver_name} this year."
#    message = f'Subject: SECRET SANTA TEST EMAIL \n\nHello {giver_name}!\n\nYou are not yet assigned to be the Secret Santa for anybody this year.' #test email
#    print(message) #pieces for testing
#    print(email_address) #pieces for testing
    n=n+1

    # Connect to the email server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, email_address, message)
    server.quit()

    print(f"Email sent to {giver_name} ({email_address}) with their assigned pick.")
#generate a new input file with the selections for this round.
outputdf = pd.DataFrame(list(zip(participants, newold, fb2, email))).T
outputdf.to_csv('output.csv', index = False, header = False)

