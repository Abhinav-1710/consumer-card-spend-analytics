import React, { useState, useEffect } from 'react';
import '@/App.css';
import axios from 'axios';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download, TrendingUp, Users, DollarSign, Target } from 'lucide-react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d', '#ffc658'];

function App() {
  const [overview, setOverview] = useState(null);
  const [categoryData, setCategoryData] = useState([]);
  const [regionData, setRegionData] = useState([]);
  const [monthlyTrends, setMonthlyTrends] = useState([]);
  const [campaignData, setCampaignData] = useState([]);
  const [segmentData, setSegmentData] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [sqlQueries, setSqlQueries] = useState({});
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const [overviewRes, categoryRes, regionRes, trendsRes, campaignRes, segmentRes, recsRes, sqlRes, statsRes] = await Promise.all([
        axios.get(`${API}/analytics/overview`),
        axios.get(`${API}/analytics/spend-by-category`),
        axios.get(`${API}/analytics/spend-by-region`),
        axios.get(`${API}/analytics/monthly-trends`),
        axios.get(`${API}/analytics/campaign-effectiveness`),
        axios.get(`${API}/analytics/customer-segmentation`),
        axios.get(`${API}/analytics/recommendations`),
        axios.get(`${API}/analytics/sql-queries`),
        axios.get(`${API}/analytics/statistical-summary`)
      ]);

      setOverview(overviewRes.data);
      setCategoryData(categoryRes.data.data);
      setRegionData(regionRes.data.data);
      setMonthlyTrends(trendsRes.data.data);
      setCampaignData(campaignRes.data.data);
      setSegmentData(segmentRes.data.data);
      setRecommendations(recsRes.data.data);
      setSqlQueries(sqlRes.data.queries);
      setStats(statsRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const downloadData = () => {
    window.open(`${API}/analytics/download-data`, '_blank');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading analytics data...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-black bg-opacity-40 backdrop-blur-sm border-b border-purple-500/30">
        <div className="container mx-auto px-6 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2" data-testid="app-title">
                Consumer Card Spend Analytics
              </h1>
              <p className="text-purple-200">Premium Dining & Travel Rewards Campaign Analysis</p>
            </div>
            <Button onClick={downloadData} className="bg-purple-600 hover:bg-purple-700" data-testid="download-button">
              <Download className="mr-2 h-4 w-4" />
              Download Data
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Overview KPIs */}
        {overview && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="kpi-transactions">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-purple-100">Total Transactions</CardTitle>
                <TrendingUp className="h-4 w-4 text-purple-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{overview.total_transactions.toLocaleString()}</div>
              </CardContent>
            </Card>

            <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="kpi-spend">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-purple-100">Total Spend</CardTitle>
                <DollarSign className="h-4 w-4 text-green-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">${overview.total_spend.toLocaleString()}</div>
              </CardContent>
            </Card>

            <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="kpi-customers">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-purple-100">Unique Customers</CardTitle>
                <Users className="h-4 w-4 text-blue-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{overview.unique_customers.toLocaleString()}</div>
              </CardContent>
            </Card>

            <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="kpi-roi">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-purple-100">Campaign ROI</CardTitle>
                <Target className="h-4 w-4 text-yellow-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">+{overview.roi_percentage.toFixed(1)}%</div>
                <p className="text-xs text-purple-200 mt-1">
                  ${overview.incremental_revenue.toLocaleString()} incremental revenue
                </p>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Tabbed Content */}
        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="bg-black bg-opacity-40 backdrop-blur-sm border border-purple-500/30 mb-6">
            <TabsTrigger value="overview" className="data-[state=active]:bg-purple-600" data-testid="tab-overview">
              Overview
            </TabsTrigger>
            <TabsTrigger value="campaign" className="data-[state=active]:bg-purple-600" data-testid="tab-campaign">
              Campaign Analysis
            </TabsTrigger>
            <TabsTrigger value="segments" className="data-[state=active]:bg-purple-600" data-testid="tab-segments">
              Customer Segments
            </TabsTrigger>
            <TabsTrigger value="sql" className="data-[state=active]:bg-purple-600" data-testid="tab-sql">
              SQL Queries
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Spend by Category */}
            <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-category-analysis">
              <CardHeader>
                <CardTitle className="text-white">Spend Analysis by Category</CardTitle>
                <CardDescription className="text-purple-200">Total spend distribution across categories</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={categoryData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#4c1d95" />
                    <XAxis dataKey="category" stroke="#e9d5ff" />
                    <YAxis stroke="#e9d5ff" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e1b4b', border: '1px solid #7c3aed' }}
                      labelStyle={{ color: '#e9d5ff' }}
                    />
                    <Legend wrapperStyle={{ color: '#e9d5ff' }} />
                    <Bar dataKey="total_spend" fill="#8b5cf6" name="Total Spend ($)" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Region Analysis */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-region-analysis">
                <CardHeader>
                  <CardTitle className="text-white">Spend by Region</CardTitle>
                  <CardDescription className="text-purple-200">Geographic distribution</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={regionData}
                        dataKey="total_spend"
                        nameKey="region"
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        label
                      >
                        {regionData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#1e1b4b', border: '1px solid #7c3aed' }}
                      />
                      <Legend wrapperStyle={{ color: '#e9d5ff' }} />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Category Percentage */}
              <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-category-breakdown">
                <CardHeader>
                  <CardTitle className="text-white">Category Breakdown</CardTitle>
                  <CardDescription className="text-purple-200">Percentage of total spend</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {categoryData.slice(0, 5).map((cat, idx) => (
                      <div key={idx}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-purple-100">{cat.category}</span>
                          <span className="text-white font-semibold">{cat.spend_percentage}%</span>
                        </div>
                        <div className="w-full bg-purple-900 rounded-full h-2">
                          <div 
                            className="bg-purple-500 h-2 rounded-full" 
                            style={{ width: `${cat.spend_percentage}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Campaign Analysis Tab */}
          <TabsContent value="campaign" className="space-y-6">
            <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-campaign-effectiveness">
              <CardHeader>
                <CardTitle className="text-white">Campaign Effectiveness: Pre vs During vs Post</CardTitle>
                <CardDescription className="text-purple-200">
                  Premium Dining & Travel Rewards Campaign (July - September 2024)
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={350}>
                  <BarChart data={campaignData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#4c1d95" />
                    <XAxis dataKey="campaign_period" stroke="#e9d5ff" />
                    <YAxis stroke="#e9d5ff" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e1b4b', border: '1px solid #7c3aed' }}
                      labelStyle={{ color: '#e9d5ff' }}
                    />
                    <Legend wrapperStyle={{ color: '#e9d5ff' }} />
                    <Bar dataKey="total_spend" fill="#8b5cf6" name="Total Spend ($)" />
                  </BarChart>
                </ResponsiveContainer>

                {/* Campaign Metrics */}
                <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                  {campaignData.filter(d => d.campaign_period === 'During-Campaign').map((item, idx) => (
                    <div key={idx} className="bg-purple-900 bg-opacity-30 rounded-lg p-4">
                      <h4 className="text-purple-200 text-sm font-medium mb-2">{item.category} Campaign</h4>
                      <div className="flex justify-between items-center">
                        <div>
                          <p className="text-white text-2xl font-bold">
                            +{item.uplift_percentage.toFixed(1)}%
                          </p>
                          <p className="text-purple-300 text-xs">Spend Uplift</p>
                        </div>
                        <div className="text-right">
                          <p className="text-white text-lg">{item.unique_customers}</p>
                          <p className="text-purple-300 text-xs">Customers</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Statistical Summary */}
            {stats && (
              <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-statistical-summary">
                <CardHeader>
                  <CardTitle className="text-white">Statistical Summary</CardTitle>
                  <CardDescription className="text-purple-200">Key statistical metrics</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-purple-300 text-sm">Mean Transaction</p>
                      <p className="text-white text-xl font-semibold">${stats.mean_transaction.toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="text-purple-300 text-sm">Median Transaction</p>
                      <p className="text-white text-xl font-semibold">${stats.median_transaction.toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="text-purple-300 text-sm">Std Deviation</p>
                      <p className="text-white text-xl font-semibold">${stats.std_transaction.toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="text-purple-300 text-sm">Campaign Mean Uplift</p>
                      <p className="text-white text-xl font-semibold">+{stats.mean_uplift.toFixed(1)}%</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Customer Segments Tab */}
          <TabsContent value="segments" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Segment Analysis */}
              <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-segment-analysis">
                <CardHeader>
                  <CardTitle className="text-white">Customer Segment Performance</CardTitle>
                  <CardDescription className="text-purple-200">Average spend by segment tier</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={segmentData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#4c1d95" />
                      <XAxis dataKey="customer_segment" stroke="#e9d5ff" />
                      <YAxis stroke="#e9d5ff" />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#1e1b4b', border: '1px solid #7c3aed' }}
                      />
                      <Legend wrapperStyle={{ color: '#e9d5ff' }} />
                      <Bar dataKey="avg_customer_spend" fill="#10b981" name="Avg Customer Spend ($)" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Recommendations */}
              <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-recommendations">
                <CardHeader>
                  <CardTitle className="text-white">Campaign Recommendations</CardTitle>
                  <CardDescription className="text-purple-200">Segments to target in future campaigns</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recommendations.map((rec, idx) => (
                      <div key={idx} className="bg-purple-900 bg-opacity-30 rounded-lg p-4">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="text-white font-semibold">{rec.segment}</h4>
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                            rec.recommendation === 'High Priority' ? 'bg-green-600 text-white' :
                            rec.recommendation === 'Medium Priority' ? 'bg-yellow-600 text-white' :
                            'bg-gray-600 text-white'
                          }`}>
                            {rec.recommendation}
                          </span>
                        </div>
                        <p className="text-purple-200 text-sm">
                          Campaign Response: <span className="text-white font-semibold">
                            {rec.uplift_percentage > 0 ? '+' : ''}{rec.uplift_percentage.toFixed(1)}%
                          </span>
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Actionable Insights */}
            <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-insights">
              <CardHeader>
                <CardTitle className="text-white">Key Insights & Recommendations</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 text-purple-100">
                  <div className="flex items-start space-x-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <p><strong className="text-white">Strong Campaign Performance:</strong> The Premium Dining & Travel Rewards campaign generated {overview?.roi_percentage.toFixed(1)}% ROI with ${overview?.incremental_revenue.toLocaleString()} incremental revenue.</p>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <p><strong className="text-white">Segment Targeting:</strong> {recommendations[0]?.segment} customers showed the highest response rate and should be prioritized for future campaigns.</p>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <p><strong className="text-white">Category Focus:</strong> Travel and Dining categories demonstrated significant uplift during the campaign period, validating the rewards structure.</p>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span className="text-yellow-400 mt-1">→</span>
                    <p><strong className="text-white">Next Steps:</strong> Consider extending campaign duration and expanding to other premium categories based on customer segment preferences.</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* SQL Queries Tab */}
          <TabsContent value="sql" className="space-y-6">
            <Card className="bg-white bg-opacity-10 backdrop-blur-md border-purple-500/30" data-testid="card-sql-showcase">
              <CardHeader>
                <CardTitle className="text-white">SQL Queries Documentation</CardTitle>
                <CardDescription className="text-purple-200">
                  Production-ready SQL queries for credit card spend analysis
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {Object.entries(sqlQueries).map(([key, query], idx) => (
                    <div key={idx} className="border border-purple-500/30 rounded-lg overflow-hidden">
                      <div className="bg-purple-900 bg-opacity-40 px-4 py-2">
                        <h4 className="text-white font-semibold">{key.replace(/_/g, ' ').toUpperCase()}</h4>
                      </div>
                      <pre className="bg-black bg-opacity-40 p-4 overflow-x-auto text-sm text-purple-100">
                        <code>{query}</code>
                      </pre>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Footer Note */}
        <div className="mt-8 text-center text-purple-200 text-sm">
          <p>💼 Built for American Express Data Analyst Application</p>
          <p className="mt-1">Demonstrates: SQL · Python · Statistical Analysis · Data Visualization · Business Insights</p>
        </div>
      </main>
    </div>
  );
}

export default App;