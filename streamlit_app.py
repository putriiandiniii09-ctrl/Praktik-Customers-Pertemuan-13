import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Customer Analytics Dashboard")

df = pd.read_csv("customers (1).csv")

# =========================
# PATCH: rapikan data string (hindari "Sales " vs "Sales")
# =========================
df["Department"] = df["Department"].astype(str).str.strip()
df["Gender"] = df["Gender"].astype(str).str.strip()

st.sidebar.header("Filter Data")

# =========================
# PATCH: options rapi + default aman
# =========================
all_departments = sorted(df["Department"].dropna().unique().tolist())
all_genders = sorted(df["Gender"].dropna().unique().tolist())

# Simpan pilihan di session_state (biar konsisten saat rerun)
if "departments_selected" not in st.session_state:
    st.session_state.departments_selected = all_departments
else:
    st.session_state.departments_selected = [
        d for d in st.session_state.departments_selected if d in all_departments
    ]
    if len(st.session_state.departments_selected) == 0:
        st.session_state.departments_selected = all_departments

if "genders_selected" not in st.session_state:
    st.session_state.genders_selected = all_genders
else:
    st.session_state.genders_selected = [
        g for g in st.session_state.genders_selected if g in all_genders
    ]
    if len(st.session_state.genders_selected) == 0:
        st.session_state.genders_selected = all_genders

departments = st.sidebar.multiselect(
    "Pilih Departments",
    options=all_departments,
    default=st.session_state.departments_selected,
    key="departments_selected"
)

genders = st.sidebar.multiselect(
    "Pilih Gender",
    options=all_genders,
    default=st.session_state.genders_selected,
    key="genders_selected"
)

st.sidebar.header("Filter Rentang Umur")
min_usia, max_usia = int(df["Age"].min()), int(df["Age"].max())
usia_range = st.sidebar.slider(
    "Usia",
    min_value=min_usia,
    max_value=max_usia,
    value=(min_usia, max_usia)
)

df_filtered = df[
    (df["Department"].isin(departments)) &
    (df["Gender"].isin(genders)) &
    (df["Age"].between(usia_range[0], usia_range[1]))
]

st.subheader("Data Tabel")
st.dataframe(df_filtered)

st.subheader("Visualisasi Statistik")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Gender")
    pie_gender = px.pie(
        df_filtered,
        names="Gender",
        color="Gender",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(pie_gender)

with col2:
    st.subheader("Gaji Rata-rata per Department")

    salary_dept = (
        df_filtered
        .groupby("Department")["AnnualSalary"]
        .mean()
        .reset_index()
    )

    bar_salary = px.bar(
        salary_dept,
        x="Department",
        y="AnnualSalary",
        color="Department",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(bar_salary)

st.subheader("Rata-rata Gaji Berdasarkan Usia")
salary_age = (
    df_filtered
    .groupby("Age")["AnnualSalary"]
    .mean()
    .reset_index()
    .sort_values("Age")
)

line_age = px.line(
    salary_age,
    x="Age",
    y="AnnualSalary",
    markers=True
)
st.plotly_chart(line_age)

st.subheader("Tambahkan Chart Lainnya Versi Anda Sendiri!")
st.write("Untuk menambahkan chart lihat dan pahami struktur tabel data set file customers.csv")

st.title("Modifikasi")

st.subheader("Jumlah Karyawan per Department")
count_dept = (
    df_filtered
    .groupby("Department")
    .size()
    .reset_index(name="Jumlah Karyawan")
)
bar_count = px.bar(
    count_dept,
    x="Department",
    y="Jumlah Karyawan",
    color="Department"
)
st.plotly_chart(bar_count)

st.subheader("Histogram Distribusi Umur")
hist_age = px.histogram(
    df_filtered,
    x="Age",
    nbins=10,
    title="Distribusi Umur"
)
st.plotly_chart(hist_age, key="hist_age_tab1")

st.subheader("Distribusi Gaji Berdasarkan Gender")
box_salary = px.box(
    df_filtered,
    x="Gender",
    y="AnnualSalary",
    color="Gender"
)
st.plotly_chart(box_salary)

# AREA CHART
st.subheader("Rata-rata gaji berdasarkan umur")
area_age = px.area(
    salary_age,
    x="Age",
    y="AnnualSalary",
)
st.plotly_chart(area_age, use_container_width=True)

st.markdown("Scatter Plot - Hubungan Umur vs Gaji")
scatter_age_salary = px.scatter(
    df_filtered,
    x="Age",
    y="AnnualSalary",
    color="Department",
    hover_data=["Gender", "Department"],
    title="Umur vs Gaji (warna = Department)"
)
st.plotly_chart(scatter_age_salary, use_container_width=True)

# HEATMAP
st.markdown("Heatmap (Opsional) - Rata-rata Gaji (Department x Gender)")
heatmap_df = (
    df_filtered.groupby(["Department", "Gender"])["AnnualSalary"]
    .mean()
    .reset_index()
)

heatmap = px.density_heatmap(
    heatmap_df,
    x="Department",
    y="Gender",
    z="AnnualSalary",
    color_continuous_scale="Viridis",
    title="Heatmap Rata-rata Gaji: Department x Gender"
)
st.plotly_chart(heatmap, use_container_width=True)

name = st.text_input(label='Nama lengkap', value='')
st.subheader("Ringkasan Data")

if df_filtered.empty:
    st.warning("Data kosong setelah filter.")
else:
    total_karyawan = len(df_filtered)
    rata_umur = df_filtered["Age"].mean()
    rata_gaji = df_filtered["AnnualSalary"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Karyawan", f"{total_karyawan:,}")

    with col2:
        st.metric("Rata-rata Umur", f"{rata_umur:.1f}")

    with col3:
        st.metric("Rata-rata Gaji", f"{rata_gaji:,.0f}")

st.write('Nama: ', name)

Nim = st.text_input(label='NIM', value='')
st.write('NIM: ', Nim)

st.subheader("Kode yang berhasil lahir dari banyak kegagalan")
