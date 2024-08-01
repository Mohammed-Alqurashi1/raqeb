import streamlit as st
from ultralytics import YOLO
import pandas as pd
from datetime import datetime
from PIL import Image
import io

# Load YOLOv8 model
model = YOLO(r"C:\Users\moham\Desktop\hacathon\best (1).pt")

# Streamlit interface
st.title("People Detection in Umrah at Makkah Holy Mosque")

# File upload
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Perform inference on the uploaded image
    results = model.predict(image, imgsz=800)  # Reduced resolution for better memory management

    # Display results
    st.subheader("Detection Results")
    for result in results:
        result.show()  # Display the result image with detections

    # Count the number of people detected
    people_count = sum([len(result.boxes) for result in results])
    
    # Save the count with the current date and time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    counts = [[people_count, current_time]]

    # Save counts to an Excel file
    df = pd.DataFrame(counts, columns=['Count', 'DateTime'])
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
    excel_file.seek(0)

    # Display the count and provide download link for the Excel file
    st.subheader("Detection Count")
    st.write(f"Number of people detected: {people_count}")
    st.download_button(label="Download Counts Excel", data=excel_file, file_name="people_counts.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
