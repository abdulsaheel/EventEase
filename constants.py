# Add a hardcoded username and password (in practice, use a database or atleast .env file)
ADMIN_USERNAME = 'admin123'
ADMIN_PASSWORD = 'password123'

#DATABASE URL
DATABASE_URL='postgresql://username:password@hostname:port/database_name'
#you can get free db here: https://console.neon.tech/


#PhonePe Production credentials 
#You will recieve these credentials in mail and reminder use only configured domain not testing urls or tunnels 
#Below details are for testing
merchant_id = "PGTESTPAYUAT86"
salt_key = "96434309-7796-489d-8924-ab56988a6076"
salt_index = 1
host_url="https://api-preprod.phonepe.com/apis/hermes"
webhook_url="https://3b20-115-98-238-11.ngrok-free.app/ticket-response"
base_redirect_url="https://3b20-115-98-238-11.ngrok-free.app/success"

#WE SUGGEST USING GMAIL ALONG WITH APP SPECIFIC PASSWORD
SENDER_EMAIL='your_gmail_Address@gmail.com'
APP_SPECIFIC_PASSWORD='your_App_specific_password'

