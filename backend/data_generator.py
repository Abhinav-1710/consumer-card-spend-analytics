import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
import json

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

class CreditCardDataGenerator:
    def __init__(self):
        self.categories = {
            'Travel': {'base_amount': 300, 'std': 200, 'weight': 0.15},
            'Dining': {'base_amount': 75, 'std': 40, 'weight': 0.20},
            'Retail': {'base_amount': 120, 'std': 80, 'weight': 0.25},
            'Groceries': {'base_amount': 150, 'std': 60, 'weight': 0.20},
            'Entertainment': {'base_amount': 60, 'std': 30, 'weight': 0.10},
            'Gas': {'base_amount': 50, 'std': 20, 'weight': 0.08},
            'Other': {'base_amount': 80, 'std': 50, 'weight': 0.02}
        }
        
        self.regions = ['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest']
        
        # Campaign details: Premium Dining & Travel Rewards (July-Sept 2024)
        self.campaign_start = datetime(2024, 7, 1)
        self.campaign_end = datetime(2024, 9, 30)
        
    def generate_customers(self, n_customers=5000):
        """Generate customer profiles"""
        customers = []
        for i in range(n_customers):
            customer = {
                'customer_id': f'CUST{str(i+1).zfill(6)}',
                'name': fake.name(),
                'email': fake.email(),
                'region': random.choice(self.regions),
                'member_since': fake.date_between(start_date='-5y', end_date='-1y'),
                'credit_limit': random.choice([5000, 10000, 15000, 25000, 50000]),
                'customer_segment': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'])
            }
            customers.append(customer)
        return pd.DataFrame(customers)
    
    def generate_transactions(self, customers_df, start_date, end_date):
        """Generate realistic credit card transactions"""
        transactions = []
        transaction_id = 1
        
        for _, customer in customers_df.iterrows():
            current_date = start_date
            
            # Number of transactions per customer (4-15 per month)
            n_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
            transactions_per_month = random.randint(4, 15)
            
            while current_date <= end_date:
                # Generate random number of transactions this month
                n_transactions = random.randint(transactions_per_month - 2, transactions_per_month + 3)
                
                for _ in range(n_transactions):
                    # Random day in the month
                    if current_date.month == 12:
                        next_month = datetime(current_date.year + 1, 1, 1)
                    else:
                        next_month = datetime(current_date.year, current_date.month + 1, 1)
                    
                    days_in_month = (next_month - current_date).days
                    transaction_date = current_date + timedelta(days=random.randint(0, days_in_month - 1))
                    
                    if transaction_date > end_date:
                        break
                    
                    # Select category based on weights
                    category = random.choices(
                        list(self.categories.keys()),
                        weights=[cat['weight'] for cat in self.categories.values()]
                    )[0]
                    
                    # Base amount for category
                    base_amount = self.categories[category]['base_amount']
                    std_amount = self.categories[category]['std']
                    
                    # Campaign boost for Travel and Dining during campaign period
                    campaign_boost = 1.0
                    in_campaign = False
                    
                    if self.campaign_start <= transaction_date <= self.campaign_end:
                        in_campaign = True
                        # Only certain customers respond to campaign (40% response rate)
                        if random.random() < 0.40:
                            if category in ['Travel', 'Dining']:
                                campaign_boost = random.uniform(1.25, 1.60)  # 25-60% increase
                    
                    # Generate amount with some randomness
                    amount = abs(np.random.normal(base_amount * campaign_boost, std_amount))
                    amount = round(max(5, amount), 2)  # Minimum $5 transaction
                    
                    transaction = {
                        'transaction_id': f'TXN{str(transaction_id).zfill(8)}',
                        'customer_id': customer['customer_id'],
                        'transaction_date': transaction_date.strftime('%Y-%m-%d'),
                        'category': category,
                        'amount': amount,
                        'merchant_name': self._get_merchant_name(category),
                        'region': customer['region'],
                        'customer_segment': customer['customer_segment'],
                        'in_campaign_period': in_campaign
                    }
                    
                    transactions.append(transaction)
                    transaction_id += 1
                
                # Move to next month
                if current_date.month == 12:
                    current_date = datetime(current_date.year + 1, 1, 1)
                else:
                    current_date = datetime(current_date.year, current_date.month + 1, 1)
        
        return pd.DataFrame(transactions)
    
    def _get_merchant_name(self, category):
        """Generate realistic merchant names"""
        merchants = {
            'Travel': ['Delta Airlines', 'Marriott Hotels', 'Hilton', 'United Airlines', 'Airbnb', 'Expedia'],
            'Dining': ['The Gourmet Kitchen', 'Starbucks', 'Olive Garden', 'Cheesecake Factory', 'Local Bistro'],
            'Retail': ['Amazon', 'Target', 'Walmart', 'Best Buy', 'Macy\'s', 'Apple Store'],
            'Groceries': ['Whole Foods', 'Trader Joe\'s', 'Safeway', 'Kroger', 'Costco'],
            'Entertainment': ['AMC Theaters', 'Netflix', 'Spotify', 'Live Nation', 'Disney+'],
            'Gas': ['Shell', 'Chevron', 'BP', 'Exxon', 'Mobil'],
            'Other': ['CVS Pharmacy', 'Walgreens', 'Home Depot', 'Lowe\'s']
        }
        return random.choice(merchants.get(category, ['Generic Merchant']))
    
    def generate_dataset(self):
        """Generate complete dataset"""
        print("Generating customers...")
        customers = self.generate_customers(5000)
        
        print("Generating transactions...")
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        transactions = self.generate_transactions(customers, start_date, end_date)
        
        print(f"Generated {len(customers)} customers and {len(transactions)} transactions")
        
        return customers, transactions

if __name__ == "__main__":
    generator = CreditCardDataGenerator()
    customers, transactions = generator.generate_dataset()
    
    # Save to CSV
    customers.to_csv('/app/backend/data/customers.csv', index=False)
    transactions.to_csv('/app/backend/data/transactions.csv', index=False)
    
    print("\nDataset saved to /app/backend/data/")
    print(f"Customers: {len(customers)}")
    print(f"Transactions: {len(transactions)}")
    print(f"\nSample transactions:\n{transactions.head()}")
