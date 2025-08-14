Weekend project, used to store a daily order in sqlite, using n8n for further workflows. Code to use telegram via API included... 
written with a hot needle, quick n dirty (it works tho'), much refactoring needed, therefor: Beta Mode :3

+after cloning add an .env-file to load necessary variables:

>TELEGRAM_BOT_TOKEN="" // API Token
>TELEGRAM_CHAD_ID=653340762 // User to send order to
>HOST_IP='localhost' // adjust ip of server
>HOST_PORT='5554' // adjust local port of server

+deprecated vars:

>CONVERTAPI_TOKEN_SB="" // not needed anymore
>CONVERTAPI_TOKEN_PROD="" // not need anymore

+ the /admin-route is not secured, add login if additional safety is needed
+ send_telegram_message(order_message) to send via Telegram, actually not used by me due to further n8n-usage
+ convert-api replaced due logic

