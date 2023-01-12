import os
import platform 
import pandas as df 
import smtplib  # for emailing section
import ssl  # for emailing section
from email.mime.text import MIMEText  # for emailing section
from email.mime.multipart import MIMEMultipart  # for emailing section
import functools  # for cmd terminal buffer flushing to allow rapid print of "." on same line

# This removes buffering done by windows CMD terminal to allow for the multiple fast prints of "." in the for-loop
# We are printing "." in the for-loop for each ping to show the script is busy working in terminal. This is not critical
print = functools.partial(print, flush=True)

# read CSV file using "Pandas" module
# "Device_IP_List.csv" is your input csv file here. Name it whatever your csv is. NB: the IP addresses must be in a column named 'IP'
device_ip_list = df.read_csv("Device_IP_List.csv")   
# load CSV into new data frame
df_device_ip_list = df.DataFrame(device_ip_list)

# Add new empty column to df called "Result"
df_device_ip_list["Result"] = ''

# load windows platform/system/cmd-prompt so can use it with ping cmds
plat = platform.system()

for index, row in df_device_ip_list.iterrows():  # to apply below ping cmd in an if-loop per row in the DF

    response = os.system("ping -n 1 " + row['IP'] + ">null")  #ping CMD. NB: the IP addresses must be in a column named 'IP'

    if response == 0:
        print(".", end='')  # this is used to show script is busy in the windows CMD terminal
        df_device_ip_list.loc[index, 'Result'] = 'pass'
    else:
        print(".", end='')  # this is used to show script is busy in the windows CMD terminal
        df_device_ip_list.loc[index, 'Result'] = 'fail'

print('\n')  # adding blank line in terminal after all the "..........."

#Creating csv output for our info incase email output is not working.
#df_device_ip_list.to_csv('csv_device_ip_list.csv')

# filter rows with result of ping 'fail' in 'Result' column and create new DF with only failed devices
true_or_false_bool_pingfail = df_device_ip_list['Result'] == 'fail'  # bool ouput = True/ False depending on "Result" = 'fail'
ping_fail_df = df_device_ip_list[true_or_false_bool_pingfail]  # creates df using filtered rows according to bool True

# filter rows with result of ping 'pass' in 'Result' column and create new DF with only passed devices
true_or_false_bool_pingpass = df_device_ip_list['Result'] == 'pass'  # bool ouput = True/ False depending "Result" = 'pass'
ping_pass_df = df_device_ip_list[true_or_false_bool_pingpass]  # creates df using filtered rows according to bool TRUE

#Append both "fail" DF and "pass" DF so that new DF has both conditions but failed devices are on top.
sorted_ping_results_df = ping_fail_df.append(ping_pass_df, ignore_index=True)

#Creating csv output for debug from processed DF.
sorted_ping_results_df.to_csv('sorted_ping_results_df')

print('*sorted DF complete')

print('*sending email')

# Email module below
##########################################
# Define email sender and receiver
sender_email = 'email@gmail.com' #the email address you are sending from
password = 'xxxxxxxxxxxxxxxx'  # this is the 16 char long app code found in your gmail sender acc settings (gmail method working in 2023)
receiver_email = ['email-1@gmail.com', 'email-2@gmail.com', ]   #whoever you are sending the email to

# Set the subject and body of the email
message = MIMEMultipart('alternative')  # 'alternative' is used in MIME to force HTML into body, not as attachment
message["Subject"] = "**Ping Response Snapshot"  #write whatever you want in the " "
message["From"] = sender_email
message["To"] = ", ".join(receiver_email)  # receiver_email

text = """\

"""

html = """\
<html>
  <head>
    <br></br>
        <b> One-shot ping report. Any failed pings will show at the top </b>  #some body text
    <br></br>
  </head>
  <body>
    {0}
  </body>
</html>
""".format(sorted_ping_results_df.to_html())  #putting your df table into html in the body of email

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)

# Send email with SSL
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

#######################################################
print('*email sent')
