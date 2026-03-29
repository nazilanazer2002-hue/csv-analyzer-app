import streamlit as st
import csv
import io
import math
st.set_page_config(page_title="CSV Data Analyzer", page_icon="📊")
st.title("📊 CSV Data Analyzer")
# ---------- Helper Functions ----------
def read_csv(file):
    content=file.read().decode("utf-8")
    reader=csv.DictReader(io.StringIO(content))
    rows=list(reader)
    headers=reader.fieldnames or []
    return headers,rows

def detect_type(values):
    non_empty = [v for v in values if v.strip()!=""]
    if not non_empty:
        return "Text"
    for v in non_empty:
        try:
            float(v)
        except ValueError:
            return "Text"
    return "Number"

def get_numeric_values(values):
    nums=[]
    for v in values:
        if v.strip()!="":
            try:
                nums.append(float(v))
            except ValueError:
                pass
    return nums
def mean(nums):
    return sum(nums)/len(nums) if nums else None

def std(nums):
    if len(nums) < 2:
        return None
    m = mean(nums)
    return math.sqrt(sum((x-m)**2 for x in nums)/len(nums))

def median(nums):
    nums=sorted(nums)
    n=len(nums)
    if n==0:
        return None
    return (nums[n//2] if n%2 else (nums[n//2-1]+nums[n//2])/2)

def fmt(x):
    return f"{x:.2f}" if x is not None else "N/A"
# ---------- Upload ----------
file=st.file_uploader("Upload CSV",type="csv")
if file:
    headers,rows=read_csv(file)
    total_rows=len(rows)
    total_cols=len(headers)
    # ---------- Overview ----------
    st.header("Dataset Overview")
    c1,c2,c3=st.columns(3)
    c1.metric("Rows",total_rows)
    c2.metric("Columns",total_cols)
    c3.metric("Cells",total_rows*total_cols)
    # ---------- Missing ----------
    st.header("Missing Values")
    missing = []
    for col in headers:
        miss = sum(1 for r in rows if r[col].strip()=="")
        pct = (miss/total_rows)*100 if total_rows else 0
        missing.append({"Column":col,"Missing":miss,"%":f"{pct:.1f}%"})
    st.table(missing)
    # ---------- Statistics ----------
    st.header("Statistics")
    numeric_cols = []
    for col in headers:
        vals = [r[col] for r in rows]
        if detect_type(vals)=="Number":
            numeric_cols.append(col)
    if not numeric_cols:
        st.info("No numeric columns found.")
    else:
        selected_col = st.selectbox("Select column",numeric_cols)
        nums = get_numeric_values([r[selected_col] for r in rows])
        stats = {"Mean": fmt(mean(nums)),
                 "Min": fmt(min(nums) if nums else None),
                 "Max": fmt(max(nums) if nums else None),
                 "Std": fmt(std(nums)),
                 "Median": fmt(median(nums))}
        st.subheader(f"Statistics for: {selected_col}")
        st.table(stats)
else:
    st.info("Upload CSV file")

