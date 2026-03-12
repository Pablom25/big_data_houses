import pandas as pd
from supabase import create_client, Client

SUPABASE_URL = "https://srokpjvugcjjywogqdle.supabase.co"
SUPABASE_KEY = "sb_publishable_Zqqpe9OFj9RctP1bLqCFGQ_LNDoVuQ3"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

df = pd.read_csv("/content/months.csv")
rows = df.to_dict(orient="records")
supabase.table("months").insert(rows).execute()
