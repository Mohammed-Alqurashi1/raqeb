import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from hijri_converter import convert

# Define the location data
location_data = {
    'Floor Level': [
        'صحن المطاف', 'الدور الاول', 'الدور الثاني', 'السطح', 
        'مطاف العربات', 'الدور الاول (المسعى)', 'الدور الثاني (المسعى)', 
        'السطح (المسعى)', 'مسار العربات (المسعى)'
    ],
    'location_id': range(1, 10)
}

location_df = pd.DataFrame(location_data)

# Define the density ranges based on the provided specifications
density_ranges = {
    1: (5000, 15000),      # صحن المطاف
    2: (3000, 8000),      # الدور الاول
    3: (1500, 5200),      # الدور الثاني
    4: (500, 3000),      # السطح
    5: (200, 1000),       # مطاف العربات
    6: (3000, 12000),      # الدور الاول (المسعى)
    7: (2000, 5000),      # الدور الثاني (المسعى)
    8: (800, 2000),      # السطح (المسعى)
    9: (300, 700)       # مسار العربات (المسعى)
}

# Hijri months percentages
hijri_month_percentages = {
    'محرم': 0.20,
    'صفر': 0.17,
    'ربيع الأول': 0.14,
    'ربيع الثاني': 0.12,
    'جمادى الأول': 0.10,
    'جمادى الثاني': 0.08,
    'رجب': 0.23,
    'شعبان': 0.30,
    'رمضان': 0.39,
    'شوال': 0.28,
    'ذو القعدة': 0.33,
    'ذو الحجة': 0.44
}

# Define the date ranges for each Hijri month in 1445
hijri_month_ranges = {
    'محرم': ('1445-01-01', '1445-01-29'),
    'صفر': ('1445-02-01', '1445-02-29'),
    'ربيع الأول': ('1445-03-01', '1445-03-29'),
    'ربيع الثاني': ('1445-04-01', '1445-04-29'),
    'جمادى الأول': ('1445-05-01', '1445-05-29'),
    'جمادى الثاني': ('1445-06-01', '1445-06-29'),
    'رجب': ('1445-07-01', '1445-07-29'),
    'شعبان': ('1445-08-01', '1445-08-29'),
    'رمضان': ('1445-09-01', '1445-09-29'),
    'شوال': ('1445-10-01', '1445-10-29'),
    'ذو القعدة': ('1445-11-01', '1445-11-29'),
    'ذو الحجة': ('1445-12-01', '1445-12-29')
}

counts = []
dates_hijri = []
times = []
location_ids_expanded = []

for month, date_range in hijri_month_ranges.items():
    start_date_hijri = convert.Hijri(int(date_range[0].split('-')[0]), int(date_range[0].split('-')[1]), int(date_range[0].split('-')[2])).to_gregorian()
    end_date_hijri = convert.Hijri(int(date_range[1].split('-')[0]), int(date_range[1].split('-')[1]), int(date_range[1].split('-')[2])).to_gregorian()
    
    # Verify the date range
    if end_date_hijri < start_date_hijri:
        continue
    
    date_range = pd.date_range(start=start_date_hijri, end=end_date_hijri, freq='H')
    
    percentage = hijri_month_percentages[month]
    
    for single_date in date_range:
        for location_id in range(1, 10):
            count_range = density_ranges[location_id]
            
            hour = single_date.hour
            if 10 <= hour < 16:  # From 10:00 to 16:00
                adjusted_range = (max(int(count_range[0] * percentage), 1), max(int(count_range[1] * percentage), 1))
            elif 20 <= hour < 24:  # Evening/Night
                adjusted_range = (count_range[0], min(int(count_range[1] * percentage * 2), count_range[1]))
            else:
                adjusted_range = count_range

            if adjusted_range[0] > adjusted_range[1]:  # Fix the range if needed
                adjusted_range = (adjusted_range[1], adjusted_range[1])

            count = random.randint(*adjusted_range)
            
            hijri_date = convert.Gregorian(single_date.year, single_date.month, single_date.day).to_hijri()
            
            counts.append(count)
            dates_hijri.append(f"{hijri_date.year}-{hijri_date.month:02d}-{hijri_date.day:02d}")
            times.append(single_date.strftime("%H:%M"))
            location_ids_expanded.append(location_id)

# Create the Crowd dataframe
crowd_df = pd.DataFrame({
    'count': counts,
    'date_hijri': dates_hijri,
    'time': times,
    'location_id': location_ids_expanded
})

# Write to Excel file with two sheets: Location and Crowd
output_file = 'umrah_crowd_hijri_1445.xlsx'
with pd.ExcelWriter(output_file) as writer:
    location_df.to_excel(writer, sheet_name='Location', index=False)
    crowd_df.to_excel(writer, sheet_name='Crowd', index=False)

print(f"Data has been written to {output_file}")