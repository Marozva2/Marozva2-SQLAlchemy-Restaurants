# seed.py
from models import Restaurant, Customer, Review ,session, restaurants_customers

# Clear existing data
session.query(Restaurant).delete()
session.query(Customer).delete()
session.query(Review).delete()
session.query(restaurants_customers).delete()
session.commit()

# Seed restaurants
restaurants_info = [
    {"id": 1, "name": "Spicy Elegance", "price": 28.45},
    {"id": 2, "name": "Savorful Symphony", "price": 24.80},
    {"id": 3, "name": "Gastronomic Delight", "price": 19.99},
    {"id": 4, "name": "Culinary Oasis", "price": 32.75},
    {"id": 5, "name": "Divine Temptations", "price": 27.25},
    {"id": 6, "name": "Harmony of Flavors", "price": 31.50},
    {"id": 7, "name": "Epicurean Marvel", "price": 23.65},
    {"id": 8, "name": "Pleasure Palette", "price": 26.99},
    {"id": 9, "name": "Exquisite Delicacies", "price": 22.75},
    {"id": 10, "name": "Blazing Zest", "price": 20.50}
]
session.add_all([Restaurant(**restaurant) for restaurant in restaurants_info])
session.commit()

# Seed customers
customers_info = [
    {"id": 1, "first_name": "Marozva", "last_name": "Chitakunye"},
    {"id": 2, "first_name": "Ruvimbo", "last_name": "Makoni"},
    {"id": 3, "first_name": "Farai", "last_name": "Mukonoweshuro"},
    {"id": 4, "first_name": "Tanatswa", "last_name": "Mazani"},
    {"id": 5, "first_name": "Tinashe", "last_name": "Chisango"},
    {"id": 6, "first_name": "Chiedza", "last_name": "Nyamande"},
    {"id": 7, "first_name": "Tawanda", "last_name": "Mutasa"},
    {"id": 8, "first_name": "Ruvarashe", "last_name": "Denga"},
    {"id": 9, "first_name": "Kudakwashe", "last_name": "Chigumira"},
    {"id": 10, "first_name": "Tatenda", "last_name": "Mushore"}
]
session.add_all([Customer(**customer) for customer in customers_info])
session.commit()

# Seed reviews
review_info = [
    {"id": 1, "rating": 4.3, "customer_id": 3, "restaurant_id": 7},
    {"id": 2, "rating": 5.0, "customer_id": 8, "restaurant_id": 2},
    {"id": 3, "rating": 3.7, "customer_id": 5, "restaurant_id": 9},
    {"id": 4, "rating": 4.8, "customer_id": 2, "restaurant_id": 4},
    {"id": 5, "rating": 2.5, "customer_id": 10, "restaurant_id": 6},
    {"id": 6, "rating": 4.1, "customer_id": 1, "restaurant_id": 3},
    {"id": 7, "rating": 3.9, "customer_id": 9, "restaurant_id": 8},
    {"id": 8, "rating": 4.5, "customer_id": 4, "restaurant_id": 1},
    {"id": 9, "rating": 2.8, "customer_id": 7, "restaurant_id": 5},
    {"id": 10, "rating": 4.0, "customer_id": 6, "restaurant_id": 10}
]
for review in review_info:
    new_review = Review(**review)
    session.add(new_review)
session.commit()

# Associate customers with restaurants
data = [
    {"id": 1, "restaurant_id": 5, "customer_id": 3},
    {"id": 2, "restaurant_id": 8, "customer_id": 7},
    {"id": 3, "restaurant_id": 2, "customer_id": 1},
    {"id": 4, "restaurant_id": 6, "customer_id": 9},
    {"id": 5, "restaurant_id": 3, "customer_id": 2},
    {"id": 6, "restaurant_id": 9, "customer_id": 8},
    {"id": 7, "restaurant_id": 1, "customer_id": 4},
    {"id": 8, "restaurant_id": 7, "customer_id": 6},
    {"id": 9, "restaurant_id": 4, "customer_id": 10},
    {"id": 10, "restaurant_id": 10, "customer_id": 5}
]
for entry in data:
    restaurant = session.query(Restaurant).filter_by(id=entry["restaurant_id"]).first()
    customer = session.query(Customer).filter_by(id=entry["customer_id"]).first()
    if restaurant is not None and customer is not None:
        restaurant.customers.append(customer)
session.commit()
