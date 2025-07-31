
import gradio as gr
from datetime import datetime

# Constants
AVERAGE_TREAD_LIFE_KM = 50000

# Prediction logic
def predict_tire_health(mileage, pressure, last_replacement_date, driving_style):
    tread_wear = min((mileage / AVERAGE_TREAD_LIFE_KM) * 100, 100)
    tread_remaining = max(100 - tread_wear, 0)

    pressure_status = "✅ Normal" if 30 <= pressure <= 35 else "⚠️ Check pressure"

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

# Final Gradio 5.x layout
with gr.Blocks() as demo:
    with gr.Column():
        gr.Image(value="banner.png", show_label=False)
        with gr.Row():
            gr.Image(value="tirelife_logo.png", show_label=False, width=40)
            gr.Markdown("## **TireLife.AI** — Predictive Tire Health Assistant")

        gr.Markdown("Get smart tire wear, pressure, and replacement insights in seconds.")

        with gr.Row():
            mileage_input = gr.Number(label="Mileage Since Last Tire Change (km)", value=10000)
            pressure_input = gr.Number(label="Current Tire Pressure (PSI)", value=32)

        with gr.Row():
            last_date_input = gr.Textbox(label="Last Replacement Date (YYYY-MM-DD)", placeholder="e.g., 2024-06-01")
            drive_style_input = gr.Radio(["City", "Highway", "Mixed"], label="Driving Pattern", value="Mixed")

        check_btn = gr.Button("🔍 Run Tire Health Check")

        with gr.Group():
            gr.Markdown("### 📊 Tire Health Overview")
            tread_output = gr.Text(label="Tread Wear")
            life_output = gr.Text(label="Remaining Life Estimate")
            pressure_output = gr.Text(label="Pressure Status")
            tip_output = gr.Text(label="Maintenance Recommendation")

        gr.Markdown("---")
        gr.Markdown("*Built by Jarnell + Sunraku • Powered by Python + Gradio*")

    check_btn.click(fn=predict_tire_health,
                    inputs=[mileage_input, pressure_input, last_date_input, drive_style_input],
                    outputs=[tread_output, life_output, pressure_output, tip_output])

if __name__ == "__main__":
    demo.launch()
