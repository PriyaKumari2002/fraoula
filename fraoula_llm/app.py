# # # import streamlit as st
# # # import pandas as pd
# # # import json
# # # import os
# # # import requests
# # # from pymongo import MongoClient

# # # # MongoDB Connection
# # # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # # client = MongoClient(MONGO_URI)

# # # db = client["fraoula_chatbot"]
# # # uploads_collection = db["uploads"]
# # # chat_collection = db["chat_history"]

# # # # --- Config ---
# # # st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# # # DATA_STORE = "knowledge_data.json"
# # # DEV_PASSWORD = "fraoula123"

# # # # Replace this with your actual API key
# # # API_KEY = st.secrets["openrouter"]["api_key"]
# # # API_URL = "https://openrouter.ai/api/v1/chat/completions"
# # # HEADERS = {
# # #     "Authorization": f"Bearer {API_KEY}",
# # #     "Content-Type": "application/json"
# # # }

# # # # --- Theme Colors (Fraoula Violet) ---
# # # PRIMARY_COLOR = "#9400D3"
# # # SECONDARY_COLOR = "#C779D9"
# # # BACKGROUND_COLOR = "#1E003E"
# # # TEXT_COLOR = "#FFFFFF"

# # # # --- Styling ---
# # # st.markdown(f"""
# # # <style>
# # # .stApp {{
# # #     background-color: {BACKGROUND_COLOR};
# # #     color: {TEXT_COLOR};
# # #     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# # # }}
# # # .stTextInput div div input {{
# # #     background-color: #2a004f;
# # #     border: 2px solid {PRIMARY_COLOR};
# # #     border-radius: 8px;
# # #     color: {TEXT_COLOR};
# # #     padding: 10px;
# # # }}
# # # .stButton button {{
# # #     background-color: {PRIMARY_COLOR};
# # #     color: white;
# # #     border-radius: 8px;
# # #     padding: 10px 20px;
# # #     font-weight: 600;
# # #     border: none;
# # #     cursor: pointer;
# # # }}
# # # .stButton button:hover {{
# # #     background-color: {SECONDARY_COLOR};
# # # }}
# # # .user-message {{
# # #     background-color: {SECONDARY_COLOR};
# # #     padding: 10px;
# # #     border-radius: 12px 12px 0 12px;
# # #     margin: 8px 0;
# # #     text-align: right;
# # #     max-width: 75%;
# # #     margin-left: auto;
# # #     color: white;
# # #     font-size: 1rem;
# # # }}
# # # .bot-message {{
# # #     background-color: #3b0070;
# # #     padding: 10px;
# # #     border-radius: 12px 12px 12px 0;
# # #     margin: 8px 0;
# # #     text-align: left;
# # #     max-width: 75%;
# # #     margin-right: auto;
# # #     color: {TEXT_COLOR};
# # #     font-size: 1rem;
# # # }}
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # --- Helper Functions ---
# # # def chunk_text(text, max_chars=500):
# # #     return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# # # # def save_data(chunks):
# # # #     data = [{"chunk": c} for c in chunks]
# # # #     existing = []
# # # #     if os.path.exists(DATA_STORE):
# # # #         with open(DATA_STORE, "r") as f:
# # # #             existing = json.load(f)
# # # #     with open(DATA_STORE, "w") as f:
# # # #         json.dump(existing + data, f)

# # # def save_data(chunks):
# # #     for chunk in chunks:
# # #         uploads_collection.insert_one({"chunk": chunk})

# # # # def load_data():
# # # #     if not os.path.exists(DATA_STORE):
# # # #         return []
# # # #     with open(DATA_STORE, "r") as f:
# # # #         raw = json.load(f)
# # # #     return [item["chunk"] for item in raw]
# # # def load_data():
# # #     return [doc["chunk"] for doc in uploads_collection.find()]

# # # def keyword_search(query, chunks, top_k=3):
# # #     ranked = sorted(
# # #         chunks,
# # #         key=lambda x: sum(1 for word in query.lower().split() if word in x.lower()),
# # #         reverse=True
# # #     )
# # #     return ranked[:top_k] if ranked else []

# # # # --- UI Layout ---
# # # tab1, tab2 = st.tabs(["Dev", "User"])

# # # # --- Developer Panel ---
# # # with tab1:
# # #     st.header("Developer Login")
# # #     if "dev_auth" not in st.session_state:
# # #         st.session_state.dev_auth = False

# # #     if not st.session_state.dev_auth:
# # #         password = st.text_input("Enter Developer Password", type="password")
# # #         if st.button("Login"):
# # #             if password == DEV_PASSWORD:
# # #                 st.session_state.dev_auth = True
# # #                 st.success("Access granted")
# # #             else:
# # #                 st.error("❌ Incorrect password.")
# # #     else:
# # #         st.subheader("Upload Files")
# # #         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

# # #         if uploaded_file:
# # #             file_type = uploaded_file.name.split('.')[-1].lower()
# # #             raw_text = ""
# # #             df_preview = None

# # #             try:
# # #                 if file_type == "csv":
# # #                     try:
# # #                         df_preview = pd.read_csv(uploaded_file, encoding="utf-8")
# # #                     except UnicodeDecodeError:
# # #                         df_preview = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
# # #                     raw_text = df_preview.to_string(index=False)
# # #                 elif file_type == "json":
# # #                     data = json.load(uploaded_file)
# # #                     raw_text = json.dumps(data, indent=2)
# # #                     if isinstance(data, list):
# # #                         df_preview = pd.DataFrame(data)
# # #                     elif isinstance(data, dict):
# # #                         df_preview = pd.json_normalize(data)
# # #                 elif file_type == "txt":
# # #                     raw_text = uploaded_file.read().decode("utf-8")
# # #                 elif file_type == "xlsx":
# # #                     df_preview = pd.read_excel(uploaded_file, engine="openpyxl")
# # #                     raw_text = df_preview.to_string(index=False)

# # #                 chunks = chunk_text(raw_text)
# # #                 save_data(chunks)
# # #                 st.success("✅ Uploaded and saved internal data.")

# # #                 if df_preview is not None:
# # #                     st.subheader("Data Preview")
# # #                     st.dataframe(df_preview)
# # #                 else:
# # #                     st.text_area("Preview", raw_text, height=200)

# # #             except Exception as e:
# # #                 st.error(f"❌ Failed to read file: {e}")

# # # # --- Chat UI ---
# # # with tab2:
# # #     st.title("Fraoula")

# # #     if "chat_history" not in st.session_state:
# # #         st.session_state.chat_history = []

# # #     chunks = load_data()

# # #     chat_container = st.container()
# # #     with chat_container:
# # #         for msg in st.session_state.chat_history:
# # #             css_class = "user-message" if msg["role"] == "user" else "bot-message"
# # #             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# # #     with st.form("chat_form", clear_on_submit=True):
# # #         col1, col2 = st.columns([8, 2])
# # #         with col1:
# # #             user_input = st.text_input("You", placeholder="Ask anything...")
# # #         with col2:
# # #             send_btn = st.form_submit_button("Send")
        
        
# # #         if send_btn and user_input.strip():
# # #             user_msg = user_input.strip()
# # #             st.session_state.chat_history.append({"role": "user", "content": user_msg})

# # #             matches = keyword_search(user_msg, chunks)
# # #             context = "\n---\n".join(matches)

# # #             messages = []
# # #             if context:
# # #                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
# # #             messages += st.session_state.chat_history

# # #             payload = {
# # #                 "model": "mistralai/mixtral-8x7b-instruct",  # replace with any OpenRouter-supported model
# # #                 "messages": messages,
# # #                 "max_tokens": 300,
# # #                 "temperature": 0.7
# # #             }

# # #             with st.spinner("Thinking..."):
# # #                 try:
# # #                     res = requests.post(API_URL, headers=HEADERS, json=payload)
# # #                     res.raise_for_status()
# # #                     bot_reply = res.json()["choices"][0]["message"]["content"]
# # #                 except Exception as e:
# # #                     bot_reply = f"❌ Error: {e}"

# # #             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
# # #             st.rerun()


# # # # Updated version with fixed KeyError and improved data handling
# # # import streamlit as st
# # # import pandas as pd
# # # import json
# # # import requests
# # # from pymongo import MongoClient
# # # from datetime import datetime

# # # # MongoDB Connection
# # # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # # client = MongoClient(MONGO_URI)

# # # db = client["fraoula_chatbot"]
# # # uploads_collection = db["uploads"]
# # # chat_collection = db["chat_history"]

# # # # --- Config ---
# # # st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# # # DEV_PASSWORD = "fraoula123"
# # # API_KEY = st.secrets["openrouter"]["api_key"]
# # # API_URL = "https://openrouter.ai/api/v1/chat/completions"
# # # HEADERS = {
# # #     "Authorization": f"Bearer {API_KEY}",
# # #     "Content-Type": "application/json"
# # # }

# # # # --- Theme Colors (Fraoula Violet) ---
# # # PRIMARY_COLOR = "#9400D3"
# # # SECONDARY_COLOR = "#C779D9"
# # # BACKGROUND_COLOR = "#1E003E"
# # # TEXT_COLOR = "#FFFFFF"

# # # # --- Styling ---
# # # st.markdown(f"""
# # # <style>
# # # /* Your existing styles here */
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # --- Helper Functions ---
# # # def process_csv(file):
# # #     try:
# # #         df = pd.read_csv(file, encoding="utf-8")
# # #     except UnicodeDecodeError:
# # #         df = pd.read_csv(file, encoding="ISO-8859-1")
# # #     # Convert each row to a dictionary and clean up NaN values
# # #     records = []
# # #     for _, row in df.iterrows():
# # #         record = {k: v for k, v in row.items() if pd.notna(v)}
# # #         records.append(record)
# # #     return records

# # # def process_json(file):
# # #     data = json.load(file)
# # #     if isinstance(data, list):
# # #         return data
# # #     elif isinstance(data, dict):
# # #         return [data]
# # #     return []

# # # def process_txt(file):
# # #     text = file.read().decode("utf-8")
# # #     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
# # #     return [{"text": p, "type": "paragraph"} for p in paragraphs]

# # # def process_excel(file):
# # #     df = pd.read_excel(file, engine="openpyxl")
# # #     records = []
# # #     for _, row in df.iterrows():
# # #         record = {k: v for k, v in row.items() if pd.notna(v)}
# # #         records.append(record)
# # #     return records

# # # def save_data(data, file_type, filename):
# # #     if not data:
# # #         return
    
# # #     documents = []
# # #     for item in data:
# # #         doc = {
# # #             "content": item,  # Changed from "data" to "content" for consistency
# # #             "file_type": file_type,
# # #             "filename": filename,
# # #             "created_at": datetime.now()
# # #         }
# # #         documents.append(doc)
    
# # #     if documents:
# # #         uploads_collection.insert_many(documents)
# # #         return len(documents)
# # #     return 0

# # # def load_data():
# # #     try:
# # #         documents = uploads_collection.find({}, {"_id": 0, "content": 1})
# # #         return [doc["content"] for doc in documents]
# # #     except Exception as e:
# # #         st.error(f"Error loading data: {e}")
# # #         return []

# # # def keyword_search(query, chunks, top_k=3):
# # #     if not chunks:
# # #         return []
    
# # #     ranked = []
# # #     for chunk in chunks:
# # #         if not isinstance(chunk, dict):
# # #             continue
# # #         score = 0
# # #         for key, value in chunk.items():
# # #             if isinstance(value, str):
# # #                 score += sum(1 for word in query.lower().split() if word in value.lower())
# # #             elif isinstance(value, (int, float)):
# # #                 if str(value) in query:
# # #                     score += 1
# # #         if score > 0:
# # #             ranked.append((score, chunk))
    
# # #     ranked.sort(reverse=True, key=lambda x: x[0])
# # #     return [item[1] for item in ranked[:top_k]]

# # # # --- UI Layout ---
# # # tab1, tab2 = st.tabs(["Dev", "User"])

# # # # --- Developer Panel ---
# # # with tab1:
# # #     st.header("Developer Login")
# # #     if "dev_auth" not in st.session_state:
# # #         st.session_state.dev_auth = False

# # #     if not st.session_state.dev_auth:
# # #         password = st.text_input("Enter Developer Password", type="password")
# # #         if st.button("Login"):
# # #             if password == DEV_PASSWORD:
# # #                 st.session_state.dev_auth = True
# # #                 st.success("Access granted")
# # #             else:
# # #                 st.error("❌ Incorrect password.")
# # #     else:
# # #         st.subheader("Upload Files")
# # #         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

# # #         if uploaded_file:
# # #             file_type = uploaded_file.name.split('.')[-1].lower()
# # #             processed_data = None
# # #             df_preview = None

# # #             try:
# # #                 if file_type == "csv":
# # #                     processed_data = process_csv(uploaded_file)
# # #                 elif file_type == "json":
# # #                     processed_data = process_json(uploaded_file)
# # #                 elif file_type == "txt":
# # #                     processed_data = process_txt(uploaded_file)
# # #                 elif file_type == "xlsx":
# # #                     processed_data = process_excel(uploaded_file)

# # #                 if processed_data:
# # #                     count = save_data(processed_data, file_type, uploaded_file.name)
# # #                     st.success(f"✅ Uploaded and saved {count} records to database.")
                    
# # #                     # Create preview
# # #                     try:
# # #                         df_preview = pd.DataFrame(processed_data)
# # #                         st.subheader("Data Preview")
# # #                         st.dataframe(df_preview)
# # #                     except Exception as e:
# # #                         st.warning(f"Couldn't create dataframe preview: {e}")
# # #                         st.json(processed_data[:3])  # Show first 3 items as JSON

# # #             except Exception as e:
# # #                 st.error(f"❌ Failed to process file: {e}")

# # # # --- Chat UI ---
# # # with tab2:
# # #     st.title("Fraoula")

# # #     if "chat_history" not in st.session_state:
# # #         st.session_state.chat_history = []

# # #     # Load data only when needed
# # #     if "loaded_data" not in st.session_state:
# # #         st.session_state.loaded_data = load_data()

# # #     chat_container = st.container()
# # #     with chat_container:
# # #         for msg in st.session_state.chat_history:
# # #             css_class = "user-message" if msg["role"] == "user" else "bot-message"
# # #             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# # #     with st.form("chat_form", clear_on_submit=True):
# # #         col1, col2 = st.columns([8, 2])
# # #         with col1:
# # #             user_input = st.text_input("You", placeholder="Ask anything...")
# # #         with col2:
# # #             send_btn = st.form_submit_button("Send")
        
# # #         if send_btn and user_input.strip():
# # #             user_msg = user_input.strip()
# # #             st.session_state.chat_history.append({"role": "user", "content": user_msg})

# # #             matches = keyword_search(user_msg, st.session_state.loaded_data)
# # #             context = "\n---\n".join([str(match) for match in matches])

# # #             messages = []
# # #             if context:
# # #                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
# # #             messages += st.session_state.chat_history

# # #             payload = {
# # #                 "model": "mistralai/mixtral-8x7b-instruct",
# # #                 "messages": messages,
# # #                 "max_tokens": 300,
# # #                 "temperature": 0.7
# # #             }

# # #             with st.spinner("Thinking..."):
# # #                 try:
# # #                     res = requests.post(API_URL, headers=HEADERS, json=payload)
# # #                     res.raise_for_status()
# # #                     bot_reply = res.json()["choices"][0]["message"]["content"]
# # #                 except Exception as e:
# # #                     bot_reply = f"❌ Error: {e}"

# # #             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
# # #             st.rerun()


# # # # ... (previous imports and MongoDB setup remain the same) ...
# # # import streamlit as st
# # # import pandas as pd
# # # import json
# # # import requests
# # # from pymongo import MongoClient
# # # from datetime import datetime
# # # import hashlib
# # # from bson import ObjectId

# # # # MongoDB Connection
# # # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # # client = MongoClient(MONGO_URI)

# # # db = client["fraoula_chatbot"]
# # # uploads_collection = db["uploads"]
# # # chat_collection = db["chat_history"]

# # # # --- Config ---
# # # st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# # # DEV_PASSWORD = "fraoula123"
# # # API_KEY = st.secrets["openrouter"]["api_key"]
# # # API_URL = "https://openrouter.ai/api/v1/chat/completions"
# # # HEADERS = {
# # #     "Authorization": f"Bearer {API_KEY}",
# # #     "Content-Type": "application/json"
# # # }

# # # # --- Theme Colors ---
# # # PRIMARY_COLOR = "#9400D3"
# # # SECONDARY_COLOR = "#C779D9"
# # # BACKGROUND_COLOR = "#1E003E"
# # # TEXT_COLOR = "#FFFFFF"

# # # # --- Styling ---
# # # st.markdown(f"""
# # # <style>
# # # .stApp {{
# # #     background-color: {BACKGROUND_COLOR};
# # #     color: {TEXT_COLOR};
# # # }}
# # # .stButton>button {{
# # #     background-color: {PRIMARY_COLOR};
# # #     color: white;
# # # }}
# # # .stTextInput>div>div>input {{
# # #     color: {TEXT_COLOR};
# # # }}
# # # .user-message {{
# # #     background-color: {SECONDARY_COLOR};
# # #     padding: 10px;
# # #     border-radius: 10px;
# # #     margin: 5px 0;
# # # }}
# # # .bot-message {{
# # #     background-color: {PRIMARY_COLOR};
# # #     padding: 10px;
# # #     border-radius: 10px;
# # #     margin: 5px 0;
# # # }}
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # --- Helper Functions ---
# # # def generate_content_hash(content):
# # #     """Generate a hash for record content to detect duplicates"""
# # #     content_str = str(sorted(content.items())).encode('utf-8')
# # #     return hashlib.md5(content_str).hexdigest()

# # # def process_csv(file):
# # #     try:
# # #         df = pd.read_csv(file, encoding="utf-8")
# # #     except UnicodeDecodeError:
# # #         df = pd.read_csv(file, encoding="ISO-8859-1")
# # #     records = []
# # #     for _, row in df.iterrows():
# # #         record = {k: v for k, v in row.items() if pd.notna(v)}
# # #         record['_content_hash'] = generate_content_hash(record)
# # #         records.append(record)
# # #     return records

# # # def process_json(file):
# # #     data = json.load(file)
# # #     records = []
    
# # #     if isinstance(data, list):
# # #         for item in data:
# # #             if isinstance(item, dict):
# # #                 item['_content_hash'] = generate_content_hash(item)
# # #                 records.append(item)
# # #             else:
# # #                 record = {'value': item, '_content_hash': generate_content_hash({'value': item})}
# # #                 records.append(record)
# # #     elif isinstance(data, dict):
# # #         for k, v in data.items():
# # #             record = {k: v, '_content_hash': generate_content_hash({k: v})}
# # #             records.append(record)
# # #     return records

# # # def process_txt(file):
# # #     text = file.read().decode("utf-8")
# # #     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
# # #     return [{"text": p, "type": "paragraph", '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

# # # def process_excel(file):
# # #     df = pd.read_excel(file, engine="openpyxl")
# # #     records = []
# # #     for _, row in df.iterrows():
# # #         record = {k: v for k, v in row.items() if pd.notna(v)}
# # #         record['_content_hash'] = generate_content_hash(record)
# # #         records.append(record)
# # #     return records

# # # def save_data(data, file_type, filename):
# # #     if not data:
# # #         return 0, 0
    
# # #     existing_hashes = set()
# # #     for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1}):
# # #         if 'content' in doc and '_content_hash' in doc['content']:
# # #             existing_hashes.add(doc['content']['_content_hash'])
    
# # #     new_records = []
# # #     updated_count = 0
    
# # #     for record in data:
# # #         content_hash = record['_content_hash']
        
# # #         if content_hash not in existing_hashes:
# # #             doc = {
# # #                 "content": record,
# # #                 "file_type": file_type,
# # #                 "filename": filename,
# # #                 "created_at": datetime.now(),
# # #                 "updated_at": datetime.now()
# # #             }
# # #             new_records.append(doc)
# # #             updated_count += 1
    
# # #     if new_records:
# # #         result = uploads_collection.insert_many(new_records)
# # #         return len(result.inserted_ids), updated_count
    
# # #     return 0, 0

# # # def load_data():
# # #     try:
# # #         documents = uploads_collection.find({}, {"_id": 0, "content": 1})
# # #         return [doc["content"] for doc in documents]
# # #     except Exception as e:
# # #         st.error(f"Error loading data: {e}")
# # #         return []

# # # def keyword_search(query, chunks, top_k=3):
# # #     if not chunks:
# # #         return []
    
# # #     ranked = []
# # #     for chunk in chunks:
# # #         if not isinstance(chunk, dict):
# # #             continue
# # #         score = 0
# # #         for key, value in chunk.items():
# # #             if isinstance(value, str):
# # #                 score += sum(1 for word in query.lower().split() if word in value.lower())
# # #             elif isinstance(value, (int, float)):
# # #                 if str(value) in query:
# # #                     score += 1
# # #         if score > 0:
# # #             ranked.append((score, chunk))
    
# # #     ranked.sort(reverse=True, key=lambda x: x[0])
# # #     return [item[1] for item in ranked[:top_k]]

# # # # --- UI Layout ---
# # # tab1, tab2 = st.tabs(["Dev", "User"])

# # # # --- Developer Panel ---
# # # with tab1:
# # #     st.header("Developer Login")
# # #     if "dev_auth" not in st.session_state:
# # #         st.session_state.dev_auth = False

# # #     if not st.session_state.dev_auth:
# # #         password = st.text_input("Enter Developer Password", type="password")
# # #         if st.button("Login"):
# # #             if password == DEV_PASSWORD:
# # #                 st.session_state.dev_auth = True
# # #                 st.success("Access granted")
# # #             else:
# # #                 st.error("❌ Incorrect password.")
# # #     else:
# # #         st.subheader("Upload Files")
# # #         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

# # #         if uploaded_file is not None:
# # #             file_type = uploaded_file.name.split('.')[-1].lower()
# # #             processed_data = None
            
# # #             try:
# # #                 if file_type == "csv":
# # #                     processed_data = process_csv(uploaded_file)
# # #                 elif file_type == "json":
# # #                     processed_data = process_json(uploaded_file)
# # #                 elif file_type == "txt":
# # #                     processed_data = process_txt(uploaded_file)
# # #                 elif file_type == "xlsx":
# # #                     processed_data = process_excel(uploaded_file)

# # #                 if processed_data:
# # #                     # FIRST update the UI with the processed data
# # #                     st.session_state.current_data_preview = processed_data
                    
# # #                     # THEN save to database
# # #                     total_count = len(processed_data)
# # #                     inserted_count, updated_count = save_data(processed_data, file_type, uploaded_file.name)
                    
# # #                     if inserted_count > 0:
# # #                         st.success("✅ File uploaded successfully")
# # #                     else:
# # #                         st.warning("⚠️ Showing modified data (no new records added)")

# # #             except Exception as e:
# # #                 st.error(f"❌ Failed to process file: {e}")
        
# # #         # Single data preview section
# # #         if 'current_data_preview' in st.session_state:
# # #             st.subheader("Current Data Preview")
# # #             try:
# # #                 df_preview = pd.DataFrame(st.session_state.current_data_preview)
# # #                 st.dataframe(df_preview)
# # #             except Exception as e:
# # #                 st.warning(f"Couldn't create dataframe preview: {e}")
# # #                 st.json(st.session_state.current_data_preview)

# # # # --- Chat UI ---
# # # with tab2:
# # #     st.title("Fraoula")

# # #     if "chat_history" not in st.session_state:
# # #         st.session_state.chat_history = []

# # #     if "loaded_data" not in st.session_state:
# # #         st.session_state.loaded_data = load_data()

# # #     chat_container = st.container()
# # #     with chat_container:
# # #         for msg in st.session_state.chat_history:
# # #             css_class = "user-message" if msg["role"] == "user" else "bot-message"
# # #             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# # #     with st.form("chat_form", clear_on_submit=True):
# # #         col1, col2 = st.columns([8, 2])
# # #         with col1:
# # #             user_input = st.text_input("You", placeholder="Ask anything...", key="user_input")
# # #         with col2:
# # #             send_btn = st.form_submit_button("Send")
        
# # #         if send_btn and user_input.strip():
# # #             user_msg = user_input.strip()
# # #             st.session_state.chat_history.append({"role": "user", "content": user_msg})

# # #             matches = keyword_search(user_msg, st.session_state.loaded_data)
# # #             context = "\n---\n".join([str(match) for match in matches])

# # #             messages = []
# # #             if context:
# # #                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
# # #             messages += st.session_state.chat_history

# # #             payload = {
# # #                 "model": "mistralai/mixtral-8x7b-instruct",
# # #                 "messages": messages,
# # #                 "max_tokens": 300,
# # #                 "temperature": 0.7
# # #             }

# # #             with st.spinner("Thinking..."):
# # #                 try:
# # #                     res = requests.post(API_URL, headers=HEADERS, json=payload)
# # #                     res.raise_for_status()
# # #                     bot_reply = res.json()["choices"][0]["message"]["content"]
# # #                 except Exception as e:
# # #                     bot_reply = f"❌ Error: {str(e)}"

# # #             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
# # #             st.rerun()


# # import streamlit as st
# # import pandas as pd
# # import json
# # import requests
# # from pymongo import MongoClient
# # from datetime import datetime
# # import hashlib
# # from bson import ObjectId

# # # MongoDB Connection
# # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # client = MongoClient(MONGO_URI)

# # db = client["fraoula_chatbot"]
# # uploads_collection = db["uploads"]
# # chat_collection = db["chat_history"]

# # # --- Config ---
# # st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# # DEV_PASSWORD = "fraoula123"
# # API_KEY = st.secrets["openrouter"]["api_key"]
# # API_URL = "https://openrouter.ai/api/v1/chat/completions"
# # HEADERS = {
# #     "Authorization": f"Bearer {API_KEY}",
# #     "Content-Type": "application/json"
# # }

# # # --- Theme Colors ---
# # PRIMARY_COLOR = "#9400D3"
# # SECONDARY_COLOR = "#C779D9"
# # BACKGROUND_COLOR = "#1E003E"
# # TEXT_COLOR = "#FFFFFF"

# # # --- Styling ---
# # st.markdown(f"""
# # <style>
# # .stApp {{
# #     background-color: {BACKGROUND_COLOR};
# #     color: {TEXT_COLOR};
# # }}
# # .stButton>button {{
# #     background-color: {PRIMARY_COLOR};
# #     color: white;
# # }}
# # .stTextInput>div>div>input {{
# #     color: {TEXT_COLOR};
# # }}
# # .user-message {{
# #     background-color: {SECONDARY_COLOR};
# #     padding: 10px;
# #     border-radius: 10px;
# #     margin: 5px 0;
# # }}
# # .bot-message {{
# #     background-color: {PRIMARY_COLOR};
# #     padding: 10px;
# #     border-radius: 10px;
# #     margin: 5px 0;
# # }}
# # </style>
# # """, unsafe_allow_html=True)

# # # --- Helper Functions ---
# # def generate_content_hash(content):
# #     """Generate a hash for record content to detect duplicates"""
# #     content_str = str(sorted(content.items())).encode('utf-8')
# #     return hashlib.md5(content_str).hexdigest()

# # def process_csv(file):
# #     try:
# #         df = pd.read_csv(file, encoding="utf-8")
# #     except UnicodeDecodeError:
# #         df = pd.read_csv(file, encoding="ISO-8859-1")
# #     records = []
# #     for _, row in df.iterrows():
# #         record = {k: v for k, v in row.items() if pd.notna(v)}
# #         record['_content_hash'] = generate_content_hash(record)
# #         records.append(record)
# #     return records

# # def process_json(file):
# #     data = json.load(file)
# #     records = []

# #     if isinstance(data, list):
# #         for item in data:
# #             if isinstance(item, dict):
# #                 item['_content_hash'] = generate_content_hash(item)
# #                 records.append(item)
# #             else:
# #                 record = {'value': item, '_content_hash': generate_content_hash({'value': item})}
# #                 records.append(record)
# #     elif isinstance(data, dict):
# #         for k, v in data.items():
# #             record = {k: v, '_content_hash': generate_content_hash({k: v})}
# #             records.append(record)
# #     return records

# # def process_txt(file):
# #     text = file.read().decode("utf-8")
# #     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
# #     return [{"text": p, "type": "paragraph", '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

# # def process_excel(file):
# #     df = pd.read_excel(file, engine="openpyxl")
# #     records = []
# #     for _, row in df.iterrows():
# #         record = {k: v for k, v in row.items() if pd.notna(v)}
# #         record['_content_hash'] = generate_content_hash(record)
# #         records.append(record)
# #     return records

# # def save_data(data, file_type, filename):
# #     if not data:
# #         return 0, 0

# #     existing_hashes = set()
# #     for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1}):
# #         if 'content' in doc and '_content_hash' in doc['content']:
# #             existing_hashes.add(doc['content']['_content_hash'])

# #     new_records = []
# #     updated_count = 0

# #     for record in data:
# #         content_hash = record['_content_hash']

# #         if content_hash not in existing_hashes:
# #             doc = {
# #                 "content": record,
# #                 "file_type": file_type,
# #                 "filename": filename,
# #                 "created_at": datetime.now(),
# #                 "updated_at": datetime.now()
# #             }
# #             new_records.append(doc)
# #             updated_count += 1

# #     if new_records:
# #         result = uploads_collection.insert_many(new_records)
# #         return len(result.inserted_ids), updated_count

# #     return 0, 0

# # def load_data():
# #     try:
# #         documents = uploads_collection.find({}, {"_id": 0, "content": 1})
# #         return [doc["content"] for doc in documents]
# #     except Exception as e:
# #         st.error(f"Error loading data: {e}")
# #         return []

# # def load_file_history(filename):
# #     try:
# #         docs = uploads_collection.find({"filename": filename}, {"_id": 0, "content": 1, "created_at": 1})
# #         return [doc["content"] for doc in docs]
# #     except Exception as e:
# #         st.error(f"Error loading file history: {e}")
# #         return []

# # def keyword_search(query, chunks, top_k=3):
# #     if not chunks:
# #         return []

# #     ranked = []
# #     for chunk in chunks:
# #         if not isinstance(chunk, dict):
# #             continue
# #         score = 0
# #         for key, value in chunk.items():
# #             if isinstance(value, str):
# #                 score += sum(1 for word in query.lower().split() if word in value.lower())
# #             elif isinstance(value, (int, float)):
# #                 if str(value) in query:
# #                     score += 1
# #         if score > 0:
# #             ranked.append((score, chunk))

# #     ranked.sort(reverse=True, key=lambda x: x[0])
# #     return [item[1] for item in ranked[:top_k]]

# # # --- UI Layout ---
# # tab1, tab2 = st.tabs(["Dev", "User"])

# # # --- Developer Panel ---
# # with tab1:
# #     st.header("Developer Login")
# #     if "dev_auth" not in st.session_state:
# #         st.session_state.dev_auth = False

# #     if not st.session_state.dev_auth:
# #         password = st.text_input("Enter Developer Password", type="password")
# #         if st.button("Login"):
# #             if password == DEV_PASSWORD:
# #                 st.session_state.dev_auth = True
# #                 st.success("Access granted")
# #             else:
# #                 st.error("❌ Incorrect password.")
# #     else:
# #         st.subheader("Upload Files")
# #         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

# #         if uploaded_file is not None:
# #             file_type = uploaded_file.name.split('.')[-1].lower()
# #             processed_data = None

# #             try:
# #                 if file_type == "csv":
# #                     processed_data = process_csv(uploaded_file)
# #                 elif file_type == "json":
# #                     processed_data = process_json(uploaded_file)
# #                 elif file_type == "txt":
# #                     processed_data = process_txt(uploaded_file)
# #                 elif file_type == "xlsx":
# #                     processed_data = process_excel(uploaded_file)

# #                 if processed_data:
# #                     inserted_count, updated_count = save_data(processed_data, file_type, uploaded_file.name)
# #                     st.session_state.current_data_preview = load_file_history(uploaded_file.name)

# #                     if inserted_count > 0:
# #                         st.success("✅ File uploaded successfully")
# #                     else:
# #                         st.warning("⚠️ Showing modified data (no new records added)")

# #             except Exception as e:
# #                 st.error(f"❌ Failed to process file: {e}")

# #         if 'current_data_preview' in st.session_state:
# #             st.subheader("Current Data Preview")
# #             try:
# #                 df_preview = pd.DataFrame(st.session_state.current_data_preview)
# #                 st.dataframe(df_preview)
# #             except Exception as e:
# #                 st.warning(f"Couldn't create dataframe preview: {e}")
# #                 st.json(st.session_state.current_data_preview)

# # # --- Chat UI ---
# # with tab2:
# #     st.title("Fraoula")

# #     if "chat_history" not in st.session_state:
# #         st.session_state.chat_history = []

# #     if "loaded_data" not in st.session_state:
# #         st.session_state.loaded_data = load_data()

# #     chat_container = st.container()
# #     with chat_container:
# #         for msg in st.session_state.chat_history:
# #             css_class = "user-message" if msg["role"] == "user" else "bot-message"
# #             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# #     with st.form("chat_form", clear_on_submit=True):
# #         col1, col2 = st.columns([8, 2])
# #         with col1:
# #             user_input = st.text_input("You", placeholder="Ask anything...", key="user_input")
# #         with col2:
# #             send_btn = st.form_submit_button("Send")

# #         if send_btn and user_input.strip():
# #             user_msg = user_input.strip()
# #             st.session_state.chat_history.append({"role": "user", "content": user_msg})

# #             matches = keyword_search(user_msg, st.session_state.loaded_data)
# #             context = "\n---\n".join([str(match) for match in matches])

# #             messages = []
# #             if context:
# #                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
# #             messages += st.session_state.chat_history

# #             payload = {
# #                 "model": "mistralai/mixtral-8x7b-instruct",
# #                 "messages": messages,
# #                 "max_tokens": 300,
# #                 "temperature": 0.7
# #             }

# #             with st.spinner("Thinking..."):
# #                 try:
# #                     res = requests.post(API_URL, headers=HEADERS, json=payload)
# #                     res.raise_for_status()
# #                     bot_reply = res.json()["choices"][0]["message"]["content"]
# #                 except Exception as e:
# #                     bot_reply = f"❌ Error: {str(e)}"

# #             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
# #             st.rerun()


# # import streamlit as st
# # import pandas as pd
# # import json
# # import os
# # import requests
# # from pymongo import MongoClient

# # # MongoDB Connection
# # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # client = MongoClient(MONGO_URI)

# # db = client["fraoula_chatbot"]
# # uploads_collection = db["uploads"]
# # chat_collection = db["chat_history"]

# # # --- Config ---
# # st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# # DATA_STORE = "knowledge_data.json"
# # DEV_PASSWORD = "fraoula123"

# # # Replace this with your actual API key
# # API_KEY = st.secrets["openrouter"]["api_key"]
# # API_URL = "https://openrouter.ai/api/v1/chat/completions"
# # HEADERS = {
# #     "Authorization": f"Bearer {API_KEY}",
# #     "Content-Type": "application/json"
# # }

# # # --- Theme Colors (Fraoula Violet) ---
# # PRIMARY_COLOR = "#9400D3"
# # SECONDARY_COLOR = "#C779D9"
# # BACKGROUND_COLOR = "#1E003E"
# # TEXT_COLOR = "#FFFFFF"

# # # --- Styling ---
# # st.markdown(f"""
# # <style>
# # .stApp {{
# #     background-color: {BACKGROUND_COLOR};
# #     color: {TEXT_COLOR};
# #     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# # }}
# # .stTextInput div div input {{
# #     background-color: #2a004f;
# #     border: 2px solid {PRIMARY_COLOR};
# #     border-radius: 8px;
# #     color: {TEXT_COLOR};
# #     padding: 10px;
# # }}
# # .stButton button {{
# #     background-color: {PRIMARY_COLOR};
# #     color: white;
# #     border-radius: 8px;
# #     padding: 10px 20px;
# #     font-weight: 600;
# #     border: none;
# #     cursor: pointer;
# # }}
# # .stButton button:hover {{
# #     background-color: {SECONDARY_COLOR};
# # }}
# # .user-message {{
# #     background-color: {SECONDARY_COLOR};
# #     padding: 10px;
# #     border-radius: 12px 12px 0 12px;
# #     margin: 8px 0;
# #     text-align: right;
# #     max-width: 75%;
# #     margin-left: auto;
# #     color: white;
# #     font-size: 1rem;
# # }}
# # .bot-message {{
# #     background-color: #3b0070;
# #     padding: 10px;
# #     border-radius: 12px 12px 12px 0;
# #     margin: 8px 0;
# #     text-align: left;
# #     max-width: 75%;
# #     margin-right: auto;
# #     color: {TEXT_COLOR};
# #     font-size: 1rem;
# # }}
# # </style>
# # """, unsafe_allow_html=True)

# # # --- Helper Functions ---
# # def chunk_text(text, max_chars=500):
# #     return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# # # def save_data(chunks):
# # #     data = [{"chunk": c} for c in chunks]
# # #     existing = []
# # #     if os.path.exists(DATA_STORE):
# # #         with open(DATA_STORE, "r") as f:
# # #             existing = json.load(f)
# # #     with open(DATA_STORE, "w") as f:
# # #         json.dump(existing + data, f)

# # def save_data(chunks):
# #     for chunk in chunks:
# #         uploads_collection.insert_one({"chunk": chunk})

# # # def load_data():
# # #     if not os.path.exists(DATA_STORE):
# # #         return []
# # #     with open(DATA_STORE, "r") as f:
# # #         raw = json.load(f)
# # #     return [item["chunk"] for item in raw]
# # def load_data():
# #     return [doc["chunk"] for doc in uploads_collection.find()]

# # def keyword_search(query, chunks, top_k=3):
# #     ranked = sorted(
# #         chunks,
# #         key=lambda x: sum(1 for word in query.lower().split() if word in x.lower()),
# #         reverse=True
# #     )
# #     return ranked[:top_k] if ranked else []

# # # --- UI Layout ---
# # tab1, tab2 = st.tabs(["Dev", "User"])

# # # --- Developer Panel ---
# # with tab1:
# #     st.header("Developer Login")
# #     if "dev_auth" not in st.session_state:
# #         st.session_state.dev_auth = False

# #     if not st.session_state.dev_auth:
# #         password = st.text_input("Enter Developer Password", type="password")
# #         if st.button("Login"):
# #             if password == DEV_PASSWORD:
# #                 st.session_state.dev_auth = True
# #                 st.success("Access granted")
# #             else:
# #                 st.error("❌ Incorrect password.")
# #     else:
# #         st.subheader("Upload Files")
# #         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

# #         if uploaded_file:
# #             file_type = uploaded_file.name.split('.')[-1].lower()
# #             raw_text = ""
# #             df_preview = None

# #             try:
# #                 if file_type == "csv":
# #                     try:
# #                         df_preview = pd.read_csv(uploaded_file, encoding="utf-8")
# #                     except UnicodeDecodeError:
# #                         df_preview = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
# #                     raw_text = df_preview.to_string(index=False)
# #                 elif file_type == "json":
# #                     data = json.load(uploaded_file)
# #                     raw_text = json.dumps(data, indent=2)
# #                     if isinstance(data, list):
# #                         df_preview = pd.DataFrame(data)
# #                     elif isinstance(data, dict):
# #                         df_preview = pd.json_normalize(data)
# #                 elif file_type == "txt":
# #                     raw_text = uploaded_file.read().decode("utf-8")
# #                 elif file_type == "xlsx":
# #                     df_preview = pd.read_excel(uploaded_file, engine="openpyxl")
# #                     raw_text = df_preview.to_string(index=False)

# #                 chunks = chunk_text(raw_text)
# #                 save_data(chunks)
# #                 st.success("✅ Uploaded and saved internal data.")

# #                 if df_preview is not None:
# #                     st.subheader("Data Preview")
# #                     st.dataframe(df_preview)
# #                 else:
# #                     st.text_area("Preview", raw_text, height=200)

# #             except Exception as e:
# #                 st.error(f"❌ Failed to read file: {e}")

# # # --- Chat UI ---
# # with tab2:
# #     st.title("Fraoula")

# #     if "chat_history" not in st.session_state:
# #         st.session_state.chat_history = []

# #     chunks = load_data()

# #     chat_container = st.container()
# #     with chat_container:
# #         for msg in st.session_state.chat_history:
# #             css_class = "user-message" if msg["role"] == "user" else "bot-message"
# #             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# #     with st.form("chat_form", clear_on_submit=True):
# #         col1, col2 = st.columns([8, 2])
# #         with col1:
# #             user_input = st.text_input("You", placeholder="Ask anything...")
# #         with col2:
# #             send_btn = st.form_submit_button("Send")
        
        
# #         if send_btn and user_input.strip():
# #             user_msg = user_input.strip()
# #             st.session_state.chat_history.append({"role": "user", "content": user_msg})

# #             matches = keyword_search(user_msg, chunks)
# #             context = "\n---\n".join(matches)

# #             messages = []
# #             if context:
# #                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
# #             messages += st.session_state.chat_history

# #             payload = {
# #                 "model": "mistralai/mixtral-8x7b-instruct",  # replace with any OpenRouter-supported model
# #                 "messages": messages,
# #                 "max_tokens": 300,
# #                 "temperature": 0.7
# #             }

# #             with st.spinner("Thinking..."):
# #                 try:
# #                     res = requests.post(API_URL, headers=HEADERS, json=payload)
# #                     res.raise_for_status()
# #                     bot_reply = res.json()["choices"][0]["message"]["content"]
# #                 except Exception as e:
# #                     bot_reply = f"❌ Error: {e}"

# #             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
# #             st.rerun()


# # # Updated version with fixed KeyError and improved data handling
# # import streamlit as st
# # import pandas as pd
# # import json
# # import requests
# # from pymongo import MongoClient
# # from datetime import datetime

# # # MongoDB Connection
# # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # client = MongoClient(MONGO_URI)

# # db = client["fraoula_chatbot"]
# # uploads_collection = db["uploads"]
# # chat_collection = db["chat_history"]

# # # --- Config ---
# # st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# # DEV_PASSWORD = "fraoula123"
# # API_KEY = st.secrets["openrouter"]["api_key"]
# # API_URL = "https://openrouter.ai/api/v1/chat/completions"
# # HEADERS = {
# #     "Authorization": f"Bearer {API_KEY}",
# #     "Content-Type": "application/json"
# # }

# # # --- Theme Colors (Fraoula Violet) ---
# # PRIMARY_COLOR = "#9400D3"
# # SECONDARY_COLOR = "#C779D9"
# # BACKGROUND_COLOR = "#1E003E"
# # TEXT_COLOR = "#FFFFFF"

# # # --- Styling ---
# # st.markdown(f"""
# # <style>
# # /* Your existing styles here */
# # </style>
# # """, unsafe_allow_html=True)

# # # --- Helper Functions ---
# # def process_csv(file):
# #     try:
# #         df = pd.read_csv(file, encoding="utf-8")
# #     except UnicodeDecodeError:
# #         df = pd.read_csv(file, encoding="ISO-8859-1")
# #     # Convert each row to a dictionary and clean up NaN values
# #     records = []
# #     for _, row in df.iterrows():
# #         record = {k: v for k, v in row.items() if pd.notna(v)}
# #         records.append(record)
# #     return records

# # def process_json(file):
# #     data = json.load(file)
# #     if isinstance(data, list):
# #         return data
# #     elif isinstance(data, dict):
# #         return [data]
# #     return []

# # def process_txt(file):
# #     text = file.read().decode("utf-8")
# #     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
# #     return [{"text": p, "type": "paragraph"} for p in paragraphs]

# # def process_excel(file):
# #     df = pd.read_excel(file, engine="openpyxl")
# #     records = []
# #     for _, row in df.iterrows():
# #         record = {k: v for k, v in row.items() if pd.notna(v)}
# #         records.append(record)
# #     return records

# # def save_data(data, file_type, filename):
# #     if not data:
# #         return
    
# #     documents = []
# #     for item in data:
# #         doc = {
# #             "content": item,  # Changed from "data" to "content" for consistency
# #             "file_type": file_type,
# #             "filename": filename,
# #             "created_at": datetime.now()
# #         }
# #         documents.append(doc)
    
# #     if documents:
# #         uploads_collection.insert_many(documents)
# #         return len(documents)
# #     return 0

# # def load_data():
# #     try:
# #         documents = uploads_collection.find({}, {"_id": 0, "content": 1})
# #         return [doc["content"] for doc in documents]
# #     except Exception as e:
# #         st.error(f"Error loading data: {e}")
# #         return []

# # def keyword_search(query, chunks, top_k=3):
# #     if not chunks:
# #         return []
    
# #     ranked = []
# #     for chunk in chunks:
# #         if not isinstance(chunk, dict):
# #             continue
# #         score = 0
# #         for key, value in chunk.items():
# #             if isinstance(value, str):
# #                 score += sum(1 for word in query.lower().split() if word in value.lower())
# #             elif isinstance(value, (int, float)):
# #                 if str(value) in query:
# #                     score += 1
# #         if score > 0:
# #             ranked.append((score, chunk))
    
# #     ranked.sort(reverse=True, key=lambda x: x[0])
# #     return [item[1] for item in ranked[:top_k]]

# # # --- UI Layout ---
# # tab1, tab2 = st.tabs(["Dev", "User"])

# # # --- Developer Panel ---
# # with tab1:
# #     st.header("Developer Login")
# #     if "dev_auth" not in st.session_state:
# #         st.session_state.dev_auth = False

# #     if not st.session_state.dev_auth:
# #         password = st.text_input("Enter Developer Password", type="password")
# #         if st.button("Login"):
# #             if password == DEV_PASSWORD:
# #                 st.session_state.dev_auth = True
# #                 st.success("Access granted")
# #             else:
# #                 st.error("❌ Incorrect password.")
# #     else:
# #         st.subheader("Upload Files")
# #         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

# #         if uploaded_file:
# #             file_type = uploaded_file.name.split('.')[-1].lower()
# #             processed_data = None
# #             df_preview = None

# #             try:
# #                 if file_type == "csv":
# #                     processed_data = process_csv(uploaded_file)
# #                 elif file_type == "json":
# #                     processed_data = process_json(uploaded_file)
# #                 elif file_type == "txt":
# #                     processed_data = process_txt(uploaded_file)
# #                 elif file_type == "xlsx":
# #                     processed_data = process_excel(uploaded_file)

# #                 if processed_data:
# #                     count = save_data(processed_data, file_type, uploaded_file.name)
# #                     st.success(f"✅ Uploaded and saved {count} records to database.")
                    
# #                     # Create preview
# #                     try:
# #                         df_preview = pd.DataFrame(processed_data)
# #                         st.subheader("Data Preview")
# #                         st.dataframe(df_preview)
# #                     except Exception as e:
# #                         st.warning(f"Couldn't create dataframe preview: {e}")
# #                         st.json(processed_data[:3])  # Show first 3 items as JSON

# #             except Exception as e:
# #                 st.error(f"❌ Failed to process file: {e}")

# # # --- Chat UI ---
# # with tab2:
# #     st.title("Fraoula")

# #     if "chat_history" not in st.session_state:
# #         st.session_state.chat_history = []

# #     # Load data only when needed
# #     if "loaded_data" not in st.session_state:
# #         st.session_state.loaded_data = load_data()

# #     chat_container = st.container()
# #     with chat_container:
# #         for msg in st.session_state.chat_history:
# #             css_class = "user-message" if msg["role"] == "user" else "bot-message"
# #             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# #     with st.form("chat_form", clear_on_submit=True):
# #         col1, col2 = st.columns([8, 2])
# #         with col1:
# #             user_input = st.text_input("You", placeholder="Ask anything...")
# #         with col2:
# #             send_btn = st.form_submit_button("Send")
        
# #         if send_btn and user_input.strip():
# #             user_msg = user_input.strip()
# #             st.session_state.chat_history.append({"role": "user", "content": user_msg})

# #             matches = keyword_search(user_msg, st.session_state.loaded_data)
# #             context = "\n---\n".join([str(match) for match in matches])

# #             messages = []
# #             if context:
# #                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
# #             messages += st.session_state.chat_history

# #             payload = {
# #                 "model": "mistralai/mixtral-8x7b-instruct",
# #                 "messages": messages,
# #                 "max_tokens": 300,
# #                 "temperature": 0.7
# #             }

# #             with st.spinner("Thinking..."):
# #                 try:
# #                     res = requests.post(API_URL, headers=HEADERS, json=payload)
# #                     res.raise_for_status()
# #                     bot_reply = res.json()["choices"][0]["message"]["content"]
# #                 except Exception as e:
# #                     bot_reply = f"❌ Error: {e}"

# #             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
# #             st.rerun()


# # # ... (previous imports and MongoDB setup remain the same) ...
# # import streamlit as st
# # import pandas as pd
# # import json
# # import requests
# # from pymongo import MongoClient
# # from datetime import datetime
# # import hashlib
# # from bson import ObjectId

# # # MongoDB Connection
# # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # client = MongoClient(MONGO_URI)

# # db = client["fraoula_chatbot"]
# # uploads_collection = db["uploads"]
# # chat_collection = db["chat_history"]

# # # --- Config ---
# # st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# # DEV_PASSWORD = "fraoula123"
# # API_KEY = st.secrets["openrouter"]["api_key"]
# # API_URL = "https://openrouter.ai/api/v1/chat/completions"
# # HEADERS = {
# #     "Authorization": f"Bearer {API_KEY}",
# #     "Content-Type": "application/json"
# # }

# # # --- Theme Colors ---
# # PRIMARY_COLOR = "#9400D3"
# # SECONDARY_COLOR = "#C779D9"
# # BACKGROUND_COLOR = "#1E003E"
# # TEXT_COLOR = "#FFFFFF"

# # # --- Styling ---
# # st.markdown(f"""
# # <style>
# # .stApp {{
# #     background-color: {BACKGROUND_COLOR};
# #     color: {TEXT_COLOR};
# # }}
# # .stButton>button {{
# #     background-color: {PRIMARY_COLOR};
# #     color: white;
# # }}
# # .stTextInput>div>div>input {{
# #     color: {TEXT_COLOR};
# # }}
# # .user-message {{
# #     background-color: {SECONDARY_COLOR};
# #     padding: 10px;
# #     border-radius: 10px;
# #     margin: 5px 0;
# # }}
# # .bot-message {{
# #     background-color: {PRIMARY_COLOR};
# #     padding: 10px;
# #     border-radius: 10px;
# #     margin: 5px 0;
# # }}
# # </style>
# # """, unsafe_allow_html=True)

# # # --- Helper Functions ---
# # def generate_content_hash(content):
# #     """Generate a hash for record content to detect duplicates"""
# #     content_str = str(sorted(content.items())).encode('utf-8')
# #     return hashlib.md5(content_str).hexdigest()

# # def process_csv(file):
# #     try:
# #         df = pd.read_csv(file, encoding="utf-8")
# #     except UnicodeDecodeError:
# #         df = pd.read_csv(file, encoding="ISO-8859-1")
# #     records = []
# #     for _, row in df.iterrows():
# #         record = {k: v for k, v in row.items() if pd.notna(v)}
# #         record['_content_hash'] = generate_content_hash(record)
# #         records.append(record)
# #     return records

# # def process_json(file):
# #     data = json.load(file)
# #     records = []
    
# #     if isinstance(data, list):
# #         for item in data:
# #             if isinstance(item, dict):
# #                 item['_content_hash'] = generate_content_hash(item)
# #                 records.append(item)
# #             else:
# #                 record = {'value': item, '_content_hash': generate_content_hash({'value': item})}
# #                 records.append(record)
# #     elif isinstance(data, dict):
# #         for k, v in data.items():
# #             record = {k: v, '_content_hash': generate_content_hash({k: v})}
# #             records.append(record)
# #     return records

# # def process_txt(file):
# #     text = file.read().decode("utf-8")
# #     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
# #     return [{"text": p, "type": "paragraph", '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

# # def process_excel(file):
# #     df = pd.read_excel(file, engine="openpyxl")
# #     records = []
# #     for _, row in df.iterrows():
# #         record = {k: v for k, v in row.items() if pd.notna(v)}
# #         record['_content_hash'] = generate_content_hash(record)
# #         records.append(record)
# #     return records

# # def save_data(data, file_type, filename):
# #     if not data:
# #         return 0, 0
    
# #     existing_hashes = set()
# #     for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1}):
# #         if 'content' in doc and '_content_hash' in doc['content']:
# #             existing_hashes.add(doc['content']['_content_hash'])
    
# #     new_records = []
# #     updated_count = 0
    
# #     for record in data:
# #         content_hash = record['_content_hash']
        
# #         if content_hash not in existing_hashes:
# #             doc = {
# #                 "content": record,
# #                 "file_type": file_type,
# #                 "filename": filename,
# #                 "created_at": datetime.now(),
# #                 "updated_at": datetime.now()
# #             }
# #             new_records.append(doc)
# #             updated_count += 1
    
# #     if new_records:
# #         result = uploads_collection.insert_many(new_records)
# #         return len(result.inserted_ids), updated_count
    
# #     return 0, 0

# # def load_data():
# #     try:
# #         documents = uploads_collection.find({}, {"_id": 0, "content": 1})
# #         return [doc["content"] for doc in documents]
# #     except Exception as e:
# #         st.error(f"Error loading data: {e}")
# #         return []

# # def keyword_search(query, chunks, top_k=3):
# #     if not chunks:
# #         return []
    
# #     ranked = []
# #     for chunk in chunks:
# #         if not isinstance(chunk, dict):
# #             continue
# #         score = 0
# #         for key, value in chunk.items():
# #             if isinstance(value, str):
# #                 score += sum(1 for word in query.lower().split() if word in value.lower())
# #             elif isinstance(value, (int, float)):
# #                 if str(value) in query:
# #                     score += 1
# #         if score > 0:
# #             ranked.append((score, chunk))
    
# #     ranked.sort(reverse=True, key=lambda x: x[0])
# #     return [item[1] for item in ranked[:top_k]]

# # # --- UI Layout ---
# # tab1, tab2 = st.tabs(["Dev", "User"])

# # # --- Developer Panel ---
# # with tab1:
# #     st.header("Developer Login")
# #     if "dev_auth" not in st.session_state:
# #         st.session_state.dev_auth = False

# #     if not st.session_state.dev_auth:
# #         password = st.text_input("Enter Developer Password", type="password")
# #         if st.button("Login"):
# #             if password == DEV_PASSWORD:
# #                 st.session_state.dev_auth = True
# #                 st.success("Access granted")
# #             else:
# #                 st.error("❌ Incorrect password.")
# #     else:
# #         st.subheader("Upload Files")
# #         uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])

# #         if uploaded_file is not None:
# #             file_type = uploaded_file.name.split('.')[-1].lower()
# #             processed_data = None
            
# #             try:
# #                 if file_type == "csv":
# #                     processed_data = process_csv(uploaded_file)
# #                 elif file_type == "json":
# #                     processed_data = process_json(uploaded_file)
# #                 elif file_type == "txt":
# #                     processed_data = process_txt(uploaded_file)
# #                 elif file_type == "xlsx":
# #                     processed_data = process_excel(uploaded_file)

# #                 if processed_data:
# #                     # FIRST update the UI with the processed data
# #                     st.session_state.current_data_preview = processed_data
                    
# #                     # THEN save to database
# #                     total_count = len(processed_data)
# #                     inserted_count, updated_count = save_data(processed_data, file_type, uploaded_file.name)
                    
# #                     if inserted_count > 0:
# #                         st.success("✅ File uploaded successfully")
# #                     else:
# #                         st.warning("⚠️ Showing modified data (no new records added)")

# #             except Exception as e:
# #                 st.error(f"❌ Failed to process file: {e}")
        
# #         # Single data preview section
# #         if 'current_data_preview' in st.session_state:
# #             st.subheader("Current Data Preview")
# #             try:
# #                 df_preview = pd.DataFrame(st.session_state.current_data_preview)
# #                 st.dataframe(df_preview)
# #             except Exception as e:
# #                 st.warning(f"Couldn't create dataframe preview: {e}")
# #                 st.json(st.session_state.current_data_preview)

# # # --- Chat UI ---
# # with tab2:
# #     st.title("Fraoula")

# #     if "chat_history" not in st.session_state:
# #         st.session_state.chat_history = []

# #     if "loaded_data" not in st.session_state:
# #         st.session_state.loaded_data = load_data()

# #     chat_container = st.container()
# #     with chat_container:
# #         for msg in st.session_state.chat_history:
# #             css_class = "user-message" if msg["role"] == "user" else "bot-message"
# #             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# #     with st.form("chat_form", clear_on_submit=True):
# #         col1, col2 = st.columns([8, 2])
# #         with col1:
# #             user_input = st.text_input("You", placeholder="Ask anything...", key="user_input")
# #         with col2:
# #             send_btn = st.form_submit_button("Send")
        
# #         if send_btn and user_input.strip():
# #             user_msg = user_input.strip()
# #             st.session_state.chat_history.append({"role": "user", "content": user_msg})

# #             matches = keyword_search(user_msg, st.session_state.loaded_data)
# #             context = "\n---\n".join([str(match) for match in matches])

# #             messages = []
# #             if context:
# #                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
# #             messages += st.session_state.chat_history

# #             payload = {
# #                 "model": "mistralai/mixtral-8x7b-instruct",
# #                 "messages": messages,
# #                 "max_tokens": 300,
# #                 "temperature": 0.7
# #             }

# #             with st.spinner("Thinking..."):
# #                 try:
# #                     res = requests.post(API_URL, headers=HEADERS, json=payload)
# #                     res.raise_for_status()
# #                     bot_reply = res.json()["choices"][0]["message"]["content"]
# #                 except Exception as e:
# #                     bot_reply = f"❌ Error: {str(e)}"

# #             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
# #             st.rerun()


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

# def load_file_history(filename):
#     try:
#         docs = uploads_collection.find({"filename": filename}, {"_id": 0, "content": 1, "created_at": 1})
#         return [doc["content"] for doc in docs]
#     except Exception as e:
#         st.error(f"Error loading file history: {e}")
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
#                     inserted_count, updated_count = save_data(processed_data, file_type, uploaded_file.name)
#                     st.session_state.current_data_preview = load_file_history(uploaded_file.name)

#                     if inserted_count > 0:
#                         st.success("✅ File uploaded successfully")
#                     else:
#                         st.warning("⚠️ Showing modified data (no new records added)")

#             except Exception as e:
#                 st.error(f"❌ Failed to process file: {e}")

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

# # # # import streamlit as st
# # # # import pandas as pd
# # # # import json
# # # # import requests
# # # # from pymongo import MongoClient
# # # # from datetime import datetime
# # # # import hashlib
# # # # from bson import ObjectId
# # # # import re

# # # # # MongoDB Connection
# # # # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # # # client = MongoClient(MONGO_URI)

# # # # db = client["fraoula_chatbot"]
# # # # uploads_collection = db["uploads"]
# # # # chat_collection = db["chat_history"]

# # # # # --- Config ---
# # # # st.set_page_config(page_title="Fraoula Chatbot", layout="wide")

# # # # DEV_PASSWORD = "fraoula123"
# # # # API_KEY = st.secrets["openrouter"]["api_key"]
# # # # API_URL = "https://openrouter.ai/api/v1/chat/completions"
# # # # HEADERS = {
# # # #     "Authorization": f"Bearer {API_KEY}",
# # # #     "Content-Type": "application/json"
# # # # }

# # # # # YouTube API Configuration
# # # # YOUTUBE_API_KEY = st.secrets["youtube"]["api_key"]
# # # # YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/channels"

# # # # # --- Theme Colors ---
# # # # PRIMARY_COLOR = "#9400D3"
# # # # SECONDARY_COLOR = "#C779D9"
# # # # BACKGROUND_COLOR = "#1E003E"
# # # # TEXT_COLOR = "#FFFFFF"

# # # # # --- Styling ---
# # # # st.markdown(f"""
# # # # <style>
# # # # .stApp {{
# # # #     background-color: {BACKGROUND_COLOR};
# # # #     color: {TEXT_COLOR};
# # # # }}
# # # # .stButton>button {{
# # # #     background-color: {PRIMARY_COLOR};
# # # #     color: white;
# # # # }}
# # # # .stTextInput>div>div>input {{
# # # #     color: {TEXT_COLOR};
# # # # }}
# # # # .user-message {{
# # # #     background-color: {SECONDARY_COLOR};
# # # #     padding: 10px;
# # # #     border-radius: 10px;
# # # #     margin: 5px 0;
# # # # }}
# # # # .bot-message {{
# # # #     background-color: {PRIMARY_COLOR};
# # # #     padding: 10px;
# # # #     border-radius: 10px;
# # # #     margin: 5px 0;
# # # # }}
# # # # </style>
# # # # """, unsafe_allow_html=True)

# # # # # --- Helper Functions ---
# # # # def generate_content_hash(content):
# # # #     content_str = str(sorted(content.items())).encode('utf-8')
# # # #     return hashlib.md5(content_str).hexdigest()

# # # # def process_csv(file):
# # # #     try:
# # # #         df = pd.read_csv(file, encoding="utf-8")
# # # #     except UnicodeDecodeError:
# # # #         df = pd.read_csv(file, encoding="ISO-8859-1")
# # # #     records = []
# # # #     for _, row in df.iterrows():
# # # #         record = {k: v for k, v in row.items() if pd.notna(v)}
# # # #         record['_content_hash'] = generate_content_hash(record)
# # # #         records.append(record)
# # # #     return records

# # # # def process_json(file):
# # # #     data = json.load(file)
# # # #     records = []

# # # #     if isinstance(data, list):
# # # #         for item in data:
# # # #             if isinstance(item, dict):
# # # #                 item['_content_hash'] = generate_content_hash(item)
# # # #                 records.append(item)
# # # #             else:
# # # #                 record = {'value': item, '_content_hash': generate_content_hash({'value': item})}
# # # #                 records.append(record)
# # # #     elif isinstance(data, dict):
# # # #         for k, v in data.items():
# # # #             record = {k: v, '_content_hash': generate_content_hash({k: v})}
# # # #             records.append(record)
# # # #     return records

# # # # def process_txt(file):
# # # #     text = file.read().decode("utf-8")
# # # #     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
# # # #     return [{"text": p, "type": "paragraph", '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

# # # # def process_excel(file):
# # # #     df = pd.read_excel(file, engine="openpyxl")
# # # #     records = []
# # # #     for _, row in df.iterrows():
# # # #         record = {k: v for k, v in row.items() if pd.notna(v)}
# # # #         record['_content_hash'] = generate_content_hash(record)
# # # #         records.append(record)
# # # #     return records

# # # # def extract_channel_id(url_or_id):
# # # #     if url_or_id.startswith('UC') and len(url_or_id) == 24:
# # # #         return url_or_id

# # # #     patterns = [
# # # #         r'youtube\.com/channel/([a-zA-Z0-9_-]{24})',
# # # #         r'youtube\.com/c/([a-zA-Z0-9_-]+)',
# # # #         r'youtube\.com/user/([a-zA-Z0-9_-]+)',
# # # #         r'youtube\.com/@([a-zA-Z0-9_-]+)'
# # # #     ]

# # # #     for pattern in patterns:
# # # #         match = re.search(pattern, url_or_id)
# # # #         if match:
# # # #             return match.group(1)
# # # #     return None

# # # # def get_youtube_channel_data(channel_input):
# # # #     channel_id = extract_channel_id(channel_input)
# # # #     if not channel_id:
# # # #         st.error("Invalid YouTube channel URL or ID.")
# # # #         return None

# # # #     params = {
# # # #         "part": "snippet,statistics",
# # # #         "id": channel_id,
# # # #         "key": YOUTUBE_API_KEY
# # # #     }

# # # #     try:
# # # #         response = requests.get(YOUTUBE_API_URL, params=params)
# # # #         response.raise_for_status()
# # # #         data = response.json()

# # # #         if "items" not in data or len(data["items"]) == 0:
# # # #             st.error("No channel found with this ID.")
# # # #             return None

# # # #         channel = data["items"][0]
# # # #         subscribers = channel["statistics"].get("subscriberCount", 0)
# # # #         views = channel["statistics"].get("viewCount", 0)
# # # #         videos = channel["statistics"].get("videoCount", 0)

# # # #         return {
# # # #             "channel_id": channel_id,
# # # #             "title": channel["snippet"]["title"],
# # # #             "description": channel["snippet"].get("description", ""),
# # # #             "subscribers": int(subscribers),
# # # #             "views": int(views),
# # # #             "videos": int(videos),
# # # #             "thumbnail": channel["snippet"]["thumbnails"]["high"]["url"],
# # # #             "timestamp": datetime.now(),
# # # #             '_content_hash': generate_content_hash({
# # # #                 'channel_id': channel_id,
# # # #                 'subscribers': subscribers,
# # # #                 'views': views,
# # # #                 'videos': videos
# # # #             })
# # # #         }

# # # #     except Exception as e:
# # # #         st.error(f"Error fetching YouTube data: {e}")
# # # #         return None

# # # # def save_youtube_data(channel_data):
# # # #     if not channel_data:
# # # #         return False

# # # #     try:
# # # #         existing = uploads_collection.find_one({
# # # #             "content.channel_id": channel_data["channel_id"],
# # # #             "content._content_hash": channel_data['_content_hash']
# # # #         })

# # # #         if not existing:
# # # #             doc = {
# # # #                 "content": channel_data,
# # # #                 "file_type": "youtube_channel",
# # # #                 "filename": f"youtube_{channel_data['channel_id']}",
# # # #                 "created_at": datetime.now(),
# # # #                 "updated_at": datetime.now()
# # # #             }
# # # #             uploads_collection.insert_one(doc)
# # # #             return True
# # # #         return False
# # # #     except Exception as e:
# # # #         st.error(f"Error saving YouTube data: {e}")
# # # #         return False

# # # # def save_data(data, file_type, filename):
# # # #     if not data:
# # # #         return 0, 0

# # # #     existing_hashes = set()
# # # #     for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1}):
# # # #         if 'content' in doc and '_content_hash' in doc['content']:
# # # #             existing_hashes.add(doc['content']['_content_hash'])

# # # #     new_records = []
# # # #     updated_count = 0

# # # #     for record in data:
# # # #         content_hash = record['_content_hash']
# # # #         if content_hash not in existing_hashes:
# # # #             doc = {
# # # #                 "content": record,
# # # #                 "file_type": file_type,
# # # #                 "filename": filename,
# # # #                 "created_at": datetime.now(),
# # # #                 "updated_at": datetime.now()
# # # #             }
# # # #             new_records.append(doc)
# # # #             updated_count += 1

# # # #     if new_records:
# # # #         result = uploads_collection.insert_many(new_records)
# # # #         return len(result.inserted_ids), updated_count

# # # #     return 0, 0

# # # # def load_data():
# # # #     try:
# # # #         documents = uploads_collection.find({}, {"_id": 0, "content": 1})
# # # #         return [doc["content"] for doc in documents]
# # # #     except Exception as e:
# # # #         st.error(f"Error loading data: {e}")
# # # #         return []

# # # # def load_file_history(filename):
# # # #     try:
# # # #         docs = uploads_collection.find({"filename": filename}, {"_id": 0, "content": 1, "created_at": 1})
# # # #         return [doc["content"] for doc in docs]
# # # #     except Exception as e:
# # # #         st.error(f"Error loading file history: {e}")
# # # #         return []

# # # # def keyword_search(query, chunks, top_k=3):
# # # #     if not chunks:
# # # #         return []

# # # #     ranked = []
# # # #     for chunk in chunks:
# # # #         if not isinstance(chunk, dict):
# # # #             continue
# # # #         score = 0
# # # #         for key, value in chunk.items():
# # # #             if isinstance(value, str):
# # # #                 score += sum(1 for word in query.lower().split() if word in value.lower())
# # # #             elif isinstance(value, (int, float)) and str(value) in query:
# # # #                 score += 1
# # # #         if score > 0:
# # # #             ranked.append((score, chunk))

# # # #     ranked.sort(reverse=True, key=lambda x: x[0])
# # # #     return [item[1] for item in ranked[:top_k]]

# # # # # --- UI Layout ---
# # # # tab1, tab2 = st.tabs(["Dev", "User"])

# # # # # --- Developer Panel ---
# # # # with tab1:
# # # #     st.header("Developer Login")
# # # #     if "dev_auth" not in st.session_state:
# # # #         st.session_state.dev_auth = False

# # # #     if not st.session_state.dev_auth:
# # # #         password = st.text_input("Enter Developer Password", type="password")
# # # #         if st.button("Login"):
# # # #             if password == DEV_PASSWORD:
# # # #                 st.session_state.dev_auth = True
# # # #                 st.success("Access granted")
# # # #             else:
# # # #                 st.error("❌ Incorrect password.")
# # # #     else:
# # # #         st.subheader("Upload Options")
# # # #         upload_option = st.radio("Select upload type:", ["File Upload", "YouTube Channel"])

# # # #         if upload_option == "File Upload":
# # # #             st.subheader("Upload Files")
# # # #             uploaded_file = st.file_uploader("Upload CSV, JSON, TXT, or Excel (.xlsx)", type=["csv", "json", "txt", "xlsx"])
# # # #             if uploaded_file:
# # # #                 file_type = uploaded_file.name.split('.')[-1].lower()
# # # #                 processed_data = None

# # # #                 try:
# # # #                     if file_type == "csv":
# # # #                         processed_data = process_csv(uploaded_file)
# # # #                     elif file_type == "json":
# # # #                         processed_data = process_json(uploaded_file)
# # # #                     elif file_type == "txt":
# # # #                         processed_data = process_txt(uploaded_file)
# # # #                     elif file_type == "xlsx":
# # # #                         processed_data = process_excel(uploaded_file)

# # # #                     if processed_data:
# # # #                         inserted_count, updated_count = save_data(processed_data, file_type, uploaded_file.name)
# # # #                         st.session_state.current_data_preview = load_file_history(uploaded_file.name)

# # # #                         if inserted_count > 0:
# # # #                             st.success("✅ File uploaded successfully")
# # # #                         else:
# # # #                             st.warning("⚠️ No new records added")

# # # #                 except Exception as e:
# # # #                     st.error(f"❌ Failed to process file: {e}")

# # # #         elif upload_option == "YouTube Channel":
# # # #             st.subheader("Fetch YouTube Channel Data")
# # # #             channel_input = st.text_input("Enter YouTube Channel URL or ID")
# # # #             if st.button("Fetch Channel Data") and channel_input:
# # # #                 with st.spinner("Fetching channel data..."):
# # # #                     channel_data = get_youtube_channel_data(channel_input)
# # # #                     if channel_data:
# # # #                         st.success("✅ Channel data fetched successfully!")
# # # #                         st.json(channel_data)
# # # #                         if save_youtube_data(channel_data):
# # # #                             st.success("✅ Channel data saved to database")
# # # #                         else:
# # # #                             st.info("ℹ️ Channel data already exists in database")
# # # #                         st.session_state.current_data_preview = [channel_data]
# # # #                     else:
# # # #                         st.error("❌ Failed to fetch channel data")

# # # #         if 'current_data_preview' in st.session_state:
# # # #             st.subheader("Current Data Preview")
# # # #             try:
# # # #                 df_preview = pd.DataFrame(st.session_state.current_data_preview)
# # # #                 st.dataframe(df_preview)
# # # #             except Exception as e:
# # # #                 st.warning(f"Couldn't create dataframe preview: {e}")
# # # #                 st.json(st.session_state.current_data_preview)

# # # # # --- Chat UI ---
# # # # with tab2:
# # # #     st.title("Fraoula")

# # # #     if "chat_history" not in st.session_state:
# # # #         st.session_state.chat_history = []

# # # #     if "loaded_data" not in st.session_state:
# # # #         st.session_state.loaded_data = load_data()

# # # #     chat_container = st.container()
# # # #     with chat_container:
# # # #         for msg in st.session_state.chat_history:
# # # #             css_class = "user-message" if msg["role"] == "user" else "bot-message"
# # # #             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# # # #     with st.form("chat_form", clear_on_submit=True):
# # # #         col1, col2 = st.columns([8, 2])
# # # #         with col1:
# # # #             user_input = st.text_input("You", placeholder="Ask anything...", key="user_input")
# # # #         with col2:
# # # #             send_btn = st.form_submit_button("Send")

# # # #         if send_btn and user_input.strip():
# # # #             user_msg = user_input.strip()
# # # #             st.session_state.chat_history.append({"role": "user", "content": user_msg})

# # # #             matches = keyword_search(user_msg, st.session_state.loaded_data)
# # # #             context = "\n---\n".join([str(match) for match in matches])

# # # #             messages = []
# # # #             if context:
# # # #                 messages.append({"role": "system", "content": f"Use this information:\n{context}"})
# # # #             messages += st.session_state.chat_history

# # # #             payload = {
# # # #                 "model": "mistralai/mixtral-8x7b-instruct",
# # # #                 "messages": messages,
# # # #                 "max_tokens": 300,
# # # #                 "temperature": 0.7
# # # #             }

# # # #             with st.spinner("Thinking..."):
# # # #                 try:
# # # #                     res = requests.post(API_URL, headers=HEADERS, json=payload)
# # # #                     res.raise_for_status()
# # # #                     bot_reply = res.json()["choices"][0]["message"]["content"]
# # # #                 except Exception as e:
# # # #                     bot_reply = f"❌ Error: {str(e)}"

# # # #             st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
# # # #             st.rerun()

# # # # YouTube Channel Data Uploader with Duplicate Detection and All URL Support

# # # import streamlit as st
# # # import pandas as pd
# # # import requests
# # # from pymongo import MongoClient
# # # from datetime import datetime
# # # import hashlib
# # # import json
# # # import re

# # # # --- Config ---
# # # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # # client = MongoClient(MONGO_URI)
# # # db = client["fraoula_chatbot"]
# # # uploads_collection = db["uploads"]

# # # YOUTUBE_API_KEY = st.secrets["youtube"]["api_key"]

# # # # --- Styling ---
# # # st.set_page_config(page_title="YouTube Channel Uploader", layout="wide")
# # # st.title("📺 YouTube Channel Data Uploader")

# # # # --- Helpers ---
# # # def generate_content_hash(content):
# # #     """Generate a hash for detecting duplicates"""
# # #     return hashlib.md5(json.dumps(content, sort_keys=True).encode()).hexdigest()

# # # def resolve_handle_to_channel_id(handle):
# # #     """Resolve @handle or search keyword to channel ID using YouTube API"""
# # #     search_url = "https://www.googleapis.com/youtube/v3/search"
# # #     params = {
# # #         "part": "snippet",
# # #         "q": handle,
# # #         "type": "channel",
# # #         "key": YOUTUBE_API_KEY
# # #     }
# # #     try:
# # #         res = requests.get(search_url, params=params)
# # #         data = res.json()
# # #         if "items" in data and len(data["items"]) > 0:
# # #             return data["items"][0]["snippet"]["channelId"]
# # #     except:
# # #         return None

# # #     return None

# # # def extract_channel_id(input_text):
# # #     """Extract or resolve YouTube Channel ID"""
# # #     if input_text.startswith("UC") and len(input_text) == 24:
# # #         return input_text

# # #     if "@" in input_text:
# # #         return resolve_handle_to_channel_id(input_text.split("@")[-1])

# # #     patterns = [
# # #         r"youtube\.com/channel/([a-zA-Z0-9_-]{24})",
# # #         r"youtube\.com/c/([a-zA-Z0-9_-]+)",
# # #         r"youtube\.com/user/([a-zA-Z0-9_-]+)",
# # #         r"youtube\.com/@([a-zA-Z0-9_-]+)"
# # #     ]

# # #     for pattern in patterns:
# # #         match = re.search(pattern, input_text)
# # #         if match:
# # #             return resolve_handle_to_channel_id(match.group(1)) if "@" in input_text else match.group(1)

# # #     return resolve_handle_to_channel_id(input_text)

# # # def fetch_channel_data(channel_id):
# # #     url = "https://www.googleapis.com/youtube/v3/channels"
# # #     params = {
# # #         "part": "snippet,statistics",
# # #         "id": channel_id,
# # #         "key": YOUTUBE_API_KEY
# # #     }
# # #     try:
# # #         res = requests.get(url, params=params)
# # #         data = res.json()
# # #         if "items" not in data or len(data["items"]) == 0:
# # #             return None

# # #         ch = data["items"][0]
# # #         stats = ch["statistics"]
# # #         snippet = ch["snippet"]
# # #         record = {
# # #             "channel_id": channel_id,
# # #             "title": snippet["title"],
# # #             "description": snippet.get("description", ""),
# # #             "subscribers": int(stats.get("subscriberCount", 0)),
# # #             "views": int(stats.get("viewCount", 0)),
# # #             "videos": int(stats.get("videoCount", 0)),
# # #             "thumbnail": snippet["thumbnails"]["default"]["url"],
# # #             "timestamp": datetime.utcnow().isoformat()
# # #         }
# # #         record["_content_hash"] = generate_content_hash(record)
# # #         return record
# # #     except:
# # #         return None

# # # def is_duplicate(channel_id, content_hash):
# # #     existing = uploads_collection.find_one({
# # #         "content.channel_id": channel_id,
# # #         "content._content_hash": content_hash
# # #     })
# # #     return existing is not None

# # # def save_channel_data(record):
# # #     doc = {
# # #         "filename": f"youtube_{record['channel_id']}",
# # #         "file_type": "youtube_channel",
# # #         "created_at": datetime.utcnow(),
# # #         "updated_at": datetime.utcnow(),
# # #         "content": record
# # #     }
# # #     uploads_collection.insert_one(doc)

# # # # --- UI ---
# # # channel_input = st.text_input("Enter YouTube Channel URL, ID, or Handle")
# # # if st.button("Fetch and Upload"):
# # #     if not channel_input:
# # #         st.warning("Please enter a YouTube channel link or ID")
# # #     else:
# # #         with st.spinner("Processing..."):
# # #             channel_id = extract_channel_id(channel_input)
# # #             if not channel_id:
# # #                 st.error("❌ Could not resolve the channel ID.")
# # #             else:
# # #                 channel_data = fetch_channel_data(channel_id)
# # #                 if not channel_data:
# # #                     st.error("❌ Failed to fetch channel data.")
# # #                 elif is_duplicate(channel_id, channel_data["_content_hash"]):
# # #                     st.info("⚠️ This channel is already in the database with no changes.")
# # #                 else:
# # #                     save_channel_data(channel_data)
# # #                     st.success("✅ Channel data uploaded successfully!")
# # #                     st.json(channel_data)

# # # st.divider()
# # # st.subheader("📦 Uploaded YouTube Channels")
# # # try:
# # #     docs = list(uploads_collection.find({"file_type": "youtube_channel"}, {"_id": 0, "content": 1}))
# # #     if docs:
# # #         df = pd.DataFrame([doc["content"] for doc in docs])
# # #         st.dataframe(df)
# # #     else:
# # #         st.write("No channel data uploaded yet.")
# # # except Exception as e:
# # #     st.error(f"Error loading data: {e}")

# # # Final Complete Code: YouTube + File Uploads + Duplicate Detection + MongoDB

# # import streamlit as st
# # import pandas as pd
# # import json
# # import requests
# # from pymongo import MongoClient
# # from datetime import datetime
# # import hashlib
# # import re

# # # --- MongoDB Connection ---
# # MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# # client = MongoClient(MONGO_URI)
# # db = client["fraoula_chatbot"]
# # uploads_collection = db["uploads"]

# # # --- API Keys ---
# # YOUTUBE_API_KEY = st.secrets["youtube"]["api_key"]

# # # --- App Config ---
# # st.set_page_config(page_title="Fraoula Uploader", layout="wide")
# # st.title("📦 Upload YouTube or File Data")

# # # --- Hash Generator ---
# # def generate_content_hash(content):
# #     return hashlib.md5(json.dumps(content, sort_keys=True).encode()).hexdigest()

# # # --- YouTube Functions ---
# # def resolve_handle_to_channel_id(handle):
# #     search_url = "https://www.googleapis.com/youtube/v3/search"
# #     params = {
# #         "part": "snippet",
# #         "q": handle,
# #         "type": "channel",
# #         "key": YOUTUBE_API_KEY
# #     }
# #     try:
# #         res = requests.get(search_url, params=params)
# #         data = res.json()
# #         if "items" in data and len(data["items"]) > 0:
# #             return data["items"][0]["snippet"]["channelId"]
# #     except:
# #         return None
# #     return None

# # def extract_channel_id(input_text):
# #     if input_text.startswith("UC") and len(input_text) == 24:
# #         return input_text
# #     if "@" in input_text:
# #         return resolve_handle_to_channel_id(input_text.split("@")[-1])

# #     patterns = [
# #         r"youtube\.com/channel/([a-zA-Z0-9_-]{24})",
# #         r"youtube\.com/c/([a-zA-Z0-9_-]+)",
# #         r"youtube\.com/user/([a-zA-Z0-9_-]+)",
# #         r"youtube\.com/@([a-zA-Z0-9_-]+)"
# #     ]
# #     for pattern in patterns:
# #         match = re.search(pattern, input_text)
# #         if match:
# #             return resolve_handle_to_channel_id(match.group(1)) if "@" in input_text else match.group(1)
# #     return resolve_handle_to_channel_id(input_text)

# # def fetch_channel_data(channel_id):
# #     url = "https://www.googleapis.com/youtube/v3/channels"
# #     params = {
# #         "part": "snippet,statistics",
# #         "id": channel_id,
# #         "key": YOUTUBE_API_KEY
# #     }
# #     try:
# #         res = requests.get(url, params=params)
# #         data = res.json()
# #         if "items" not in data or len(data["items"]) == 0:
# #             return None

# #         ch = data["items"][0]
# #         stats = ch["statistics"]
# #         snippet = ch["snippet"]
# #         record = {
# #             "channel_id": channel_id,
# #             "title": snippet["title"],
# #             "description": snippet.get("description", ""),
# #             "subscribers": int(stats.get("subscriberCount", 0)),
# #             "views": int(stats.get("viewCount", 0)),
# #             "videos": int(stats.get("videoCount", 0)),
# #             "thumbnail": snippet["thumbnails"]["default"]["url"],
# #             "timestamp": datetime.utcnow().isoformat()
# #         }
# #         record["_content_hash"] = generate_content_hash(record)
# #         return record
# #     except:
# #         return None

# # def is_duplicate(channel_id, content_hash):
# #     existing = uploads_collection.find_one({
# #         "content.channel_id": channel_id,
# #         "content._content_hash": content_hash
# #     })
# #     return existing is not None

# # def save_channel_data(record):
# #     doc = {
# #         "filename": f"youtube_{record['channel_id']}",
# #         "file_type": "youtube_channel",
# #         "created_at": datetime.utcnow(),
# #         "updated_at": datetime.utcnow(),
# #         "content": record
# #     }
# #     uploads_collection.insert_one(doc)

# # # --- File Processors ---
# # def process_csv(file):
# #     df = pd.read_csv(file)
# #     records = []
# #     for _, row in df.iterrows():
# #         record = {k: v for k, v in row.items() if pd.notna(v)}
# #         record['_content_hash'] = generate_content_hash(record)
# #         records.append(record)
# #     return records

# # def process_json(file):
# #     data = json.load(file)
# #     records = []
# #     if isinstance(data, list):
# #         for item in data:
# #             record = item if isinstance(item, dict) else {"value": item}
# #             record['_content_hash'] = generate_content_hash(record)
# #             records.append(record)
# #     elif isinstance(data, dict):
# #         for k, v in data.items():
# #             record = {k: v, '_content_hash': generate_content_hash({k: v})}
# #             records.append(record)
# #     return records

# # def process_txt(file):
# #     text = file.read().decode("utf-8")
# #     paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
# #     return [{"text": p, '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

# # def process_excel(file):
# #     df = pd.read_excel(file)
# #     records = []
# #     for _, row in df.iterrows():
# #         record = {k: v for k, v in row.items() if pd.notna(v)}
# #         record['_content_hash'] = generate_content_hash(record)
# #         records.append(record)
# #     return records

# # def save_file_records(records, filename, file_type):
# #     if not records:
# #         return 0
# #     existing_hashes = set(
# #         doc["content"].get("_content_hash")
# #         for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1})
# #     )
# #     new_docs = [
# #         {
# #             "filename": filename,
# #             "file_type": file_type,
# #             "created_at": datetime.utcnow(),
# #             "updated_at": datetime.utcnow(),
# #             "content": record
# #         }
# #         for record in records if record['_content_hash'] not in existing_hashes
# #     ]
# #     if new_docs:
# #         uploads_collection.insert_many(new_docs)
# #     return len(new_docs)

# # # --- UI Layout ---
# # tab1, tab2 = st.tabs(["📂 Upload Files", "📺 YouTube Channel"])

# # # --- File Upload Tab ---
# # with tab1:
# #     st.subheader("Upload CSV, JSON, TXT, or Excel")
# #     uploaded_file = st.file_uploader("Choose a file", type=["csv", "json", "txt", "xlsx"])
# #     if uploaded_file:
# #         ext = uploaded_file.name.split('.')[-1].lower()
# #         if ext == "csv":
# #             records = process_csv(uploaded_file)
# #         elif ext == "json":
# #             records = process_json(uploaded_file)
# #         elif ext == "txt":
# #             records = process_txt(uploaded_file)
# #         elif ext == "xlsx":
# #             records = process_excel(uploaded_file)
# #         else:
# #             records = []

# #         count = save_file_records(records, uploaded_file.name, ext)
# #         st.success(f"✅ {count} new records added to database.")
# #         if records:
# #             st.dataframe(pd.DataFrame(records))

# # # --- YouTube Channel Tab ---
# # with tab2:
# #     st.subheader("Upload YouTube Channel Data")
# #     channel_input = st.text_input("Enter YouTube Channel URL, ID, or @handle")
# #     if st.button("Fetch and Upload"):
# #         if not channel_input:
# #             st.warning("Please enter something")
# #         else:
# #             with st.spinner("Fetching channel data..."):
# #                 channel_id = extract_channel_id(channel_input)
# #                 if not channel_id:
# #                     st.error("❌ Could not resolve channel ID.")
# #                 else:
# #                     data = fetch_channel_data(channel_id)
# #                     if not data:
# #                         st.error("❌ Could not fetch channel data.")
# #                     elif is_duplicate(channel_id, data['_content_hash']):
# #                         st.info("⚠️ Channel already exists with same data.")
# #                     else:
# #                         save_channel_data(data)
# #                         st.success("✅ Channel data saved!")
# #                         st.json(data)

# # # --- Show All Data ---
# # st.divider()
# # st.subheader("📊 All Uploaded Data")
# # docs = list(uploads_collection.find({}, {"_id": 0, "content": 1}))
# # if docs:
# #     df = pd.DataFrame([doc["content"] for doc in docs])
# #     st.dataframe(df)
# # else:
# #     st.write("No data found.")

# import streamlit as st
# import pandas as pd
# import json
# import requests
# from pymongo import MongoClient
# from datetime import datetime
# import hashlib
# import re

# # --- MongoDB Connection ---
# MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
# client = MongoClient(MONGO_URI)
# db = client["fraoula_chatbot"]
# uploads_collection = db["uploads"]
# chat_collection = db["chat_history"]

# # --- API Keys ---
# YOUTUBE_API_KEY = st.secrets["youtube"]["api_key"]
# OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
# OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# # --- App Config ---
# st.set_page_config(page_title="Fraoula Chatbot", layout="wide")
# DEV_PASSWORD = "fraoula123"  # Change this in production

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
#     return hashlib.md5(json.dumps(content, sort_keys=True).encode()).hexdigest()

# # --- YouTube Functions ---
# def resolve_handle_to_channel_id(handle):
#     search_url = "https://www.googleapis.com/youtube/v3/search"
#     params = {
#         "part": "snippet",
#         "q": handle,
#         "type": "channel",
#         "key": YOUTUBE_API_KEY
#     }
#     try:
#         res = requests.get(search_url, params=params)
#         data = res.json()
#         if "items" in data and len(data["items"]) > 0:
#             return data["items"][0]["snippet"]["channelId"]
#     except Exception as e:
#         st.error(f"Error resolving handle: {e}")
#     return None

# def extract_channel_id(input_text):
#     if input_text.startswith("UC") and len(input_text) == 24:
#         return input_text
#     if "@" in input_text:
#         return resolve_handle_to_channel_id(input_text.split("@")[-1])

#     patterns = [
#         r"youtube\.com/channel/([a-zA-Z0-9_-]{24})",
#         r"youtube\.com/c/([a-zA-Z0-9_-]+)",
#         r"youtube\.com/user/([a-zA-Z0-9_-]+)",
#         r"youtube\.com/@([a-zA-Z0-9_-]+)"
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, input_text)
#         if match:
#             return resolve_handle_to_channel_id(match.group(1)) if "@" in input_text else match.group(1)
#     return resolve_handle_to_channel_id(input_text)

# def fetch_channel_data(channel_id):
#     url = "https://www.googleapis.com/youtube/v3/channels"
#     params = {
#         "part": "snippet,statistics",
#         "id": channel_id,
#         "key": YOUTUBE_API_KEY
#     }
#     try:
#         res = requests.get(url, params=params)
#         res.raise_for_status()
#         data = res.json()
#         if "items" not in data or len(data["items"]) == 0:
#             return None

#         ch = data["items"][0]
#         stats = ch["statistics"]
#         snippet = ch["snippet"]
#         record = {
#             "channel_id": channel_id,
#             "title": snippet["title"],
#             "description": snippet.get("description", ""),
#             "subscribers": int(stats.get("subscriberCount", 0)),
#             "views": int(stats.get("viewCount", 0)),
#             "videos": int(stats.get("videoCount", 0)),
#             "thumbnail": snippet["thumbnails"]["high"]["url"],
#             "timestamp": datetime.utcnow().isoformat()
#         }
#         record["_content_hash"] = generate_content_hash(record)
#         return record
#     except Exception as e:
#         st.error(f"Error fetching channel data: {e}")
#     return None

# def is_duplicate(channel_id, content_hash):
#     existing = uploads_collection.find_one({
#         "content.channel_id": channel_id,
#         "content._content_hash": content_hash
#     })
#     return existing is not None

# def save_channel_data(record):
#     doc = {
#         "filename": f"youtube_{record['channel_id']}",
#         "file_type": "youtube_channel",
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow(),
#         "content": record
#     }
#     uploads_collection.insert_one(doc)

# # --- File Processors ---
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
#     return [{"text": p, '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

# def process_excel(file):
#     df = pd.read_excel(file, engine="openpyxl")
#     records = []
#     for _, row in df.iterrows():
#         record = {k: v for k, v in row.items() if pd.notna(v)}
#         record['_content_hash'] = generate_content_hash(record)
#         records.append(record)
#     return records

# def save_file_records(records, filename, file_type):
#     if not records:
#         return 0
#     existing_hashes = set(
#         doc["content"].get("_content_hash")
#         for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1})
#     )
#     new_docs = [
#         {
#             "filename": filename,
#             "file_type": file_type,
#             "created_at": datetime.utcnow(),
#             "updated_at": datetime.utcnow(),
#             "content": record
#         }
#         for record in records if record['_content_hash'] not in existing_hashes
#     ]
#     if new_docs:
#         uploads_collection.insert_many(new_docs)
#     return len(new_docs)

# # --- Chat Functions ---
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
#             elif isinstance(value, (int, float)) and str(value) in query:
#                 score += 1
#         if score > 0:
#             ranked.append((score, chunk))
#     ranked.sort(reverse=True, key=lambda x: x[0])
#     return [item[1] for item in ranked[:top_k]]

# def get_chat_response(user_input, loaded_data):
#     matches = keyword_search(user_input, loaded_data)
#     context = "\n---\n".join([str(match) for match in matches])
    
#     messages = []
#     if context:
#         messages.append({"role": "system", "content": f"Use this information:\n{context}"})
#     messages.append({"role": "user", "content": user_input})
    
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     payload = {
#         "model": "mistralai/mixtral-8x7b-instruct",
#         "messages": messages,
#         "max_tokens": 300,
#         "temperature": 0.7
#     }
    
#     try:
#         res = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
#         res.raise_for_status()
#         return res.json()["choices"][0]["message"]["content"]
#     except Exception as e:
#         return f"❌ Error: {str(e)}"

# # --- UI Layout ---
# tab1, tab2 = st.tabs(["👨‍💻 Developer", "👤 User"])

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
#         st.subheader("Upload Options")
#         upload_option = st.radio("Select upload type:", ["📂 File Upload", "📺 YouTube Channel"])
        
#         if upload_option == "📂 File Upload":
#             st.subheader("Upload Files")
#             uploaded_file = st.file_uploader("Choose a file (CSV, JSON, TXT, Excel)", type=["csv", "json", "txt", "xlsx"])
#             if uploaded_file:
#                 ext = uploaded_file.name.split('.')[-1].lower()
#                 if ext == "csv":
#                     records = process_csv(uploaded_file)
#                 elif ext == "json":
#                     records = process_json(uploaded_file)
#                 elif ext == "txt":
#                     records = process_txt(uploaded_file)
#                 elif ext == "xlsx":
#                     records = process_excel(uploaded_file)
#                 else:
#                     records = []

#                 count = save_file_records(records, uploaded_file.name, ext)
#                 if count > 0:
#                     st.success(f"✅ {count} new records added to database.")
#                 else:
#                     st.info("ℹ️ No new records to add (data already exists)")
#                 if records:
#                     st.dataframe(pd.DataFrame(records))

#         elif upload_option == "📺 YouTube Channel":
#             st.subheader("Fetch YouTube Channel Data")
#             channel_input = st.text_input("Enter YouTube Channel URL, ID, or @handle")
#             if st.button("Fetch and Upload") and channel_input:
#                 with st.spinner("Fetching channel data..."):
#                     channel_id = extract_channel_id(channel_input)
#                     if not channel_id:
#                         st.error("❌ Could not resolve channel ID.")
#                     else:
#                         data = fetch_channel_data(channel_id)
#                         if not data:
#                             st.error("❌ Could not fetch channel data.")
#                         elif is_duplicate(channel_id, data['_content_hash']):
#                             st.info("⚠️ Channel already exists with same data.")
#                         else:
#                             save_channel_data(data)
#                             st.success("✅ Channel data saved!")
#                             st.json(data)

#         st.divider()
#         st.subheader("📊 All Uploaded Data")
#         docs = list(uploads_collection.find({}, {"_id": 0, "content": 1}))
#         if docs:
#             df = pd.DataFrame([doc["content"] for doc in docs])
#             st.dataframe(df)
#         else:
#             st.write("No data found.")

# # --- User Chat Interface ---
# with tab2:
#     st.title("💬 Fraoula Chatbot")
    
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
    
#     if "loaded_data" not in st.session_state:
#         st.session_state.loaded_data = load_data()
    
#     # Display chat history
#     chat_container = st.container()
#     with chat_container:
#         for msg in st.session_state.chat_history:
#             css_class = "user-message" if msg["role"] == "user" else "bot-message"
#             st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)
    
#     # Chat input
#     with st.form("chat_form", clear_on_submit=True):
#         user_input = st.text_input("Your message:", placeholder="Ask me anything...", key="user_input")
#         submit_button = st.form_submit_button("Send")
        
#         if submit_button and user_input.strip():
#             user_msg = user_input.strip()
#             st.session_state.chat_history.append({"role": "user", "content": user_msg})
            
#             with st.spinner("Thinking..."):
#                 bot_reply = get_chat_response(user_msg, st.session_state.loaded_data)
#                 st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
#                 st.rerun()

import streamlit as st
import pandas as pd
import json
import requests
from pymongo import MongoClient
from datetime import datetime
import hashlib
import re

# --- MongoDB Connection ---
MONGO_URI = "mongodb+srv://fraoula:123@cluster0.d4kydid.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["fraoula_chatbot"]
uploads_collection = db["uploads"]
chat_collection = db["chat_history"]

# --- API Keys ---
YOUTUBE_API_KEY = st.secrets["youtube"]["api_key"]
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- App Config ---
st.set_page_config(page_title="Fraoula Chatbot", layout="wide")
DEV_PASSWORD = "fraoula123"  # Change this in production

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
    return hashlib.md5(json.dumps(content, sort_keys=True).encode()).hexdigest()

# --- YouTube Functions ---
def resolve_handle_to_channel_id(handle):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": handle,
        "type": "channel",
        "key": YOUTUBE_API_KEY,
        "maxResults": 1
    }
    try:
        res = requests.get(search_url, params=params)
        res.raise_for_status()
        data = res.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["snippet"]["channelId"]
    except Exception as e:
        st.error(f"Error resolving handle: {e}")
    return None

def extract_channel_id(input_text):
    # Handle direct channel ID
    if input_text.startswith("UC") and len(input_text) == 24:
        return input_text
    
    # Handle @username format
    if input_text.startswith("@"):
        return resolve_handle_to_channel_id(input_text)
    
    # Handle URL patterns
    patterns = [
        r"youtube\.com/channel/([a-zA-Z0-9_-]{24})",
        r"youtube\.com/c/([a-zA-Z0-9_-]+)",
        r"youtube\.com/user/([a-zA-Z0-9_-]+)",
        r"youtube\.com/@([a-zA-Z0-9_-]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_text)
        if match:
            return resolve_handle_to_channel_id(match.group(1))
    
    # If no pattern matched, try to resolve directly
    return resolve_handle_to_channel_id(input_text)

def fetch_channel_data(channel_id):
    # First get channel statistics and basic info
    channels_url = "https://www.googleapis.com/youtube/v3/channels"
    channels_params = {
        "part": "snippet,statistics,brandingSettings",
        "id": channel_id,
        "key": YOUTUBE_API_KEY
    }
    
    try:
        # Get channel main data
        res = requests.get(channels_url, params=channels_params)
        res.raise_for_status()
        data = res.json()
        
        if "items" not in data or len(data["items"]) == 0:
            return None

        channel = data["items"][0]
        stats = channel["statistics"]
        snippet = channel["snippet"]
        branding = channel.get("brandingSettings", {})
        
        # Get country and language from branding settings
        country = branding.get("channel", {}).get("country", "")
        language = snippet.get("defaultLanguage", "")
        
        # Get location from snippet if available
        location = snippet.get("country", "")
        
        # Prepare the record
        record = {
            "channel_id": channel_id,
            "title": snippet["title"],
            "description": snippet.get("description", ""),
            "published_at": snippet.get("publishedAt", ""),
            "subscribers": int(stats.get("subscriberCount", 0)),
            "views": int(stats.get("viewCount", 0)),
            "videos": int(stats.get("videoCount", 0)),
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "country": country,
            "location": location,
            "language": language,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add content hash for duplicate detection
        record["_content_hash"] = generate_content_hash(record)
        
        return record
        
    except Exception as e:
        st.error(f"Error fetching channel data: {e}")
        return None

def is_duplicate(channel_id, content_hash):
    existing = uploads_collection.find_one({
        "content.channel_id": channel_id,
        "content._content_hash": content_hash
    })
    return existing is not None

def save_channel_data(record):
    doc = {
        "filename": f"youtube_{record['channel_id']}",
        "file_type": "youtube_channel",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "content": record
    }
    uploads_collection.insert_one(doc)

# --- File Processors ---
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
    return [{"text": p, '_content_hash': generate_content_hash({"text": p})} for p in paragraphs]

def process_excel(file):
    df = pd.read_excel(file, engine="openpyxl")
    records = []
    for _, row in df.iterrows():
        record = {k: v for k, v in row.items() if pd.notna(v)}
        record['_content_hash'] = generate_content_hash(record)
        records.append(record)
    return records

def save_file_records(records, filename, file_type):
    if not records:
        return 0
    existing_hashes = set(
        doc["content"].get("_content_hash")
        for doc in uploads_collection.find({"filename": filename}, {"content._content_hash": 1})
    )
    new_docs = [
        {
            "filename": filename,
            "file_type": file_type,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "content": record
        }
        for record in records if record['_content_hash'] not in existing_hashes
    ]
    if new_docs:
        uploads_collection.insert_many(new_docs)
    return len(new_docs)

# --- Chat Functions ---
def load_data():
    try:
        documents = uploads_collection.find({}, {"_id": 0, "content": 1})
        return [doc["content"] for doc in documents]
    except Exception as e:
        st.error(f"Error loading data: {e}")
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
            elif isinstance(value, (int, float)) and str(value) in query:
                score += 1
        if score > 0:
            ranked.append((score, chunk))
    ranked.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in ranked[:top_k]]

def get_chat_response(user_input, loaded_data):
    matches = keyword_search(user_input, loaded_data)
    context = "\n---\n".join([str(match) for match in matches])
    
    messages = []
    if context:
        messages.append({"role": "system", "content": f"Use this information:\n{context}"})
    messages.append({"role": "user", "content": user_input})
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0.7
    }
    
    try:
        res = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- UI Layout ---
tab1, tab2 = st.tabs(["👨‍💻 Developer", "👤 User"])

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
        st.subheader("Upload Options")
        upload_option = st.radio("Select upload type:", ["📂 File Upload", "📺 YouTube Channel"])
        
        if upload_option == "📂 File Upload":
            st.subheader("Upload Files")
            uploaded_file = st.file_uploader("Choose a file (CSV, JSON, TXT, Excel)", type=["csv", "json", "txt", "xlsx"])
            if uploaded_file:
                ext = uploaded_file.name.split('.')[-1].lower()
                if ext == "csv":
                    records = process_csv(uploaded_file)
                elif ext == "json":
                    records = process_json(uploaded_file)
                elif ext == "txt":
                    records = process_txt(uploaded_file)
                elif ext == "xlsx":
                    records = process_excel(uploaded_file)
                else:
                    records = []

                count = save_file_records(records, uploaded_file.name, ext)
                if count > 0:
                    st.success(f"✅ {count} new records added to database.")
                else:
                    st.info("ℹ️ No new records to add (data already exists)")
                if records:
                    st.dataframe(pd.DataFrame(records))

        elif upload_option == "📺 YouTube Channel":
            st.subheader("Fetch YouTube Channel Data")
            channel_input = st.text_input("Enter YouTube Channel ID or @handle (e.g., @pewdiepie)")
            
            if st.button("Fetch Channel Data") and channel_input:
                with st.spinner("Fetching channel data..."):
                    channel_id = extract_channel_id(channel_input)
                    if not channel_id:
                        st.error("❌ Could not resolve channel ID.")
                    else:
                        data = fetch_channel_data(channel_id)
                        if not data:
                            st.error("❌ Could not fetch channel data.")
                        elif is_duplicate(channel_id, data['_content_hash']):
                            st.info("⚠️ Channel already exists with same data.")
                        else:
                            save_channel_data(data)
                            st.success("✅ Channel data saved!")
                            
                            # Display the fetched data in a nice format
                            st.subheader("Channel Data Preview")
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                st.image(data["thumbnail"], width=200)
                                st.metric("Subscribers", f"{data['subscribers']:,}")
                                st.metric("Total Views", f"{data['views']:,}")
                                st.metric("Videos", data['videos'])
                            
                            with col2:
                                st.subheader(data["title"])
                                st.write(data["description"])
                                st.write(f"**Country:** {data.get('country', 'N/A')}")
                                st.write(f"**Language:** {data.get('language', 'N/A')}")
                                st.write(f"**Channel ID:** {data['channel_id']}")
                                st.write(f"**Published At:** {data.get('published_at', 'N/A')}")

        st.divider()
        st.subheader("📊 All Uploaded Data")
        docs = list(uploads_collection.find({}, {"_id": 0, "content": 1}))
        if docs:
            # Create a DataFrame with the most important fields
            df = pd.DataFrame([doc["content"] for doc in docs])
            
            # Reorder columns to show the most important first
            preferred_columns = ['title', 'subscribers', 'views', 'videos', 'country', 
                               'language', 'channel_id', 'published_at', 'description']
            
            # Get the columns that actually exist in the data
            available_columns = [col for col in preferred_columns if col in df.columns]
            
            # Add any remaining columns
            remaining_columns = [col for col in df.columns if col not in preferred_columns]
            display_columns = available_columns + remaining_columns
            
            st.dataframe(df[display_columns])
        else:
            st.write("No data found.")

# --- User Chat Interface ---
with tab2:
    st.title("💬 Fraoula Chatbot")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "loaded_data" not in st.session_state:
        st.session_state.loaded_data = load_data()
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            css_class = "user-message" if msg["role"] == "user" else "bot-message"
            st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:", placeholder="Ask me anything...", key="user_input")
        submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input.strip():
            user_msg = user_input.strip()
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            
            with st.spinner("Thinking..."):
                bot_reply = get_chat_response(user_msg, st.session_state.loaded_data)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
                st.rerun()
