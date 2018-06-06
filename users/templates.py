
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def verificationEmail(user_name, otp, href):

    button_style= "text-align: center; display: inline-block; padding: 10px; font-size: 14px; margin-bottom: 5px; width: 150px; color: #FFFFFF; background-color: #3FCB75; border-radius: 4px; text-transform: uppercase; font-weight: 500; text-decoration: none; transition: box-shadow 200ms ease-out;"
    div_style = "margin: 0 auto; width:80%; text-align:left; background-color:white; padding:24px; font-size: 1.1em; color:black"
    body_style= "background-color:#EEEEEE; height:60vh; padding:24px"
    parent_div_style = "background-color:#EEEEEE; padding:24px;"
    html = """\
    <html>
      <head></head>
      <body style={body_style}>
          <div style="{parent_div_style}">
            <div style="{div_style}">
                <p>Hi {user_name},</p>
                <p>Thank you for signing up with us! Click below to verify your e-mail.</p>
                <a href={href} style="{button_style}">Verify Email</a><br>
                If you have trouble opening it in your browser, please copy and paste the link below:<br>
                {href}
                <p>Thank You</p>
                <p>Mess Feedback System Team</p>
            </div>
          </div>
      </body>
    </html>
    """.format(user_name=user_name, href=href, button_style=button_style, div_style=div_style, body_style=body_style,parent_div_style=parent_div_style)

    return html

def forgetOtp(user_name, otp):

    div_style = "margin: 0 auto; width:80%; text-align:left; background-color:white; padding:24px; font-size: 1.1em; color:black"
    body_style= "background-color:#EEEEEE; height:60vh; padding:24px"
    parent_div_style = "background-color:#EEEEEE; padding:24px;"

    html = """\
    <html>
      <head></head>
      <body style={body_style}>
          <div style="{parent_div_style}">
            <div style="{div_style}">
                <p>Hi {user_name},</p>
                Your OTP for changing the password is <b>{otp}</b>:<br>
                Copy this otp and use it for changing your password
                <p>Thank You</p>
                <p>Mess Feedback System Team</p>
            </div>
          </div>
      </body>
    </html>
    """.format(otp=otp, user_name=user_name, div_style=div_style, body_style=body_style,parent_div_style=parent_div_style)

    return html
