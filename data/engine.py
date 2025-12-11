# data/engine.py
import pandas as pd
import numpy as np
# import geopandas as gpd
import requests
from datetime import datetime, timedelta
from faker import Faker
import warnings
from functools import lru_cache
# Suppress warnings
warnings.filterwarnings("ignore")

@lru_cache(maxsize=1)
def load_data():
    print("Initializing Optick Data Engine (Facility Management Context)...")
    print("Loading data from source...")
    fake = Faker('en_IN')
    Faker.seed(42)
    np.random.seed(42)

    # --- Configuration ---
    num_employees = 5000
    
    # Real FM Locations
    location_map = {
        'Maharashtra': {'city': ['Mumbai', 'Pune', 'Nagpur'], 'zone': 'West'},
        'Karnataka': {'city': ['Bangalore', 'Mysore'], 'zone': 'South'},
        'Tamil Nadu': {'city': ['Chennai', 'Coimbatore'], 'zone': 'South'},
        'Telangana': {'city': ['Hyderabad'], 'zone': 'South'},
        'Delhi': {'city': ['New Delhi'], 'zone': 'North'},
        'Haryana': {'city': ['Gurugram', 'Manesar'], 'zone': 'North'},
        'Gujarat': {'city': ['Ahmedabad', 'Vadodara'], 'zone': 'West'},
        'West Bengal': {'city': ['Kolkata'], 'zone': 'East'}
    }
    states = list(location_map.keys())

    # --- Generate Facility Sites ---
    site_data = []
    # FM Site types: Corporate Offices, Warehouses, Data Centers, Malls
    site_types = ['Corporate Tower', 'Logistics Hub', 'Data Center', 'MFG Plant', 'Tech Campus']
    
    for state in states:
        cities = location_map[state]['city']
        zone = location_map[state]['zone']
        for i in range(np.random.randint(4, 7)):
            city = np.random.choice(cities)
            s_type = np.random.choice(site_types)
            site_name = f"{city} {s_type} {chr(65+i)}" # e.g., "Mumbai Data Center A"
            
            # FM specific categories
            category = np.random.choice(['Critical (24x7)', 'Standard (Day)', 'Remote'], p=[0.3, 0.6, 0.1])
            is_hp = True if s_type in ['Data Center', 'Corporate Tower'] else False
            
            site_data.append({
                'Site_Name': site_name, 'State': state, 'City': city, 'Zone': zone, 
                'Category': category, 'High_Profile': is_hp
            })
    df_sites = pd.DataFrame(site_data)

    # --- Generate FM Workforce ---
    # Departments in FM
    depts = ['Engineering (Hard Services)', 'Soft Services', 'Security', 'EHS (Health & Safety)', 'Administration']
    
    role_map = {
        'Engineering (Hard Services)': ['HVAC Technician', 'Electrician', 'Plumber', 'BMS Operator', 'Maintenance Lead', 'Chief Engineer'],
        'Soft Services': ['Housekeeping Steward', 'HK Supervisor', 'Pantry Staff', 'Horticulturist', 'Soft Services Manager'],
        'Security': ['Security Guard', 'CCTV Operator', 'Security Supervisor', 'Security Officer'],
        'EHS (Health & Safety)': ['Fire Safety Officer', 'EHS Executive', 'Safety Marshall'],
        'Administration': ['Front Desk Executive', 'Mailroom Assistant', 'Helpdesk Coordinator', 'Facility Manager', 'Cluster Head']
    }

    grades = ['L1 (Associate)', 'L2 (Skilled)', 'L3 (Supervisor)', 'L4 (Manager)', 'L5 (Director)']
    
    # FM Skills
    skills_pool = [
        'HVAC Maintenance', 'Electrical Safety', 'Fire Safety', 'Crowd Mgmt', 
        'Waste Mgmt', 'Vendor Mgmt', 'Project Mgmt', 'First Aid/CPR', 'BMS Systems'
    ]

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*5)
    
    emp_list = []
    print(f"Generating {num_employees} FM records...")
    
    for i in range(num_employees):
        dept = np.random.choice(depts, p=[0.3, 0.35, 0.2, 0.05, 0.1])
        role = np.random.choice(role_map[dept])
        
        # Gender skew in certain FM roles (Realistic)
        if dept in ['Security', 'Engineering (Hard Services)']:
            gender = np.random.choice(['Male', 'Female'], p=[0.9, 0.1])
        elif dept == 'Administration':
            gender = np.random.choice(['Male', 'Female'], p=[0.4, 0.6])
        else:
            gender = np.random.choice(['Male', 'Female'], p=[0.6, 0.4])

        if gender == 'Male':
            name = f"{fake.first_name_male()} {fake.last_name()}"
        else:
            name = f"{fake.first_name_female()} {fake.last_name()}"
            
        site = df_sites.sample(1).iloc[0]
        
        # Grade logic
        if 'Manager' in role or 'Head' in role or 'Chief' in role:
            grade = np.random.choice(['L4 (Manager)', 'L5 (Director)'])
        elif 'Supervisor' in role or 'Officer' in role or 'Lead' in role:
            grade = 'L3 (Supervisor)'
        elif 'Technician' in role or 'Operator' in role or 'Executive' in role:
            grade = 'L2 (Skilled)'
        else:
            grade = 'L1 (Associate)'

        # Shifts (Crucial for FM)
        if site['Category'] == 'Critical (24x7)' and grade in ['L1 (Associate)', 'L2 (Skilled)', 'L3 (Supervisor)']:
            shift = np.random.choice(['General', 'Morning', 'Evening', 'Night'], p=[0.1, 0.3, 0.3, 0.3])
        else:
            shift = 'General'

        # Join Date & Turnover (High turnover in L1/L2)
        join_date = fake.date_between(start_date=start_date, end_date=end_date)
        join_date = pd.to_datetime(join_date)
        
        # Churn rate higher for Blue collar
        churn_prob = 0.25 if grade in ['L1 (Associate)', 'L2 (Skilled)'] else 0.10
        status = np.random.choice(['Active', 'Resigned'], p=[1-churn_prob, churn_prob])
        
        resignation_date = None
        if status == 'Resigned':
            resignation_date = join_date + timedelta(days=np.random.randint(30, 600))
            if resignation_date > end_date: 
                resignation_date = end_date
                status = 'Active'

        # Experience
        tenure_days = (end_date - join_date).days
        tenure_years = round(tenure_days / 365, 1)
        prior_exp = np.random.randint(0, 15)
        total_exp = round(tenure_years + prior_exp, 1)

        emp_list.append({
            'Emp_ID': f"FM-{50000+i}",
            'Name': name,
            'Role': role,
            'Department': dept, # New field
            'Grade': grade,
            'Gender': gender,
            'Site_Name': site['Site_Name'],
            'City': site['City'],
            'State': site['State'],
            'Zone': site['Zone'],
            'Category': site['Category'], # Site Criticality
            'Is_High_Profile': site['High_Profile'],
            'Join_Date': join_date,
            'Status': status,
            'Resignation_Date': resignation_date,
            'Compliance_Score': np.random.randint(70, 100), # Renamed from Rating
            'Shift': shift, # New Field
            'Software_User': np.random.choice(['Yes', 'No'], p=[0.4, 0.6]), # CAFM usage
            'Education': np.random.choice(['10th Pass', '12th Pass', 'Diploma', 'ITI', 'Graduate', 'MBA'], 
                                          p=[0.1, 0.1, 0.3, 0.2, 0.25, 0.05]),
            'Primary_Skill': np.random.choice(skills_pool),
            'Tenure_Years': tenure_years,
            'Total_Experience': total_exp
        })

    df = pd.DataFrame(emp_list)
    df['Join_Month_Year'] = df['Join_Date'].dt.to_period('M').astype(str)
    
    # Mapping 'Compliance_Score' back to 'Rating' for compatibility with existing charts if needed, 
    # or just keeping it distinct. Let's alias it for safety.
    df['Rating'] = (df['Compliance_Score'] / 20).round(1) # Scale 100 down to 5 for compatibility

    # --- Map Data ---
    india_geojson = None
    try:
        import json
        import os
        
        # Use local file path
        # Assuming script execution root is /home/parzival/analytics/ or we use absolute path
        # Using concise absolute path for reliability in this environment
        base_dir = os.path.dirname(os.path.abspath(__file__))
        geojson_path = os.path.join(base_dir, "india_states_optimized.geojson")
        
        # DEBUG LOGGING
        print(f"DEBUG: base_dir: {base_dir}")
        print(f"DEBUG: geojson_path: {geojson_path}")
        print(f"DEBUG: Files in data dir: {os.listdir(base_dir)}")
        
        with open(geojson_path, 'r') as f:
             india_geojson = json.load(f)
        
        # Rename logic for JSON (Manual fix since we aren't using GPD anymore)
        for feature in india_geojson['features']:
            if feature['properties']['NAME_1'] == 'NCT of Delhi':
                feature['properties']['NAME_1'] = 'Delhi'
                
    except Exception as e:
        print(f"Map Data Load Failed: {e}")

    print("Facility Management Data Generation Complete.")
    return df, india_geojson
