taskkill /F /FI "WindowTitle eq new_app_*"
start "new_app_req" python app_req.py 1 50000