import base64
import os
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="منصة التقييم العقاري الذكي | CYSTECH",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_data
def get_img_base64(path="C:/Users/tasne/Desktop/التدريب الميداني/ML/real_estate_bg.jpg.jpg"):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

bg_b64 = get_img_base64()
app_bg_css = (
    f"""
    background-image: linear-gradient(180deg, rgba(248, 250, 252, 0.84) 0%, rgba(241, 245, 249, 0.92) 100%),
                      url("data:image/jpeg;base64,{bg_b64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """
    if bg_b64
    else "background-color: #f8fafc;"
)
hero_bg_css = (
    f"""
    background-image: linear-gradient(105deg, rgba(15, 23, 42, 0.45) 0%, rgba(15, 61, 62, 0.86) 52%, rgba(15, 23, 42, 0.95) 100%),
                      url("data:image/jpeg;base64,{bg_b64}");
    background-size: cover;
    background-position: center;
    """
    if bg_b64
    else "background: linear-gradient(135deg, #0f172a 0%, #0f3d3e 65%, #134e4a 100%);"
)

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif;
    }}
    .stApp {{
        {app_bg_css}
    }}
    /* ضبط RTL بدقة على النصوص، التبويبات، التسميات، وخيارات الراديو دون قلب المنزلقات */
    [data-testid="stMarkdownContainer"],
    [data-testid="stCaptionContainer"],
    [data-testid="stAlert"],
    .hero-banner,
    .result-box,
    .listing-card {{
        direction: rtl !important;
        text-align: right !important;
    }}
    [data-testid="stWidgetLabel"] {{
        direction: rtl !important;
        text-align: right !important;
        width: 100% !important;
        display: flex !important;
        justify-content: flex-start !important;
    }}
    [data-testid="stWidgetLabel"] p {{
        text-align: right !important;
        width: 100% !important;
    }}
    [data-testid="stRadio"],
    [data-testid="stSelectbox"],
    [data-testid="stNumberInput"] {{
        direction: rtl !important;
        text-align: right !important;
        width: 100% !important;
    }}
    [data-testid="stRadio"] > div[role="radiogroup"] {{
        direction: rtl !important;
        justify-content: flex-start !important;
        width: 100% !important;
    }}
    [data-testid="stMetric"] {{
        direction: rtl !important;
        text-align: right !important;
        background: rgba(255, 255, 255, 0.92);
        padding: 0.85rem 1rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }}
    [data-baseweb="tab-list"] {{
        direction: rtl !important;
        justify-content: flex-start !important;
        gap: 0.75rem;
        background: rgba(255, 255, 255, 0.82);
        backdrop-filter: blur(8px);
        padding: 0.45rem 0.75rem;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
    }}
    [data-baseweb="select"] > div {{
        direction: rtl !important;
        text-align: right !important;
    }}
    /* تنسيق البطاقات الزجاجية التي تحتوي المدخلات */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.90);
        backdrop-filter: blur(10px);
        border-radius: 16px !important;
        border: 1px solid rgba(203, 213, 225, 0.85) !important;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
        padding: 0.35rem 0.45rem;
    }}
    .hero-banner {{
        {hero_bg_css}
        padding: 2.4rem 2.5rem;
        border-radius: 18px;
        color: #ffffff;
        margin-bottom: 1.4rem;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.22);
        border-bottom: 4px solid #f59e0b;
    }}
    .hero-badge {{
        display: inline-block;
        background: rgba(245, 158, 11, 0.22);
        color: #fde68a;
        border: 1px solid rgba(245, 158, 11, 0.55);
        padding: 0.25rem 0.9rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }}
    .hero-title {{
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 0.45rem 0;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.35);
    }}
    .hero-sub {{
        font-size: 1.02rem;
        color: #e2e8f0;
        margin: 0;
    }}
    .section-title {{
        font-size: 1.08rem;
        font-weight: 800;
        color: #0f3d3e;
        margin-bottom: 0.65rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.45rem;
    }}
    .result-box {{
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(10px);
        border: 1.5px solid #0f766e;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 8px 24px rgba(15, 118, 110, 0.12);
    }}
    .listing-card {{
        background: rgba(255, 255, 255, 0.94);
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.15rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
        border-top: 4px solid #0f766e;
    }}
    .listing-price {{
        font-size: 1.32rem;
        font-weight: 800;
        color: #0f3d3e;
        margin-bottom: 0.35rem;
    }}
    .listing-meta {{
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.7;
    }}
    .tier-pill-luxury {{
        display: inline-block;
        background: #fef3c7;
        color: #b45309;
        padding: 0.2rem 0.75rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.85rem;
    }}
    .tier-pill-std {{
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 0.2rem 0.75rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.85rem;
    }}
    div.stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, #0f766e 0%, #0f3d3e 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-size: 1.08rem;
        font-weight: 700;
        box-shadow: 0 4px 14px rgba(15, 118, 110, 0.28);
    }}
    div.stButton > button[kind="primary"]:hover {{
        background: linear-gradient(90deg, #115e59 0%, #0f172a 100%);
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_bundle(path="real_estate_bundle.joblib"):
    return joblib.load(path)

@st.cache_data
def load_market_data(path="real_estate_cleaned.csv"):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

try:
    bundle = load_bundle()
    reg_model = bundle["reg_model"]
    rf_model = bundle.get("rf_model")
    clf_model = bundle["clf_model"]
    scaler = bundle["scaler"]
    feature_columns = bundle["feature_columns"]
    median_threshold = bundle["median_threshold"]
except FileNotFoundError:
    st.error("لم يتم العثور على ملف `real_estate_bundle.joblib`. شغّل نوتبوك Colab أولاً ثم ضع الملف بجانب `app_streamlit.py`.")
    st.stop()

market_df = load_market_data()

# 4. الترويسة الرئيسية 
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">بوابة التقييم العقاري الذكي · CYSTECH</div>
    <div class="hero-title">🏡 اكتشف القيمة السوقية الحقيقية لعقارك بالذكاء الاصطناعي</div>
    <p class="hero-sub">منصة تفاعلية لتسعير العقارات، تصنيف الفخامة، ومقارنة العقار بعروض السوق المشابهة — إعداد م. تسنيم الأعرج</p>
</div>
""", unsafe_allow_html=True)

# 5. تبويبات الموقع التفاعلية 
tab_predict, tab_market, tab_about = st.tabs([
    "🏡 قيّم عقارك الآن",
    "📊 مستكشف السوق العقاري",
    "ℹ️ عن النماذج والنظام"
])

with tab_predict:
    # ترتيب الأعمدة من اليمين إلى اليسار بصرياً: المساحة (يمين) -> المزايا (وسط) -> الموقع (يسار)
    col_left, col_mid, col_right = st.columns(3, gap="medium")

    with col_right:
        with st.container(border=True):
            st.markdown('<div class="section-title">📐 1. المساحة والبناء</div>', unsafe_allow_html=True)
            square_meters = st.slider("المساحة الإجمالية (م²)", min_value=50, max_value=350, value=165, step=5)
            num_bedrooms = st.number_input("عدد غرف النوم", min_value=1, max_value=7, value=3, step=1)
            num_bathrooms = st.number_input("عدد الحمامات", min_value=1, max_value=5, value=2, step=1)
            num_floors = st.number_input("عدد الطوابق", min_value=1, max_value=4, value=2, step=1)
            year_built = st.slider("سنة البناء", min_value=1900, max_value=2026, value=2016, step=1)

    with col_mid:
        with st.container(border=True):
            st.markdown('<div class="section-title">✨ 2. المزايا والرفاهية</div>', unsafe_allow_html=True)
            has_garden = st.radio("هل يحتوي على حديقة؟", options=["نعم (1)", "لا (0)"], horizontal=True)
            has_pool = st.radio("هل يحتوي على مسبح؟", options=["لا (0)", "نعم (1)"], horizontal=True)
            garage_area = st.slider("مساحة الكراج (م²)", min_value=10, max_value=50, value=24, step=1)

    with col_left:
        with st.container(border=True):
            st.markdown('<div class="section-title">📍 3. الموقع والمنطقة</div>', unsafe_allow_html=True)
            location_score = st.slider("تقييم حيوية الموقع (من 1 إلى 10)", min_value=1.0, max_value=10.0, value=7.2, step=0.1)
            urban_zone = st.selectbox(
                "النطاق العمراني",
                options=["Urban_Core (<5km)", "Suburban (5-12km)", "Outskirts (>12km)"],
                index=1
            )
            location_tier = st.selectbox(
                "تصنيف المنطقة",
                options=["Prime_Score (7-10)", "Mid_Score (3.5-7)", "Low_Score (0-3.5)"],
                index=0
            )

    predict_clicked = st.button("احسب التقييم العقاري الفوري", type="primary", use_container_width=True)

    if predict_clicked:
        garden_val = 1 if "1" in has_garden else 0
        pool_val = 1 if "1" in has_pool else 0

        user_house = pd.DataFrame([{
            "Square_Meters": square_meters,
            "Num_Bedrooms": num_bedrooms,
            "Num_Bathrooms": num_bathrooms,
            "Num_Floors": num_floors,
            "Year_Built": year_built,
            "Has_Garden": garden_val,
            "Has_Pool": pool_val,
            "Garage_Area_SqM": garage_area,
            "Location_Score": location_score,
            "Urban_Zone": urban_zone,
            "Location_Tier": location_tier,
        }])

        user_encoded = pd.get_dummies(
            user_house,
            columns=["Urban_Zone", "Location_Tier"],
            dtype=int
        ).reindex(columns=feature_columns, fill_value=0)

        user_scaled = scaler.transform(user_encoded)

        pred_lr = float(reg_model.predict(user_scaled)[0])
        pred_rf = float(rf_model.predict(user_scaled)[0]) if rf_model is not None else None
        pred_class = int(clf_model.predict(user_scaled)[0])
        pred_prob = float(clf_model.predict_proba(user_scaled)[0][1] * 100)
        price_per_sqm = pred_lr / max(1, square_meters)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.subheader("📋 تقرير التقييم العقاري الفوري")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("احتمالية تصنيف الفخامة", f"{pred_prob:.1f}%")
        m2.metric("سعر المتر المربع التقديري", f"${price_per_sqm:,.0f} / م²")
        if pred_rf is not None:
            m3.metric("تقدير الغابة العشوائية (Random Forest)", f"${pred_rf:,.0f}")
        else:
            m3.metric("عتبة الفخامة بالسوق", f"${median_threshold:,.0f}")
        m4.metric("السعر التقديري (Linear Regression)", f"${pred_lr:,.0f}")

        pill = '<span class="tier-pill-luxury">🌟 عقار فاخر (Luxury)</span>' if pred_class == 1 else '<span class="tier-pill-std">🏘️ عقار قياسي (Standard)</span>'
        st.markdown(f"**التصنيف السوقي المتوقع:** {pill} &nbsp;|&nbsp; *(تُقارن النتيجة بوسيط السوق البالغ ${median_threshold:,.0f})*", unsafe_allow_html=True)
        st.progress(min(100, max(0, int(round(pred_prob)))) / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

        if market_df is not None:
            st.markdown("### 🏘️ عقارات مشابهة في السوق")
            same_zone = market_df[market_df["Urban_Zone"] == urban_zone].copy()
            pool_df = same_zone if len(same_zone) >= 3 else market_df.copy()
            pool_df["diff"] = (pool_df["Square_Meters"] - square_meters).abs()
            comps = pool_df.nsmallest(3, "diff")

            c_cols = st.columns(3, gap="medium")
            for idx, (_, row) in enumerate(comps.iterrows()):
                with c_cols[2 - idx]:
                    garden_txt = "حديقة" if row.get("Has_Garden", 0) == 1 else "بدون حديقة"
                    pool_txt = "مسبح" if row.get("Has_Pool", 0) == 1 else "بدون مسبح"
                    st.markdown(f"""
                    <div class="listing-card">
                        <div class="listing-price">${row['Price']:,.0f}</div>
                        <div class="listing-meta">
                            📐 <strong>{row['Square_Meters']:.0f} م²</strong> · 🛏️ {int(row['Num_Bedrooms'])} غرف · 🚿 {int(row['Num_Bathrooms'])} حمامات<br>
                            📍 {row['Urban_Zone']} · {row['Location_Tier']}<br>
                            🌿 {garden_txt} · 🏊 {pool_txt} · بناء {int(row['Year_Built'])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

with tab_market:
    if market_df is None:
        st.info("ضع ملف `real_estate_cleaned.csv` في نفس المجلد لتفعيل مستكشف السوق التفاعلي.")
    else:
        with st.container(border=True):
            st.subheader("🔎 تصفية واستكشاف عقارات السوق")
            f1, f2 = st.columns(2)
            zones = ["الكل"] + sorted(market_df["Urban_Zone"].dropna().unique().tolist())
            tiers = ["الكل"] + sorted(market_df["Location_Tier"].dropna().unique().tolist())
            sel_tier = f1.selectbox("تصفية حسب تصنيف الموقع", tiers)
            sel_zone = f2.selectbox("تصفية حسب النطاق العمراني", zones)

            filtered = market_df.copy()
            if sel_zone != "الكل":
                filtered = filtered[filtered["Urban_Zone"] == sel_zone]
            if sel_tier != "الكل":
                filtered = filtered[filtered["Location_Tier"] == sel_tier]

            k1, k2, k3 = st.columns(3)
            k1.metric("متوسط المساحة", f"{filtered['Square_Meters'].mean():,.0f} م²" if len(filtered) else "—")
            k2.metric("متوسط السعر", f"${filtered['Price'].mean():,.0f}" if len(filtered) else "—")
            k3.metric("عدد العقارات المطابقة", f"{len(filtered)}")

            if len(filtered):
                st.markdown("**متوسط الأسعار حسب تصنيف الموقع:**")
                chart_df = filtered.groupby("Location_Tier")["Price"].mean().sort_values(ascending=False)
                st.bar_chart(chart_df, color="#0f766e")
                st.dataframe(
                    filtered[["Square_Meters", "Num_Bedrooms", "Num_Bathrooms", "Year_Built", "Urban_Zone", "Location_Tier", "Price"]].head(15),
                    use_container_width=True,
                )

with tab_about:
    with st.container(border=True):
        st.subheader("⚙️ كيف يعمل النظام من الداخل؟")
        st.markdown("""
        - **حزمة النموذج (`real_estate_bundle.joblib`):** تضم نماذج `LinearRegression` و `RandomForestRegressor` و `LogisticRegression` بالإضافة إلى أداة `StandardScaler` وقائمة الأعمدة الـ `13` بالترتيب الدقيق.
        - **منع تسريب البيانات (`Leakage-Free`):** تمر مدخلات المستخدم أولاً عبر `pd.get_dummies` ثم `reindex` وأخيراً `scaler.transform` باستخدام إحصائيات التدريب المحفوظة.
        - **إدارة وتشغيل محلي:** يعمل التطبيق بالكامل محلياً عبر `Streamlit` دون إرسال أي بيانات لخوادم خارجية.
        """)