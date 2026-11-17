import joblib
import pandas as pd
import gradio as gr

# 1. تحميل حزمة النموذج المحفوظة (Model Bundle)
bundle = joblib.load("real_estate_bundle.joblib")
reg_model = bundle["reg_model"]
clf_model = bundle["clf_model"]
scaler = bundle["scaler"]
feature_columns = bundle["feature_columns"]
median_threshold = bundle["median_threshold"]

# 2. دالة التنبؤ الرئيسية (Inference Function)
def predict_house(
    square_meters, num_bedrooms, num_bathrooms, year_built,
    has_garden, has_pool, garage_spaces, renovation_years_ago,
    transit_km, urban_zone, location_tier
):
    garden_val = 1 if has_garden == "نعم (1)" else 0
    pool_val = 1 if has_pool == "نعم (1)" else 0

    user_df = pd.DataFrame([{
        "Square_Meters": square_meters,
        "Num_Bedrooms": num_bedrooms,
        "Num_Bathrooms": num_bathrooms,
        "Year_Built": year_built,
        "Has_Garden": garden_val,
        "Has_Pool": pool_val,
        "Garage_Spaces": garage_spaces,
        "Renovation_Years_Ago": renovation_years_ago,
        "Proximity_to_Transit_km": transit_km,
        "Urban_Zone": urban_zone,
        "Location_Tier": location_tier,
    }])

    user_encoded = pd.get_dummies(
        user_df,
        columns=["Urban_Zone", "Location_Tier"],
        drop_first=True,
        dtype=int
    ).reindex(columns=feature_columns, fill_value=0)

    user_scaled = scaler.transform(user_encoded)

    predicted_price = float(reg_model.predict(user_scaled)[0])
    luxury_prob = float(clf_model.predict_proba(user_scaled)[0][1] * 100)
    tier_label = "عقار فاخر (Luxury)" if clf_model.predict(user_scaled)[0] == 1 else "عقار قياسي (Standard)"

    return (
        f"${predicted_price:,.0f}",
        f"{tier_label} — بنسبة ثقة {luxury_prob:.1f}% (العتبة: ${median_threshold:,.0f})"
    )

# 3. بناء واجهة Gradio التفاعلية
demo = gr.Interface(
    fn=predict_house,
    inputs=[
        gr.Slider(40, 350, value=160, step=5, label="المساحة (Square_Meters)"),
        gr.Slider(1, 7, value=3, step=1, label="عدد غرف النوم (Num_Bedrooms)"),
        gr.Slider(1, 5, value=2, step=1, label="عدد الحمامات (Num_Bathrooms)"),
        gr.Slider(1960, 2025, value=2015, step=1, label="سنة البناء (Year_Built)"),
        gr.Radio(["لا (0)", "نعم (1)"], value="نعم (1)", label="حديقة (Has_Garden)"),
        gr.Radio(["لا (0)", "نعم (1)"], value="لا (0)", label="مسبح (Has_Pool)"),
        gr.Slider(0, 4, value=1, step=1, label="مواقف السيارات (Garage_Spaces)"),
        gr.Slider(0, 50, value=5, step=1, label="سنوات منذ التجديد (Renovation_Years_Ago)"),
        gr.Slider(0.1, 10.0, value=1.5, step=0.1, label="البعد عن المواصلات كم (Proximity_to_Transit_km)"),
        gr.Dropdown(["Urban_Core (<5km)", "Suburban (5-12km)", "Outskirts (>12km)"], value="Suburban (5-12km)", label="النطاق العمراني (Urban_Zone)"),
        gr.Dropdown(["Prime_Score (7-10)", "Mid_Score (3.5-7)", "Low_Score (0-3.5)"], value="Prime_Score (7-10)", label="تصنيف الموقع (Location_Tier)"),
    ],
    outputs=[
        gr.Textbox(label="السعر التقديري للعقار (Predicted Price)"),
        gr.Textbox(label="تصنيف الفخامة (Luxury Tier & Confidence)"),
    ],
    title="نظام التنبؤ بأسعار العقارات — Gradio Local App",
    description="تطبيق محلي تفاعلي يربط واجهة Gradio بنموذج تعلم الآلة المحفوظ عبر joblib | م. تسنيم الأعرج — CYSTECH",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()