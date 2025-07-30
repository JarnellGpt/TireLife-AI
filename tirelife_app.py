
import gradio as gr
from datetime import datetime

# Average tread life in km (can vary by tire type)
AVERAGE_TREAD_LIFE_KM = 50000

# Prediction logic
def predict_tire_health(mileage, pressure, last_replacement_date, driving_style):
    # Estimate tread wear
    tread_wear = min((mileage / AVERAGE_TREAD_LIFE_KM) * 100, 100)
    tread_remaining = max(100 - tread_wear, 0)

    # Pressure alert
    pressure_status = "✅ Normal" if 30 <= pressure <= 35 else "⚠️ Check pressure"

    # Months until recommended replacement
    km_per_month = {
        "City": 1000,
        "Highway": 2000,
        "Mixed": 1500
    }.get(driving_style, 1500)

    try:
        last_date = datetime.strptime(last_replacement_date, "%Y-%m-%d")
        months_since_change = (datetime.today().year - last_date.year) * 12 + (datetime.today().month - last_date.month)
    except:
        months_since_change = 0

    estimated_remaining_km = AVERAGE_TREAD_LIFE_KM - mileage
    months_to_replace = max(int(estimated_remaining_km / (km_per_month + 1)), 0)

    recommendation = "✅ Safe for now" if tread_wear < 70 else "🛞 Consider replacing soon"

    return (
        f"Tread Wear: {tread_wear:.1f}%",
        f"Remaining Life: ~{months_to_replace} months",
        f"Pressure Status: {pressure_status}",
        f"Recommendation: {recommendation}"
    )

# Gradio UI
demo = gr.Interface(
    fn=predict_tire_health,
    inputs=[
        gr.Number(label="Mileage Since Last Tire Change (km)", value=10000),
        gr.Number(label="Current Tire Pressure (PSI)", value=32),
        gr.Textbox(label="Last Replacement Date (YYYY-MM-DD)", placeholder="e.g., 2024-06-01"),
        gr.Radio(choices=["City", "Highway", "Mixed"], label="Driving Pattern", value="Mixed")
    ],
    outputs=[
        gr.Text(label="Tread Wear"),
        gr.Text(label="Remaining Life Estimate"),
        gr.Text(label="Pressure Status"),
        gr.Text(label="Maintenance Recommendation")
    ],
    title="🛞 TireLife.AI",
    description="Estimate your tire wear and get smart alerts based on mileage, pressure, and usage."
)

if __name__ == "__main__":
    demo.launch()
