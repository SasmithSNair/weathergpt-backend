# Starter seed for offline location search: every state & UT capital, plus
# a spread of major cities per state. NOT an exhaustive list of every town in
# India — that would need a bulk import from an official gazetteer (e.g. the
# Survey of India / Census place-code dataset). This gives immediate,
# reasonably wide offline coverage and is designed to be extended by bulk
# INSERT later without touching any code.

INDIA_LOCATIONS = [
    # Andhra Pradesh
    {"name": "Amaravati", "state": "Andhra Pradesh", "district": "Guntur", "lat": 16.5417, "lon": 80.5150},
    {"name": "Visakhapatnam", "state": "Andhra Pradesh", "district": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185},
    {"name": "Vijayawada", "state": "Andhra Pradesh", "district": "Krishna", "lat": 16.5062, "lon": 80.6480},
    {"name": "Tirupati", "state": "Andhra Pradesh", "district": "Tirupati", "lat": 13.6288, "lon": 79.4192},
    # Arunachal Pradesh
    {"name": "Itanagar", "state": "Arunachal Pradesh", "district": "Papum Pare", "lat": 27.0844, "lon": 93.6053},
    # Assam
    {"name": "Dispur", "state": "Assam", "district": "Kamrup", "lat": 26.1433, "lon": 91.7898},
    {"name": "Guwahati", "state": "Assam", "district": "Kamrup Metropolitan", "lat": 26.1445, "lon": 91.7362},
    {"name": "Silchar", "state": "Assam", "district": "Cachar", "lat": 24.8333, "lon": 92.7789},
    # Bihar
    {"name": "Patna", "state": "Bihar", "district": "Patna", "lat": 25.5941, "lon": 85.1376},
    {"name": "Gaya", "state": "Bihar", "district": "Gaya", "lat": 24.7955, "lon": 84.9994},
    {"name": "Muzaffarpur", "state": "Bihar", "district": "Muzaffarpur", "lat": 26.1225, "lon": 85.3906},
    # Chhattisgarh
    {"name": "Raipur", "state": "Chhattisgarh", "district": "Raipur", "lat": 21.2514, "lon": 81.6296},
    {"name": "Bilaspur", "state": "Chhattisgarh", "district": "Bilaspur", "lat": 22.0797, "lon": 82.1391},
    # Goa
    {"name": "Panaji", "state": "Goa", "district": "North Goa", "lat": 15.4909, "lon": 73.8278},
    # Gujarat
    {"name": "Gandhinagar", "state": "Gujarat", "district": "Gandhinagar", "lat": 23.2156, "lon": 72.6369},
    {"name": "Ahmedabad", "state": "Gujarat", "district": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"name": "Surat", "state": "Gujarat", "district": "Surat", "lat": 21.1702, "lon": 72.8311},
    {"name": "Vadodara", "state": "Gujarat", "district": "Vadodara", "lat": 22.3072, "lon": 73.1812},
    {"name": "Rajkot", "state": "Gujarat", "district": "Rajkot", "lat": 22.3039, "lon": 70.8022},
    # Haryana
    {"name": "Chandigarh", "state": "Haryana", "district": "Chandigarh", "lat": 30.7333, "lon": 76.7794},
    {"name": "Gurugram", "state": "Haryana", "district": "Gurugram", "lat": 28.4595, "lon": 77.0266},
    {"name": "Faridabad", "state": "Haryana", "district": "Faridabad", "lat": 28.4089, "lon": 77.3178},
    # Himachal Pradesh
    {"name": "Shimla", "state": "Himachal Pradesh", "district": "Shimla", "lat": 31.1048, "lon": 77.1734},
    {"name": "Manali", "state": "Himachal Pradesh", "district": "Kullu", "lat": 32.2432, "lon": 77.1892},
    # Jharkhand
    {"name": "Ranchi", "state": "Jharkhand", "district": "Ranchi", "lat": 23.3441, "lon": 85.3096},
    {"name": "Jamshedpur", "state": "Jharkhand", "district": "East Singhbhum", "lat": 22.8046, "lon": 86.2029},
    # Karnataka
    {"name": "Bengaluru", "state": "Karnataka", "district": "Bengaluru Urban", "lat": 12.9716, "lon": 77.5946},
    {"name": "Mysuru", "state": "Karnataka", "district": "Mysuru", "lat": 12.2958, "lon": 76.6394},
    {"name": "Mangaluru", "state": "Karnataka", "district": "Dakshina Kannada", "lat": 12.9141, "lon": 74.8560},
    {"name": "Hubballi", "state": "Karnataka", "district": "Dharwad", "lat": 15.3647, "lon": 75.1240},
    # Kerala
    {"name": "Thiruvananthapuram", "state": "Kerala", "district": "Thiruvananthapuram", "lat": 8.5241, "lon": 76.9366},
    {"name": "Kochi", "state": "Kerala", "district": "Ernakulam", "lat": 9.9312, "lon": 76.2673},
    {"name": "Kozhikode", "state": "Kerala", "district": "Kozhikode", "lat": 11.2588, "lon": 75.7804},
    # Madhya Pradesh
    {"name": "Bhopal", "state": "Madhya Pradesh", "district": "Bhopal", "lat": 23.2599, "lon": 77.4126},
    {"name": "Indore", "state": "Madhya Pradesh", "district": "Indore", "lat": 22.7196, "lon": 75.8577},
    {"name": "Gwalior", "state": "Madhya Pradesh", "district": "Gwalior", "lat": 26.2183, "lon": 78.1828},
    # Maharashtra
    {"name": "Mumbai", "state": "Maharashtra", "district": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Pune", "state": "Maharashtra", "district": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"name": "Nagpur", "state": "Maharashtra", "district": "Nagpur", "lat": 21.1458, "lon": 79.0882},
    {"name": "Nashik", "state": "Maharashtra", "district": "Nashik", "lat": 19.9975, "lon": 73.7898},
    # Manipur
    {"name": "Imphal", "state": "Manipur", "district": "Imphal West", "lat": 24.8170, "lon": 93.9368},
    # Meghalaya
    {"name": "Shillong", "state": "Meghalaya", "district": "East Khasi Hills", "lat": 25.5788, "lon": 91.8933},
    # Mizoram
    {"name": "Aizawl", "state": "Mizoram", "district": "Aizawl", "lat": 23.7271, "lon": 92.7176},
    # Nagaland
    {"name": "Kohima", "state": "Nagaland", "district": "Kohima", "lat": 25.6751, "lon": 94.1086},
    # Odisha
    {"name": "Bhubaneswar", "state": "Odisha", "district": "Khordha", "lat": 20.2961, "lon": 85.8245},
    {"name": "Cuttack", "state": "Odisha", "district": "Cuttack", "lat": 20.4625, "lon": 85.8830},
    # Punjab
    {"name": "Amritsar", "state": "Punjab", "district": "Amritsar", "lat": 31.6340, "lon": 74.8723},
    {"name": "Ludhiana", "state": "Punjab", "district": "Ludhiana", "lat": 30.9010, "lon": 75.8573},
    # Rajasthan
    {"name": "Jaipur", "state": "Rajasthan", "district": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"name": "Jodhpur", "state": "Rajasthan", "district": "Jodhpur", "lat": 26.2389, "lon": 73.0243},
    {"name": "Udaipur", "state": "Rajasthan", "district": "Udaipur", "lat": 24.5854, "lon": 73.7125},
    # Sikkim
    {"name": "Gangtok", "state": "Sikkim", "district": "East Sikkim", "lat": 27.3389, "lon": 88.6065},
    # Tamil Nadu
    {"name": "Chennai", "state": "Tamil Nadu", "district": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"name": "Coimbatore", "state": "Tamil Nadu", "district": "Coimbatore", "lat": 11.0168, "lon": 76.9558},
    {"name": "Madurai", "state": "Tamil Nadu", "district": "Madurai", "lat": 9.9252, "lon": 78.1198},
    {"name": "Salem", "state": "Tamil Nadu", "district": "Salem", "lat": 11.6643, "lon": 78.1460},
    {"name": "Tiruchirappalli", "state": "Tamil Nadu", "district": "Tiruchirappalli", "lat": 10.7905, "lon": 78.7047},
    # Telangana
    {"name": "Hyderabad", "state": "Telangana", "district": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"name": "Warangal", "state": "Telangana", "district": "Warangal", "lat": 17.9784, "lon": 79.6006},
    # Tripura
    {"name": "Agartala", "state": "Tripura", "district": "West Tripura", "lat": 23.8315, "lon": 91.2868},
    # Uttar Pradesh
    {"name": "Lucknow", "state": "Uttar Pradesh", "district": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    {"name": "Kanpur", "state": "Uttar Pradesh", "district": "Kanpur Nagar", "lat": 26.4499, "lon": 80.3319},
    {"name": "Varanasi", "state": "Uttar Pradesh", "district": "Varanasi", "lat": 25.3176, "lon": 82.9739},
    {"name": "Agra", "state": "Uttar Pradesh", "district": "Agra", "lat": 27.1767, "lon": 78.0081},
    {"name": "Noida", "state": "Uttar Pradesh", "district": "Gautam Buddha Nagar", "lat": 28.5355, "lon": 77.3910},
    # Uttarakhand
    {"name": "Dehradun", "state": "Uttarakhand", "district": "Dehradun", "lat": 30.3165, "lon": 78.0322},
    {"name": "Haridwar", "state": "Uttarakhand", "district": "Haridwar", "lat": 29.9457, "lon": 78.1642},
    # West Bengal
    {"name": "Kolkata", "state": "West Bengal", "district": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"name": "Howrah", "state": "West Bengal", "district": "Howrah", "lat": 22.5958, "lon": 88.2636},
    {"name": "Darjeeling", "state": "West Bengal", "district": "Darjeeling", "lat": 27.0410, "lon": 88.2663},
    # Union Territories
    {"name": "New Delhi", "state": "Delhi", "district": "New Delhi", "lat": 28.6139, "lon": 77.2090},
    {"name": "Puducherry", "state": "Puducherry", "district": "Puducherry", "lat": 11.9416, "lon": 79.8083},
    {"name": "Srinagar", "state": "Jammu & Kashmir", "district": "Srinagar", "lat": 34.0837, "lon": 74.7973},
    {"name": "Jammu", "state": "Jammu & Kashmir", "district": "Jammu", "lat": 32.7266, "lon": 74.8570},
    {"name": "Leh", "state": "Ladakh", "district": "Leh", "lat": 34.1526, "lon": 77.5771},
    {"name": "Port Blair", "state": "Andaman & Nicobar Islands", "district": "South Andaman", "lat": 11.6234, "lon": 92.7265},
    {"name": "Kavaratti", "state": "Lakshadweep", "district": "Lakshadweep", "lat": 10.5669, "lon": 72.6420},
    {"name": "Daman", "state": "Dadra & Nagar Haveli and Daman & Diu", "district": "Daman", "lat": 20.3974, "lon": 72.8328},
    # Saravanampatti (added on request — near where this project was built)
    {"name": "Saravanampatti", "state": "Tamil Nadu", "district": "Coimbatore", "lat": 11.0768, "lon": 77.0030},
]
