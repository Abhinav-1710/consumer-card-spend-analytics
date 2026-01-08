import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import json

class CreditCardAnalytics:
    def __init__(self, transactions_df, customers_df):
        self.transactions = transactions_df.copy()
        self.customers = customers_df.copy()
        
        # Convert date columns
        self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        
        # Add month and year columns
        self.transactions['month'] = self.transactions['transaction_date'].dt.to_period('M')
        self.transactions['year_month'] = self.transactions['transaction_date'].dt.strftime('%Y-%m')
        
        # Campaign dates
        self.campaign_start = datetime(2024, 7, 1)
        self.campaign_end = datetime(2024, 9, 30)
        self.pre_campaign_start = datetime(2024, 1, 1)
        self.pre_campaign_end = datetime(2024, 6, 30)
        self.post_campaign_start = datetime(2024, 10, 1)
        self.post_campaign_end = datetime(2024, 12, 31)
    
    def get_overview_metrics(self):
        """Calculate key overview metrics"""
        total_transactions = len(self.transactions)
        total_spend = self.transactions['amount'].sum()
        avg_transaction = self.transactions['amount'].mean()
        unique_customers = self.transactions['customer_id'].nunique()
        
        # Campaign metrics
        campaign_transactions = self.transactions[
            (self.transactions['transaction_date'] >= self.campaign_start) &
            (self.transactions['transaction_date'] <= self.campaign_end) &
            (self.transactions['category'].isin(['Travel', 'Dining']))
        ]
        
        campaign_revenue = campaign_transactions['amount'].sum()
        
        # Calculate incremental revenue
        pre_campaign = self.transactions[
            (self.transactions['transaction_date'] >= self.pre_campaign_start) &
            (self.transactions['transaction_date'] <= self.pre_campaign_end) &
            (self.transactions['category'].isin(['Travel', 'Dining']))
        ]['amount'].sum()
        
        expected_baseline = (pre_campaign / 6) * 3  # 6 months pre, 3 months campaign
        incremental_revenue = campaign_revenue - expected_baseline
        roi_percentage = (incremental_revenue / expected_baseline) * 100 if expected_baseline > 0 else 0
        
        return {
            'total_transactions': int(total_transactions),
            'total_spend': round(float(total_spend), 2),
            'avg_transaction_size': round(float(avg_transaction), 2),
            'unique_customers': int(unique_customers),
            'campaign_revenue': round(float(campaign_revenue), 2),
            'incremental_revenue': round(float(incremental_revenue), 2),
            'roi_percentage': round(float(roi_percentage), 2)
        }
    
    def get_spend_by_category(self):
        """Analyze spend by category"""
        category_analysis = self.transactions.groupby('category').agg({
            'transaction_id': 'count',
            'amount': ['sum', 'mean']
        }).reset_index()
        
        category_analysis.columns = ['category', 'transaction_count', 'total_spend', 'avg_transaction']
        
        # Add percentage
        total_spend = category_analysis['total_spend'].sum()
        category_analysis['spend_percentage'] = (category_analysis['total_spend'] / total_spend * 100).round(2)
        
        # Sort by total spend
        category_analysis = category_analysis.sort_values('total_spend', ascending=False)
        
        return category_analysis.to_dict('records')
    
    def get_spend_by_region(self):
        """Analyze spend by geographic region"""
        region_analysis = self.transactions.groupby('region').agg({
            'customer_id': 'nunique',
            'transaction_id': 'count',
            'amount': ['sum', 'mean']
        }).reset_index()
        
        region_analysis.columns = ['region', 'unique_customers', 'transaction_count', 'total_spend', 'avg_transaction']
        region_analysis = region_analysis.sort_values('total_spend', ascending=False)
        
        return region_analysis.to_dict('records')
    
    def get_monthly_trends(self):
        """Analyze monthly spend trends"""
        monthly = self.transactions.groupby(['year_month', 'category']).agg({
            'transaction_id': 'count',
            'amount': 'sum'
        }).reset_index()
        
        monthly.columns = ['month', 'category', 'transaction_count', 'total_spend']
        
        return monthly.to_dict('records')
    
    def get_campaign_effectiveness(self):
        """Analyze campaign effectiveness (Pre vs During vs Post)"""
        # Filter for campaign-relevant categories
        relevant_transactions = self.transactions[
            self.transactions['category'].isin(['Travel', 'Dining'])
        ].copy()
        
        # Assign campaign period
        def assign_period(date):
            if date < self.campaign_start:
                return 'Pre-Campaign'
            elif date <= self.campaign_end:
                return 'During-Campaign'
            else:
                return 'Post-Campaign'
        
        relevant_transactions['campaign_period'] = relevant_transactions['transaction_date'].apply(assign_period)
        
        # Analyze by period and category
        campaign_analysis = relevant_transactions.groupby(['campaign_period', 'category']).agg({
            'transaction_id': 'count',
            'amount': ['sum', 'mean'],
            'customer_id': 'nunique'
        }).reset_index()
        
        campaign_analysis.columns = [
            'campaign_period', 'category', 'transaction_count', 
            'total_spend', 'avg_transaction', 'unique_customers'
        ]
        
        # Calculate uplift for during-campaign period
        results = []
        for category in ['Travel', 'Dining']:
            cat_data = campaign_analysis[campaign_analysis['category'] == category]
            
            pre = cat_data[cat_data['campaign_period'] == 'Pre-Campaign']
            during = cat_data[cat_data['campaign_period'] == 'During-Campaign']
            post = cat_data[cat_data['campaign_period'] == 'Post-Campaign']
            
            pre_avg_monthly = pre['total_spend'].values[0] / 6 if len(pre) > 0 else 0
            during_total = during['total_spend'].values[0] if len(during) > 0 else 0
            during_expected = pre_avg_monthly * 3  # 3 months campaign
            
            uplift = ((during_total - during_expected) / during_expected * 100) if during_expected > 0 else 0
            
            for _, row in cat_data.iterrows():
                record = row.to_dict()
                if row['campaign_period'] == 'During-Campaign':
                    record['uplift_percentage'] = round(float(uplift), 2)
                else:
                    record['uplift_percentage'] = 0.0
                results.append(record)
        
        return results
    
    def get_customer_segmentation(self):
        """Analyze customer segments"""
        customer_metrics = self.transactions.groupby(['customer_id', 'customer_segment']).agg({
            'transaction_id': 'count',
            'amount': ['sum', 'mean'],
            'category': 'nunique'
        }).reset_index()
        
        customer_metrics.columns = [
            'customer_id', 'customer_segment', 'transaction_count',
            'total_spend', 'avg_transaction', 'categories_used'
        ]
        
        # Aggregate by segment
        segment_analysis = customer_metrics.groupby('customer_segment').agg({
            'customer_id': 'count',
            'total_spend': 'mean',
            'transaction_count': 'mean',
            'avg_transaction': 'mean'
        }).reset_index()
        
        segment_analysis.columns = [
            'customer_segment', 'customer_count', 'avg_customer_spend',
            'avg_transactions_per_customer', 'avg_transaction_size'
        ]
        
        segment_analysis = segment_analysis.sort_values('avg_customer_spend', ascending=False)
        
        return segment_analysis.to_dict('records')
    
    def get_recommended_segments(self):
        """Recommend customer segments for future campaigns"""
        # Calculate campaign response by segment
        campaign_txns = self.transactions[
            (self.transactions['transaction_date'] >= self.campaign_start) &
            (self.transactions['transaction_date'] <= self.campaign_end) &
            (self.transactions['category'].isin(['Travel', 'Dining']))
        ]
        
        pre_campaign_txns = self.transactions[
            (self.transactions['transaction_date'] >= self.pre_campaign_start) &
            (self.transactions['transaction_date'] <= self.pre_campaign_end) &
            (self.transactions['category'].isin(['Travel', 'Dining']))
        ]
        
        # Calculate uplift by segment
        campaign_by_segment = campaign_txns.groupby('customer_segment')['amount'].sum()
        pre_by_segment = pre_campaign_txns.groupby('customer_segment')['amount'].sum() / 6 * 3
        
        uplift_by_segment = ((campaign_by_segment - pre_by_segment) / pre_by_segment * 100).round(2)
        
        recommendations = []
        for segment in uplift_by_segment.index:
            recommendations.append({
                'segment': segment,
                'uplift_percentage': float(uplift_by_segment[segment]),
                'recommendation': 'High Priority' if uplift_by_segment[segment] > 20 else 
                                 'Medium Priority' if uplift_by_segment[segment] > 10 else 'Low Priority'
            })
        
        return sorted(recommendations, key=lambda x: x['uplift_percentage'], reverse=True)
    
    def get_statistical_summary(self):
        """Generate statistical summary"""
        # Overall statistics
        stats = {
            'mean_transaction': float(self.transactions['amount'].mean()),
            'median_transaction': float(self.transactions['amount'].median()),
            'std_transaction': float(self.transactions['amount'].std()),
            'min_transaction': float(self.transactions['amount'].min()),
            'max_transaction': float(self.transactions['amount'].max()),
        }
        
        # Campaign period statistics
        campaign_txns = self.transactions[
            (self.transactions['transaction_date'] >= self.campaign_start) &
            (self.transactions['transaction_date'] <= self.campaign_end) &
            (self.transactions['category'].isin(['Travel', 'Dining']))
        ]
        
        pre_campaign_txns = self.transactions[
            (self.transactions['transaction_date'] >= self.pre_campaign_start) &
            (self.transactions['transaction_date'] <= self.pre_campaign_end) &
            (self.transactions['category'].isin(['Travel', 'Dining']))
        ]
        
        stats['campaign_mean'] = float(campaign_txns['amount'].mean()) if len(campaign_txns) > 0 else 0
        stats['pre_campaign_mean'] = float(pre_campaign_txns['amount'].mean()) if len(pre_campaign_txns) > 0 else 0
        stats['mean_uplift'] = float((stats['campaign_mean'] - stats['pre_campaign_mean']) / stats['pre_campaign_mean'] * 100) if stats['pre_campaign_mean'] > 0 else 0
        
        return stats
