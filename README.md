# Consumer Card Spend & Campaign Effectiveness Analytics

## 🎯 Project Overview

**Project Title:** Consumer Credit Card Spend Analysis & Marketing Campaign Optimization

**Purpose:** Data-driven analysis of credit card spending patterns and marketing campaign effectiveness to support strategic business decisions.

**Target Role:** Data Analyst at American Express

---

## 📈 Dataset Description

### Synthetic Data Generation
- **Customers:** 5,000 unique cardholders
- **Transactions:** 600,000+ credit card transactions
- **Time Period:** January 2024 - December 2024 (12 months)
- **Categories:** Travel, Dining, Retail, Groceries, Entertainment, Gas, Other
- **Geographic Regions:** Northeast, Southeast, Midwest, West, Southwest
- **Customer Segments:** Bronze, Silver, Gold, Platinum

### Campaign Details
**Campaign Name:** Premium Dining & Travel Rewards Boost

**Campaign Period:** July 1, 2024 - September 30, 2024 (Q3 2024)

**Campaign Mechanics:**
- Enhanced rewards on Travel and Dining purchases
- 40% customer response rate
- 25-60% spend increase among responding customers

**Baseline Comparison:**
- Pre-Campaign: January - June 2024 (6 months)
- During Campaign: July - September 2024 (3 months)
- Post-Campaign: October - December 2024 (3 months)

---

## 🔧 Technical Stack

### Backend
- **Framework:** FastAPI (Python)
- **Data Processing:** Pandas, NumPy
- **Statistical Analysis:** Scikit-learn, SciPy
- **Data Generation:** Faker library

### Frontend
- **Framework:** React 19
- **UI Components:** Radix UI, Tailwind CSS
- **Data Visualization:** Recharts
- **State Management:** React Hooks

### Database
- **Primary:** CSV files (for portability)
- **Optional:** MongoDB (for extended features)

### Tools Demonstrated
- SQL query design (PostgreSQL/MySQL compatible)
- Python data analysis
- Statistical methodologies
- Interactive dashboards
- Business intelligence reporting

---

## 📊 Key Analyses Performed

### 1. Spend Pattern Analysis
- **By Category:** Identified spending distribution across 7 major categories
- **By Geography:** Regional spend patterns and customer concentration
- **By Time:** Monthly trends, seasonality, and growth patterns
- **By Segment:** Customer tier behavior and lifetime value

### 2. Campaign Effectiveness Metrics
- **ROI Calculation:** Incremental revenue vs baseline
- **Uplift Analysis:** Pre vs During vs Post campaign comparison
- **Response Rate:** Percentage of customers who increased spending
- **Category Impact:** Travel and Dining spend lift during campaign

### 3. Statistical Analysis
- **Descriptive Statistics:** Mean, median, standard deviation
- **Trend Analysis:** Month-over-month growth rates
- **Variance Analysis:** Spending volatility by segment
- **Correlation:** Category cross-purchase behavior

### 4. Customer Segmentation
- **Spend-Based Segmentation:** Average customer value by tier
- **Behavior Clustering:** High-value vs low-engagement customers
- **Campaign Response:** Segment-level uplift percentages
- **Lifetime Value:** Transaction frequency and average ticket size

---

## 📝 SQL Queries

All SQL queries are available in `/app/backend/sql_queries.py` and include:

1. **Spend by Category** - Aggregation with percentage calculations
2. **Spend by Region** - Geographic analysis with customer counts
3. **Monthly Spend Trend** - Time-series analysis with date functions
4. **Campaign Effectiveness** - Pre/During/Post comparison with CTEs
5. **Customer Segmentation** - Multi-level aggregation
6. **Top Customers** - Ranking and joins
7. **Campaign Response Rate** - Complex conditional logic
8. **Incremental Revenue** - Financial calculation with baseline
9. **Category Trends with Window Functions** - Moving averages and growth rates

---

## 🎯 Key Findings

### Campaign Performance
- **Total Campaign Revenue:** $10.81M in Travel & Dining
- **Incremental Revenue:** $1.48M above baseline
- **ROI:** 15.86% revenue lift
- **Customer Engagement:** 40% response rate

### Spend Distribution
- **Top Category:** Retail (25% of total spend)
- **Campaign Categories:** Travel (15%) + Dining (20%) = 35% combined
- **Steady Categories:** Groceries (20%), Entertainment (10%)

### Customer Insights
- **Platinum Segment:** Highest average spend per customer
- **Gold Segment:** Best campaign response rate
- **Regional Leaders:** West and Northeast regions

### Statistical Insights
- **Mean Transaction:** $137.40
- **Campaign Uplift:** 28-45% increase in target categories
- **Consistency:** Low variance in monthly spending patterns

---

## 📄 Project Outputs

### 1. Interactive Dashboard
- Live web application with real-time data visualization
- Multiple views: Overview, Campaign Analysis, Segmentation, SQL
- Exportable charts and insights

### 2. SQL Query Library
- Production-ready SQL queries
- Documented with comments and use cases
- Compatible with PostgreSQL/MySQL

### 3. Python Analysis Scripts
- `data_generator.py` - Synthetic dataset creation
- `analytics_engine.py` - Statistical analysis functions
- `sql_queries.py` - SQL query templates

### 4. API Endpoints
- RESTful API with 10+ endpoints
- JSON responses for easy integration
- Downloadable CSV data

### 5. Documentation
- This README file
- Inline code comments
- API documentation

---

## 🚀 Running the Project

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (optional)

### Backend Setup
```bash
cd /app/backend
pip install -r requirements.txt
python data_generator.py  # Generate dataset
python server.py          # Start API server
```

### Frontend Setup
```bash
cd /app/frontend
yarn install
yarn start  # Start React app
```

### Access the Application
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8001/docs
- **Backend API:** http://localhost:8001/api

---

## 💼 Skills Demonstrated

### Technical Skills
✓ **SQL Proficiency**
  - Complex queries with CTEs, window functions, joins
  - Aggregations and group-by operations
  - Date/time manipulations

✓ **Python Data Analysis**
  - Pandas for data manipulation
  - NumPy for numerical operations
  - Statistical analysis and calculations

✓ **Data Visualization**
  - Interactive charts (bar, line, pie)
  - Dashboard design
  - Insight presentation

✓ **Business Analysis**
  - KPI identification and tracking
  - Campaign ROI measurement
  - Customer segmentation
  - Actionable recommendations

✓ **API Development**
  - RESTful API design
  - Data serialization
  - Error handling

✓ **Statistical Methods**
  - Descriptive statistics
  - Trend analysis
  - Uplift measurement
  - A/B testing concepts

---

## 💡 Business Recommendations

### Immediate Actions
1. **Scale Campaign to High-Performing Segments**
   - Focus on Gold and Platinum customers (highest uplift)
   - Allocate 60% of marketing budget to these tiers

2. **Extend Campaign Duration**
   - Continue Travel & Dining rewards for Q4
   - Monitor for diminishing returns

3. **Geographic Expansion**
   - Prioritize West and Northeast regions
   - Customize offers for regional preferences

### Strategic Initiatives
1. **Cross-Category Bundling**
   - Combine Travel + Dining + Entertainment
   - Test "Experience Package" rewards

2. **Personalized Offers**
   - Use transaction history for tailored campaigns
   - Implement predictive modeling for offer acceptance

3. **Retention Programs**
   - Target low-engagement Bronze/Silver customers
   - Create graduation incentives to higher tiers

### Measurement & Iteration
1. **Monthly Performance Reviews**
   - Track ROI against 15% benchmark
   - Adjust campaign parameters based on data

2. **A/B Testing Framework**
   - Test offer variations by segment
   - Measure statistical significance

3. **Predictive Analytics**
   - Build churn prediction models
   - Forecast campaign impact before launch

---

## 📚 Learning Outcomes

Through this project, I have demonstrated:

1. **End-to-End Data Analysis**
   - From data generation to insight delivery
   - Complete analytical workflow

2. **Business-Focused Approach**
   - Aligned analysis with strategic goals
   - Actionable recommendations, not just numbers

3. **Technical Versatility**
   - Backend and frontend development
   - SQL, Python, visualization tools

4. **Communication Skills**
   - Clear documentation
   - Visual storytelling
   - Executive-level summaries

---

## 📞 Contact & Portfolio

**Project Purpose:** American Express Data Analyst Application

**Key Differentiators:**
- Production-ready code quality
- Real-world campaign scenario
- Full-stack implementation
- Business-focused insights

**Next Steps:**
This project demonstrates my ability to:
- Transform raw data into business intelligence
- Design and implement analytical solutions
- Communicate findings to stakeholders
- Drive data-driven decision making

---

## 🔑 Key Metrics Summary

| Metric | Value |
|--------|-------|
| Total Transactions | 600,981 |
| Total Spend | $82.57M |
| Unique Customers | 5,000 |
| Campaign Revenue | $10.81M |
| Incremental Revenue | $1.48M |
| ROI | +15.86% |
| Avg Transaction | $137.40 |
| Campaign Duration | 3 months |
| Response Rate | 40% |
| Top Performing Segment | Gold |

---

**Built with ❤️ for American Express Data Analyst Role**

*Demonstrates: SQL · Python · Statistical Analysis · Data Visualization · Business Intelligence*