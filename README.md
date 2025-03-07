# What does EmailVer do?
This program verifies the email and check it's authenticity by classifying it as suspicous or not...

# What does listEmail do?
- This program lists the email with . variances and + aliases that can usually seem harmless but are used by potential attackers.
- One may put these on Gmail Alerts to get alerted if someone misuses such aliases

# Running the programs
- Clone the repository:
  <br></br>
  ```
  git clone https://github.com/Joshni86/Email_verification.git
  ```
- cd Email_verification
- Install the module: dnspython
  <br></br>
  ```
  pip install dnspython
  ```
- Now run the file you want by either clicking the play button if you're using VS code or by pasting the following in your terminal
  <br></br>
  ```
  python listEmail.py
  ```
  or
  <br></br>
  ```
  python EmailVer.py
  ```    
