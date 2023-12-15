# models.py
from sqlalchemy import create_engine, Column, Integer, String, Table, Float, ForeignKey, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from termcolor import colored

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Float())

    review = relationship('Review', backref='restaurant')
    customers = relationship('Customer', secondary='restaurants_customers', back_populates='restaurants')

    def all_restaurants_reviews(self):
        return self.review

    def all_restaurant_customers(self):
        return self.customers

    def full_restaurant_reviews(self):
        return f"Review for {self} by {self.customers}: {self.review} stars."

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def __repr__(self):
        return f'<Restaurant {self.name}>'

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    review = relationship('Review', backref='customer')
    restaurants = relationship('Restaurant', secondary='restaurants_customers', back_populates='customers')

    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def all_customer_reviews(self):
        return self.review

    def all_customers_restaurants(self):
        return self.restaurants

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        try:
            max_review = max(self.review, key=lambda review: review.rating)
            return max_review.restaurant
        except (ValueError, TypeError):
            return None

    def add_review(self, restaurant, rating):
        new_review = Review(rating=rating, customer=self, restaurant=restaurant)
        try:
            session.add(new_review)
            session.commit()
            self.review.append(new_review)
            restaurant.review.append(new_review)
            session.commit()
            print(f"New review for {restaurant.name} added successfully!")
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error adding review: {e}")

    def delete_reviews(self, restaurant):
        try:
            session.query(Review).filter_by(restaurant_id=restaurant.id).delete()
            session.commit()
            print(f'Reviews for {restaurant.name} deleted successfully')
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting reviews: {e}")

    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer(), primary_key=True)
    rating = Column(Float())
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))

    def __init__(self, rating, customer_id, restaurant_id, id=None):
        self.id = id
        self.rating = rating
        self.customer = session.query(Customer).get(customer_id)
        self.restaurant = session.query(Restaurant).get(restaurant_id)

    def customer_review(self):
        return self.customer

    def restaurant_review(self):
        return self.restaurant

    def full_review(self):
        return f"Review for {self.restaurant} by {self.customer} {self.id}: {self.rating} stars."

    def __repr__(self):
        return f'<Review {self.rating}>'

restaurants_customers = Table(
    'restaurants_customers',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    extend_existing=True,
)

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

retrieved_review = session.query(Review).filter_by(id=1).first()
if retrieved_review is not None:
    review_customer = retrieved_review.customer_review()
    print(f"Customer who left review 1: {colored(str(review_customer), 'green')}")
else:
    print(colored("No review with ID 1 found.", 'red'))

retrieved_review1 = session.query(Review).filter_by(id=1).first()
if retrieved_review1 is not None:
    review_restaurant = retrieved_review1.restaurant_review()
    print(f"Restaurant that was rated in review 1: {colored(str(review_restaurant), 'cyan')}")
else:
    print(colored("No review with ID 1 found.", 'red'))
