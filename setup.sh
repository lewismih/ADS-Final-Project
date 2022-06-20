mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
primaryColor=\"#FF4B4B\"\n\
backgroundColor=\"#0E1117\"\n\
secondaryBackgroundColor=\"#262730\"\n\
textColor=\"#FAFAFA\"\n\
font=\"sans serif\"\n\
" > ~/.streamlit/config.toml