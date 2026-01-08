"""SQL Queries for Credit Card Spend Analysis

This module contains SQL queries that would be used in a production database.
For demonstration purposes, we'll also have pandas equivalents.
"""

SQL_QUERIES = {
    "spend_by_category": """
    -- Total Spend by Category
    SELECT 
        category,
        COUNT(*) as transaction_count,
        ROUND(SUM(amount), 2) as total_spend,
        ROUND(AVG(amount), 2) as avg_transaction_size,
        ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM transactions), 2) as spend_percentage
    FROM transactions
    GROUP BY category
    ORDER BY total_spend DESC;
    """,
    
    "spend_by_region": """
    -- Total Spend by Geographic Region
    SELECT 
        region,
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(*) as transaction_count,
        ROUND(SUM(amount), 2) as total_spend,
        ROUND(AVG(amount), 2) as avg_transaction
    FROM transactions
    GROUP BY region
    ORDER BY total_spend DESC;
    """,
    
    "monthly_spend_trend": """
    -- Monthly Spend Trend with Year-over-Year Comparison
    SELECT 
        DATE_TRUNC('month', transaction_date) as month,
        category,
        COUNT(*) as transaction_count,
        ROUND(SUM(amount), 2) as total_spend,
        ROUND(AVG(amount), 2) as avg_transaction
    FROM transactions
    GROUP BY DATE_TRUNC('month', transaction_date), category
    ORDER BY month, category;
    """,
    
    "campaign_effectiveness": """
    -- Campaign Effectiveness Analysis (Pre vs During vs Post)
    WITH campaign_periods AS (
        SELECT 
            transaction_date,
            customer_id,
            category,
            amount,
            CASE 
                WHEN transaction_date < '2024-07-01' THEN 'Pre-Campaign'
                WHEN transaction_date BETWEEN '2024-07-01' AND '2024-09-30' THEN 'During-Campaign'
                ELSE 'Post-Campaign'
            END as campaign_period
        FROM transactions
    )
    SELECT 
        campaign_period,
        category,
        COUNT(*) as transaction_count,
        ROUND(SUM(amount), 2) as total_spend,
        ROUND(AVG(amount), 2) as avg_transaction_size,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM campaign_periods
    WHERE category IN ('Travel', 'Dining')
    GROUP BY campaign_period, category
    ORDER BY category, campaign_period;
    """,
    
    "customer_segmentation": """
    -- Customer Segmentation by Spend Behavior
    WITH customer_metrics AS (
        SELECT 
            customer_id,
            customer_segment,
            COUNT(*) as transaction_count,
            ROUND(SUM(amount), 2) as total_spend,
            ROUND(AVG(amount), 2) as avg_transaction,
            COUNT(DISTINCT category) as categories_used
        FROM transactions
        GROUP BY customer_id, customer_segment
    )
    SELECT 
        customer_segment,
        COUNT(*) as customer_count,
        ROUND(AVG(total_spend), 2) as avg_customer_spend,
        ROUND(AVG(transaction_count), 2) as avg_transactions_per_customer,
        ROUND(AVG(avg_transaction), 2) as avg_transaction_size
    FROM customer_metrics
    GROUP BY customer_segment
    ORDER BY avg_customer_spend DESC;
    """,
    
    "top_customers_by_spend": """
    -- Top 20 Customers by Total Spend
    SELECT 
        t.customer_id,
        c.name,
        c.customer_segment,
        c.region,
        COUNT(*) as transaction_count,
        ROUND(SUM(t.amount), 2) as total_spend,
        ROUND(AVG(t.amount), 2) as avg_transaction
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    GROUP BY t.customer_id, c.name, c.customer_segment, c.region
    ORDER BY total_spend DESC
    LIMIT 20;
    """,
    
    "campaign_response_rate": """
    -- Campaign Response Rate Analysis
    WITH campaign_customers AS (
        SELECT 
            customer_id,
            SUM(CASE WHEN transaction_date BETWEEN '2024-07-01' AND '2024-09-30' 
                     AND category IN ('Travel', 'Dining') 
                     THEN amount ELSE 0 END) as campaign_spend,
            SUM(CASE WHEN transaction_date < '2024-07-01' 
                     AND category IN ('Travel', 'Dining') 
                     THEN amount ELSE 0 END) / 6.0 as avg_monthly_pre_campaign
        FROM transactions
        GROUP BY customer_id
    )
    SELECT 
        COUNT(*) as total_customers,
        SUM(CASE WHEN campaign_spend > avg_monthly_pre_campaign * 3 * 1.2 THEN 1 ELSE 0 END) as responded_customers,
        ROUND(100.0 * SUM(CASE WHEN campaign_spend > avg_monthly_pre_campaign * 3 * 1.2 THEN 1 ELSE 0 END) / COUNT(*), 2) as response_rate_percentage
    FROM campaign_customers
    WHERE avg_monthly_pre_campaign > 0;
    """,
    
    "incremental_revenue": """
    -- Calculate Incremental Revenue from Campaign
    WITH spend_comparison AS (
        SELECT 
            SUM(CASE WHEN transaction_date BETWEEN '2024-07-01' AND '2024-09-30' 
                     AND category IN ('Travel', 'Dining') 
                     THEN amount ELSE 0 END) as campaign_period_spend,
            SUM(CASE WHEN transaction_date BETWEEN '2024-01-01' AND '2024-06-30' 
                     AND category IN ('Travel', 'Dining') 
                     THEN amount ELSE 0 END) / 6.0 * 3 as expected_spend
        FROM transactions
    )
    SELECT 
        ROUND(campaign_period_spend, 2) as actual_campaign_spend,
        ROUND(expected_spend, 2) as expected_baseline_spend,
        ROUND(campaign_period_spend - expected_spend, 2) as incremental_revenue,
        ROUND(((campaign_period_spend - expected_spend) / expected_spend) * 100, 2) as revenue_lift_percentage
    FROM spend_comparison;
    """,
    
    "category_trends_window": """
    -- Category Spend Trends Using Window Functions
    SELECT 
        DATE_TRUNC('month', transaction_date) as month,
        category,
        ROUND(SUM(amount), 2) as monthly_spend,
        ROUND(AVG(SUM(amount)) OVER (
            PARTITION BY category 
            ORDER BY DATE_TRUNC('month', transaction_date) 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2) as three_month_moving_avg,
        ROUND(
            (SUM(amount) - LAG(SUM(amount)) OVER (PARTITION BY category ORDER BY DATE_TRUNC('month', transaction_date))) 
            / LAG(SUM(amount)) OVER (PARTITION BY category ORDER BY DATE_TRUNC('month', transaction_date)) * 100,
        2) as month_over_month_growth
    FROM transactions
    GROUP BY DATE_TRUNC('month', transaction_date), category
    ORDER BY category, month;
    """
}

def get_query(query_name):
    """Get SQL query by name"""
    return SQL_QUERIES.get(query_name, "Query not found")

def get_all_queries():
    """Get all SQL queries"""
    return SQL_QUERIES
