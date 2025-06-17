# import streamlit as st
# import pandas as pd
# import json
# import os
# import requests
# from pymongo import MongoClient

# # MongoDB Connection
# MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# client = MongoClient(MONGO_URI)

# db = client["fraoula_chatbot"]
# uploads_collection = db["uploads"]
# chat_collection = db["chat_history"]

# # --- Config ---
# st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# DATA_STORE = "knowledge_data.json"
# DEV_PASSWORD = "fraoula123"

# # Replace this with your actual API key
# API_KEY = st.secrets["openrouter"]["api_key"]
# API_URL = "https://openrouter.ai/api/v1/chat/completions"
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# # --- Theme Colors (Fraoula Violet) ---
# PRIMARY_COLOR = "#9400D3"
# SECONDARY_COLOR = "#C779D9"
# BACKGROUND_COLOR = "#1E003E"
# TEXT_COLOR = "#FFFFFF"

# # --- Styling ---
# st.markdown(f"""
# <style>
# .stApp {{
#     background-color: {BACKGROUND_COLOR};
#     color: {TEXT_COLOR};
#     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# }}
# .stTextInput div div input {{
#     background-color: #2a004f;
#     border: 2px solid {PRIMARY_COLOR};
#     border-radius: 8px;
#     color: {TEXT_COLOR};
#     padding: 10px;
# }}
# .stButton button {{
#     background-color: {PRIMARY_COLOR};
#     color: white;
#     border-radius: 8px;
#     padding: 10px 20px;
#     font-weight: 600;
#     border: none;
#     cursor: pointer;
# }}
# .stButton button:hover {{
#     background-color: {SECONDARY_COLOR};
# }}
# .user-message {{
#     background-color: {SECONDARY_COLOR};
#     padding: 10px;
#     border-radius: 12px 12px 0 12px;
#     margin: 8px 0;
#     text-align: right;
#     max-width: 75%;
#     margin-left: auto;
#     color: white;
#     font-size: 1rem;
# }}
# .bot-message {{
#     background-color: #3b0070;
#     padding: 10px;
#     border-radius: 12px 12px 12px 0;
#     margin: 8px 0;
#     text-align: left;
#     max-width: 75%;
#     margin-right: auto;
#     color: {TEXT_COLOR};
#     font-size: 1rem;
# }}
# </style>
# """, unsafe_allow_html=True)

# # --- Helper Functions ---
# def chunk_text(text, max_chars=500):
#     return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# # def save_data(chunks):
# #     data = [{"chunk": c} for c in chunks]
# #     existing = []
# #     if os.path.exists(DATA_STORE):
# #         with open(DATA_STORE, "r") as f:
# #             existing = json.load(f)
# #     with open(DATA_STORE, "w") as f:
# #         json.dump(existing + data, f)

# def save_data(chunks):
#     for chunk in chunks:
#         uploads_collection.insert_one({"chunk": chunk})

# # def load_data():
# #     if not os.path.exists(DATA_STORE):
# #         return []
# #     with open(DATA_STORE, "r") as f:
# #         raw = json.load(f)
# #     return [item["chunk"] for item in raw]
# def load_data():
#     return [doc["chunk"] for doc in uploads_collection.find()]

# def keyword_search(query, chunks, top_k=3):
#     ranked = sorted(
#         chunks,
#         key=lambda x: sum(1 for word in query.lower().split() if word in x.lower()),
#         reverse=True
#     )
#     return ranked[:top_k] if ranked else []

# # --- UI Layout ---
# tab1, tab2 = st.tabs(["Dev", "User"])

# # --- Developer Panel ---
# with tab1:
#     st.header("Developer Login")
#     if "dev_auth" not in st.session_state:
#         st.session_state.dev_auth = False

#     if not st.session_state.dev_auth:
#         password = st.text_input("Enter Developer Password", type="password")
#         if st.button("Login"):
#             if password == DEV_PASSWORD:
#                 st.session_state.dev_auth = True
#                 st.success("Access granted")
#             else:
#                 st.error("❌ Incorrect password.")
#     else:
#         st.subheader("Upload Files")
#         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

#         if uploaded_file:
#             file_type = uploaded_file.name.split('.')[-1].lower()
#             raw_text = ""
#             df_preview = None

#             try:
#                 if file_type == "csv":
#                     try:
#                         df_preview = pd.read_csv(uploaded_file, encoding="utf-8")
#                     except UnicodeDecodeError:
#                         df_preview = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
#                     raw_text = df_preview.to_string(index=False)
#                 elif file_type == "json":
#                     data = json.load(uploaded_file)
#                     raw_text = json.dumps(data, indent=2)
#                     if isinstance(data, list):
#                         df_preview = pd.DataFrame(data)
#                     elif isinstance(data, dict):
#                         df_preview = pd.json_normalize(data)
#                 elif file_type == "txt":
#                     raw_text = uploaded_file.read().decode("utf-8")
#                 elif file_type == "xlsx":
#                     df_preview = pd.read_excel(uploaded_file, engine="openpyxl")
#                     raw_text = df_preview.to_string(index=False)

#                 chunks = chunk_text(raw_text)
#                 save_data(chunks)
#                 st.success("✅ Uploaded and saved internal data.")

#                 if df_preview is not None:
#                     st.subheader("Data Preview")
#                     st.dataframe(df_preview)
#                 else:
#                     st.text_area("Preview", raw_text, height=200)

#             except Exception as e:
#                 st.error(f"❌ Failed to read file: {e}")

# # --- Chat UI ---
# with tab2:
#     st.title("Fraoula")

#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     chunks = load_data()

#     chat_container = st.container()
#     with chat_container:
#         for msg in st.session_state.chat_history:
#             css_class = "user-message" if msg["role"] == "user" else "bot-message"
#             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

#     with st.form("chat_form", clear_on_submit=True):
#         col1, col2 = st.columns([8, 2])
#         with col1:
#             user_input = st.text_input("You", placeholder="Ask anything...")
#         with col2:
#             send_btn = st.form_submit_button("Send")
        
        
#         if send_btn and user_input.strip():
#             user_msg = user_input.strip()
#             st.session_state.chat_history.append({"role": "user", "content": user_msg})

#             matches = keyword_search(user_msg, chunks)
#             context = "\n---\n".join(matches)

#             messages = []
#             if context:
#                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
#             messages += st.session_state.chat_history

#             payload = {
#                 "model": "mistralai/mixtral-8x7b-instruct",  # replace with any OpenRouter-supported model
#                 "messages": messages,
#                 "max_tokens": 300,
#                 "temperature": 0.7
#             }

#             with st.spinner("Thinking..."):
#                 try:
#                     res = requests.post(API_URL, headers=HEADERS, json=payload)
#                     res.raise_for_status()
#                     bot_reply = res.json()["choices"][0]["message"]["content"]
#                 except Exception as e:
#                     bot_reply = f"❌ Error: {e}"

#             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
#             st.rerun()


# # Updated version with fixed KeyError and improved data handling
# import streamlit as st
# import pandas as pd
# import json
# import requests
# from pymongo import MongoClient
# from datetime import datetime

# # MongoDB Connection
# MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# client = MongoClient(MONGO_URI)

# db = client["fraoula_chatbot"]
# uploads_collection = db["uploads"]
# chat_collection = db["chat_history"]

# # --- Config ---
# st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# DEV_PASSWORD = "fraoula123"
# API_KEY = st.secrets["openrouter"]["api_key"]
# API_URL = "https://openrouter.ai/api/v1/chat/completions"
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# # --- Theme Colors (Fraoula Violet) ---
# PRIMARY_COLOR = "#9400D3"
# SECONDARY_COLOR = "#C779D9"
# BACKGROUND_COLOR = "#1E003E"
# TEXT_COLOR = "#FFFFFF"

# # --- Styling ---
# st.markdown(f"""
# <style>
# /* Your existing styles here */
# </style>
# """, unsafe_allow_html=True)

# # --- Helper Functions ---
# def process_csv(file):
#     try:
#         df = pd.read_csv(file, encoding="utf-8")
#     except UnicodeDecodeError:
#         df = pd.read_csv(file, encoding="ISO-8859-1")
#     # Convert each row to a dictionary and clean up NaN values
#     records = []
#     for _, row in df.iterrows():
#         record = {k: v for k, v in row.items() if pd.notna(v)}
#         records.append(record)
#     return records

# def process_json(file):
#     data = json.load(file)
#     if isinstance(data, list):
#         return data
#     elif isinstance(data, dict):
#         return [data]
#     return []

# def process_txt(file):
#     text = file.read().decode("utf-8")
#     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
#     return [{"text": p, "type": "paragraph"} for p in paragraphs]

# def process_excel(file):
#     df = pd.read_excel(file, engine="openpyxl")
#     records = []
#     for _, row in df.iterrows():
#         record = {k: v for k, v in row.items() if pd.notna(v)}
#         records.append(record)
#     return records

# def save_data(data, file_type, filename):
#     if not data:
#         return
    
#     documents = []
#     for item in data:
#         doc = {
#             "content": item,  # Changed from "data" to "content" for consistency
#             "file_type": file_type,
#             "filename": filename,
#             "created_at": datetime.now()
#         }
#         documents.append(doc)
    
#     if documents:
#         uploads_collection.insert_many(documents)
#         return len(documents)
#     return 0

# def load_data():
#     try:
#         documents = uploads_collection.find({}, {"_id": 0, "content": 1})
#         return [doc["content"] for doc in documents]
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return []

# def keyword_search(query, chunks, top_k=3):
#     if not chunks:
#         return []
    
#     ranked = []
#     for chunk in chunks:
#         if not isinstance(chunk, dict):
#             continue
#         score = 0
#         for key, value in chunk.items():
#             if isinstance(value, str):
#                 score += sum(1 for word in query.lower().split() if word in value.lower())
#             elif isinstance(value, (int, float)):
#                 if str(value) in query:
#                     score += 1
#         if score > 0:
#             ranked.append((score, chunk))
    
#     ranked.sort(reverse=True, key=lambda x: x[0])
#     return [item[1] for item in ranked[:top_k]]

# # --- UI Layout ---
# tab1, tab2 = st.tabs(["Dev", "User"])

# # --- Developer Panel ---
# with tab1:
#     st.header("Developer Login")
#     if "dev_auth" not in st.session_state:
#         st.session_state.dev_auth = False

#     if not st.session_state.dev_auth:
#         password = st.text_input("Enter Developer Password", type="password")
#         if st.button("Login"):
#             if password == DEV_PASSWORD:
#                 st.session_state.dev_auth = True
#                 st.success("Access granted")
#             else:
#                 st.error("❌ Incorrect password.")
#     else:
#         st.subheader("Upload Files")
#         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

#         if uploaded_file:
#             file_type = uploaded_file.name.split('.')[-1].lower()
#             processed_data = None
#             df_preview = None

#             try:
#                 if file_type == "csv":
#                     processed_data = process_csv(uploaded_file)
#                 elif file_type == "json":
#                     processed_data = process_json(uploaded_file)
#                 elif file_type == "txt":
#                     processed_data = process_txt(uploaded_file)
#                 elif file_type == "xlsx":
#                     processed_data = process_excel(uploaded_file)

#                 if processed_data:
#                     count = save_data(processed_data, file_type, uploaded_file.name)
#                     st.success(f"✅ Uploaded and saved {count} records to database.")
                    
#                     # Create preview
#                     try:
#                         df_preview = pd.DataFrame(processed_data)
#                         st.subheader("Data Preview")
#                         st.dataframe(df_preview)
#                     except Exception as e:
#                         st.warning(f"Couldn't create dataframe preview: {e}")
#                         st.json(processed_data[:3])  # Show first 3 items as JSON

#             except Exception as e:
#                 st.error(f"❌ Failed to process file: {e}")

# # --- Chat UI ---
# with tab2:
#     st.title("Fraoula")

#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     # Load data only when needed
#     if "loaded_data" not in st.session_state:
#         st.session_state.loaded_data = load_data()

#     chat_container = st.container()
#     with chat_container:
#         for msg in st.session_state.chat_history:
#             css_class = "user-message" if msg["role"] == "user" else "bot-message"
#             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

#     with st.form("chat_form", clear_on_submit=True):
#         col1, col2 = st.columns([8, 2])
#         with col1:
#             user_input = st.text_input("You", placeholder="Ask anything...")
#         with col2:
#             send_btn = st.form_submit_button("Send")
        
#         if send_btn and user_input.strip():
#             user_msg = user_input.strip()
#             st.session_state.chat_history.append({"role": "user", "content": user_msg})

#             matches = keyword_search(user_msg, st.session_state.loaded_data)
#             context = "\n---\n".join([str(match) for match in matches])

#             messages = []
#             if context:
#                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
#             messages += st.session_state.chat_history

#             payload = {
#                 "model": "mistralai/mixtral-8x7b-instruct",
#                 "messages": messages,
#                 "max_tokens": 300,
#                 "temperature": 0.7
#             }

#             with st.spinner("Thinking..."):
#                 try:
#                     res = requests.post(API_URL, headers=HEADERS, json=payload)
#                     res.raise_for_status()
#                     bot_reply = res.json()["choices"][0]["message"]["content"]
#                 except Exception as e:
#                     bot_reply = f"❌ Error: {e}"

#             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
#             st.rerun()


# # ... (previous imports and MongoDB setup remain the same) ...
# import streamlit as st
# import pandas as pd
# import json
# import requests
# from pymongo import MongoClient
# from datetime import datetime
# import hashlib
# from bson import ObjectId

# # MongoDB Connection
# MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# client = MongoClient(MONGO_URI)

# db = client["fraoula_chatbot"]
# uploads_collection = db["uploads"]
# chat_collection = db["chat_history"]

# # --- Config ---
# st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# DEV_PASSWORD = "fraoula123"
# API_KEY = st.secrets["openrouter"]["api_key"]
# API_URL = "https://openrouter.ai/api/v1/chat/completions"
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# # --- Theme Colors ---
# PRIMARY_COLOR = "#9400D3"
# SECONDARY_COLOR = "#C779D9"
# BACKGROUND_COLOR = "#1E003E"
# TEXT_COLOR = "#FFFFFF"

# # --- Styling ---
# st.markdown(f"""
# <style>
# .stApp {{
#     background-color: {BACKGROUND_COLOR};
#     color: {TEXT_COLOR};
# }}
# .stButton>button {{
#     background-color: {PRIMARY_COLOR};
#     color: white;
# }}
# .stTextInput>div>div>input {{
#     color: {TEXT_COLOR};
# }}
# .user-message {{
#     background-color: {SECONDARY_COLOR};
#     padding: 10px;
#     border-radius: 10px;
#     margin: 5px 0;
# }}
# .bot-message {{
#     background-color: {PRIMARY_COLOR};
#     padding: 10px;
#     border-radius: 10px;
#     margin: 5px 0;
# }}
# </style>
# """, unsafe_allow_html=True)

# # --- Helper Functions ---
# def generate_content_hash(content):
#     """Generate a hash for record content to detect duplicates"""
#     content_str = str(sorted(content.items())).encode('utf-8')
#     return hashlib.md5(content_str).hexdigest()

# def process_csv(file):
#     try:
#         df = pd.read_csv(file, encoding="utf-8")
#     except UnicodeDecodeError:
#         df = pd.read_csv(file, encoding="ISO-8859-1")
#     records = []
#     for _, row in df.iterrows():
#         record = {k: v for k, v in row.items() if pd.notna(v)}
#         record['_content_hash'] = generate_content_hash(record)
#         records.append(record)
#     return records

# def process_json(file):
#     data = json.load(file)
#     records = []
    
#     if isinstance(data, list):
#         for item in data:
#             if isinstance(item, dict):
#                 item['_content_hash'] = generate_content_hash(item)
#                 records.append(item)
#             else:
#                 record = {'value': item, '_content_hash': generate_content_hash({'value': item})}
#                 records.append(record)
#     elif isinstance(data, dict):
#         for k, v in data.items():
#             record = {k: v, '_content_hash': generate_content_hash({k: v})}
#             records.append(record)
#     return records

# def process_txt(file):
#     text = file.read().decode("utf-8")
#     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
#     return [{"text": p, "type": "paragraph", '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

# def process_excel(file):
#     df = pd.read_excel(file, engine="openpyxl")
#     records = []
#     for _, row in df.iterrows():
#         record = {k: v for k, v in row.items() if pd.notna(v)}
#         record['_content_hash'] = generate_content_hash(record)
#         records.append(record)
#     return records

# def save_data(data, file_type, filename):
#     if not data:
#         return 0, 0
    
#     existing_hashes = set()
#     for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1}):
#         if 'content' in doc and '_content_hash' in doc['content']:
#             existing_hashes.add(doc['content']['_content_hash'])
    
#     new_records = []
#     updated_count = 0
    
#     for record in data:
#         content_hash = record['_content_hash']
        
#         if content_hash not in existing_hashes:
#             doc = {
#                 "content": record,
#                 "file_type": file_type,
#                 "filename": filename,
#                 "created_at": datetime.now(),
#                 "updated_at": datetime.now()
#             }
#             new_records.append(doc)
#             updated_count += 1
    
#     if new_records:
#         result = uploads_collection.insert_many(new_records)
#         return len(result.inserted_ids), updated_count
    
#     return 0, 0

# def load_data():
#     try:
#         documents = uploads_collection.find({}, {"_id": 0, "content": 1})
#         return [doc["content"] for doc in documents]
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return []

# def keyword_search(query, chunks, top_k=3):
#     if not chunks:
#         return []
    
#     ranked = []
#     for chunk in chunks:
#         if not isinstance(chunk, dict):
#             continue
#         score = 0
#         for key, value in chunk.items():
#             if isinstance(value, str):
#                 score += sum(1 for word in query.lower().split() if word in value.lower())
#             elif isinstance(value, (int, float)):
#                 if str(value) in query:
#                     score += 1
#         if score > 0:
#             ranked.append((score, chunk))
    
#     ranked.sort(reverse=True, key=lambda x: x[0])
#     return [item[1] for item in ranked[:top_k]]

# # --- UI Layout ---
# tab1, tab2 = st.tabs(["Dev", "User"])

# # --- Developer Panel ---
# with tab1:
#     st.header("Developer Login")
#     if "dev_auth" not in st.session_state:
#         st.session_state.dev_auth = False

#     if not st.session_state.dev_auth:
#         password = st.text_input("Enter Developer Password", type="password")
#         if st.button("Login"):
#             if password == DEV_PASSWORD:
#                 st.session_state.dev_auth = True
#                 st.success("Access granted")
#             else:
#                 st.error("❌ Incorrect password.")
#     else:
#         st.subheader("Upload Files")
#         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

#         if uploaded_file is not None:
#             file_type = uploaded_file.name.split('.')[-1].lower()
#             processed_data = None
            
#             try:
#                 if file_type == "csv":
#                     processed_data = process_csv(uploaded_file)
#                 elif file_type == "json":
#                     processed_data = process_json(uploaded_file)
#                 elif file_type == "txt":
#                     processed_data = process_txt(uploaded_file)
#                 elif file_type == "xlsx":
#                     processed_data = process_excel(uploaded_file)

#                 if processed_data:
#                     # FIRST update the UI with the processed data
#                     st.session_state.current_data_preview = processed_data
                    
#                     # THEN save to database
#                     total_count = len(processed_data)
#                     inserted_count, updated_count = save_data(processed_data, file_type, uploaded_file.name)
                    
#                     if inserted_count > 0:
#                         st.success("✅ File uploaded successfully")
#                     else:
#                         st.warning("⚠️ Showing modified data (no new records added)")

#             except Exception as e:
#                 st.error(f"❌ Failed to process file: {e}")
        
#         # Single data preview section
#         if 'current_data_preview' in st.session_state:
#             st.subheader("Current Data Preview")
#             try:
#                 df_preview = pd.DataFrame(st.session_state.current_data_preview)
#                 st.dataframe(df_preview)
#             except Exception as e:
#                 st.warning(f"Couldn't create dataframe preview: {e}")
#                 st.json(st.session_state.current_data_preview)

# # --- Chat UI ---
# with tab2:
#     st.title("Fraoula")

#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     if "loaded_data" not in st.session_state:
#         st.session_state.loaded_data = load_data()

#     chat_container = st.container()
#     with chat_container:
#         for msg in st.session_state.chat_history:
#             css_class = "user-message" if msg["role"] == "user" else "bot-message"
#             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

#     with st.form("chat_form", clear_on_submit=True):
#         col1, col2 = st.columns([8, 2])
#         with col1:
#             user_input = st.text_input("You", placeholder="Ask anything...", key="user_input")
#         with col2:
#             send_btn = st.form_submit_button("Send")
        
#         if send_btn and user_input.strip():
#             user_msg = user_input.strip()
#             st.session_state.chat_history.append({"role": "user", "content": user_msg})

#             matches = keyword_search(user_msg, st.session_state.loaded_data)
#             context = "\n---\n".join([str(match) for match in matches])

#             messages = []
#             if context:
#                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
#             messages += st.session_state.chat_history

#             payload = {
#                 "model": "mistralai/mixtral-8x7b-instruct",
#                 "messages": messages,
#                 "max_tokens": 300,
#                 "temperature": 0.7
#             }

#             with st.spinner("Thinking..."):
#                 try:
#                     res = requests.post(API_URL, headers=HEADERS, json=payload)
#                     res.raise_for_status()
#                     bot_reply = res.json()["choices"][0]["message"]["content"]
#                 except Exception as e:
#                     bot_reply = f"❌ Error: {str(e)}"

#             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
#             st.rerun()


import streamlit as st
import pandas as pd
import json
import requests
from pymongo import MongoClient
from datetime import datetime
import hashlib
from bson import ObjectId

# MongoDB Connection
MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
client = MongoClient(MONGO_URI)

db = client["fraoula_chatbot"]
uploads_collection = db["uploads"]
chat_collection = db["chat_history"]

# --- Config ---
st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

DEV_PASSWORD = "fraoula123"
API_KEY = st.secrets["openrouter"]["api_key"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# --- Theme Colors ---
PRIMARY_COLOR = "#9400D3"
SECONDARY_COLOR = "#C779D9"
BACKGROUND_COLOR = "#1E003E"
TEXT_COLOR = "#FFFFFF"

# --- Styling ---
st.markdown(f"""
<style>
.stApp {{
    background-color: {BACKGROUND_COLOR};
    color: {TEXT_COLOR};
}}
.stButton>button {{
    background-color: {PRIMARY_COLOR};
    color: white;
}}
.stTextInput>div>div>input {{
    color: {TEXT_COLOR};
}}
.user-message {{
    background-color: {SECONDARY_COLOR};
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}}
.bot-message {{
    background-color: {PRIMARY_COLOR};
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}}
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def generate_content_hash(content):
    """Generate a hash for record content to detect duplicates"""
    content_str = str(sorted(content.items())).encode('utf-8')
    return hashlib.md5(content_str).hexdigest()

def process_csv(file):
    try:
        df = pd.read_csv(file, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file, encoding="ISO-8859-1")
    records = []
    for _, row in df.iterrows():
        record = {k: v for k, v in row.items() if pd.notna(v)}
        record['_content_hash'] = generate_content_hash(record)
        records.append(record)
    return records

def process_json(file):
    data = json.load(file)
    records = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                item['_content_hash'] = generate_content_hash(item)
                records.append(item)
            else:
                record = {'value': item, '_content_hash': generate_content_hash({'value': item})}
                records.append(record)
    elif isinstance(data, dict):
        for k, v in data.items():
            record = {k: v, '_content_hash': generate_content_hash({k: v})}
            records.append(record)
    return records

def process_txt(file):
    text = file.read().decode("utf-8")
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return [{"text": p, "type": "paragraph", '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

def process_excel(file):
    df = pd.read_excel(file, engine="openpyxl")
    records = []
    for _, row in df.iterrows():
        record = {k: v for k, v in row.items() if pd.notna(v)}
        record['_content_hash'] = generate_content_hash(record)
        records.append(record)
    return records

def save_data(data, file_type, filename):
    if not data:
        return 0, 0

    existing_hashes = set()
    for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1}):
        if 'content' in doc and '_content_hash' in doc['content']:
            existing_hashes.add(doc['content']['_content_hash'])

    new_records = []
    updated_count = 0

    for record in data:
        content_hash = record['_content_hash']

        if content_hash not in existing_hashes:
            doc = {
                "content": record,
                "file_type": file_type,
                "filename": filename,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            new_records.append(doc)
            updated_count += 1

    if new_records:
        result = uploads_collection.insert_many(new_records)
        return len(result.inserted_ids), updated_count

    return 0, 0

def load_data():
    try:
        documents = uploads_collection.find({}, {"_id": 0, "content": 1})
        return [doc["content"] for doc in documents]
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

def load_file_history(filename):
    try:
        docs = uploads_collection.find({"filename": filename}, {"_id": 0, "content": 1, "created_at": 1})
        return [doc["content"] for doc in docs]
    except Exception as e:
        st.error(f"Error loading file history: {e}")
        return []

def keyword_search(query, chunks, top_k=3):
    if not chunks:
        return []

    ranked = []
    for chunk in chunks:
        if not isinstance(chunk, dict):
            continue
        score = 0
        for key, value in chunk.items():
            if isinstance(value, str):
                score += sum(1 for word in query.lower().split() if word in value.lower())
            elif isinstance(value, (int, float)):
                if str(value) in query:
                    score += 1
        if score > 0:
            ranked.append((score, chunk))

    ranked.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in ranked[:top_k]]

# --- UI Layout ---
tab1, tab2 = st.tabs(["Dev", "User"])

# --- Developer Panel ---
with tab1:
    st.header("Developer Login")
    if "dev_auth" not in st.session_state:
        st.session_state.dev_auth = False

    if not st.session_state.dev_auth:
        password = st.text_input("Enter Developer Password", type="password")
        if st.button("Login"):
            if password == DEV_PASSWORD:
                st.session_state.dev_auth = True
                st.success("Access granted")
            else:
                st.error("❌ Incorrect password.")
    else:
        st.subheader("Upload Files")
        uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

        if uploaded_file is not None:
            file_type = uploaded_file.name.split('.')[-1].lower()
            processed_data = None

            try:
                if file_type == "csv":
                    processed_data = process_csv(uploaded_file)
                elif file_type == "json":
                    processed_data = process_json(uploaded_file)
                elif file_type == "txt":
                    processed_data = process_txt(uploaded_file)
                elif file_type == "xlsx":
                    processed_data = process_excel(uploaded_file)

                if processed_data:
                    inserted_count, updated_count = save_data(processed_data, file_type, uploaded_file.name)
                    st.session_state.current_data_preview = load_file_history(uploaded_file.name)

                    if inserted_count > 0:
                        st.success("✅ File uploaded successfully")
                    else:
                        st.warning("⚠️ Showing modified data (no new records added)")

            except Exception as e:
                st.error(f"❌ Failed to process file: {e}")

        if 'current_data_preview' in st.session_state:
            st.subheader("Current Data Preview")
            try:
                df_preview = pd.DataFrame(st.session_state.current_data_preview)
                st.dataframe(df_preview)
            except Exception as e:
                st.warning(f"Couldn't create dataframe preview: {e}")
                st.json(st.session_state.current_data_preview)

# --- Chat UI ---
with tab2:
    st.title("Fraoula")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "loaded_data" not in st.session_state:
        st.session_state.loaded_data = load_data()

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            css_class = "user-message" if msg["role"] == "user" else "bot-message"
            st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 2])
        with col1:
            user_input = st.text_input("You", placeholder="Ask anything...", key="user_input")
        with col2:
            send_btn = st.form_submit_button("Send")

        if send_btn and user_input.strip():
            user_msg = user_input.strip()
            st.session_state.chat_history.append({"role": "user", "content": user_msg})

            matches = keyword_search(user_msg, st.session_state.loaded_data)
            context = "\n---\n".join([str(match) for match in matches])

            messages = []
            if context:
                messages.append({"role": "system", "content": f"Use this information:\n{context}"})
            messages += st.session_state.chat_history

            payload = {
                "model": "mistralai/mixtral-8x7b-instruct",
                "messages": messages,
                "max_tokens": 300,
                "temperature": 0.7
            }

            with st.spinner("Thinking..."):
                try:
                    res = requests.post(API_URL, headers=HEADERS, json=payload)
                    res.raise_for_status()
                    bot_reply = res.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    bot_reply = f"❌ Error: {str(e)}"

            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            st.rerun()
