import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime, timedelta
import random
import uuid

# ✅ First Streamlit command
st.set_page_config(page_title="HealthKart Dashboard", layout="wide")
st.title("📊 HealthKart Influencer Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("📁 Upload influencer CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.success(f"✅ Uploaded: {uploaded_file.name}")
        st.write("### 📋 Preview of Uploaded Data")
        st.dataframe(df.head())

        # Validate required columns
        required_columns = ["Influencer Name", "Engagement Rate (%)", "ROAS"]
        if all(col in df.columns for col in required_columns):

            st.write("### 📊 Engagement Rate")
            st.bar_chart(df.set_index("Influencer Name")["Engagement Rate (%)"])

            st.write("### 💰 ROAS (Return on Ad Spend)")
            st.line_chart(df.set_index("Influencer Name")["ROAS"])
        
        else:
            st.error("❌ Uploaded CSV doesn't contain required columns: " + ", ".join(required_columns))

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")

else:
    st.info("⬆️ Please upload a CSV file to get started.")

# Set page config
#st.set_page_config(
#    page_title="HealthKart Influencer Dashboard",
#    page_icon="💪",
#    layout="wide",
#    initial_sidebar_state="expanded"
#)

# Function to generate synthetic data
def generate_synthetic_data(seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    # Constants
    platforms = ["Instagram", "YouTube", "Twitter", "TikTok"]
    categories = ["Fitness", "Nutrition", "Bodybuilding", "Wellness", "Sports"]
    brands = ["MuscleBlaze", "HKVitals", "Gritzo", "TrueBasics", "bGREEN"]
    products = {
        "MuscleBlaze": ["Biozyme Whey", "Creatine", "Mass Gainer", "Pre-Workout", "BCAA"],
        "HKVitals": ["Multivitamin", "Fish Oil", "Vitamin D3", "Biotin", "Zinc"],
        "Gritzo": ["SuperMilk", "Protein Bars", "Protein Cookies", "Fitness Shakes", "Energy Drinks"],
        "TrueBasics": ["Joint Support", "Hair Vitamins", "Collagen", "Magnesium", "Probiotics"],
        "bGREEN": ["Plant Protein", "Organic Greens", "Vegan BCAA", "Superfood Mix", "Natural Energy"]
    }
    genders = ["Male", "Female", "Non-binary"]
    payment_basis = ["Post", "Order", "Hybrid"]
    
    # Generate influencers data (100 influencers)
    num_influencers = 100
    influencer_ids = [str(uuid.uuid4()) for _ in range(num_influencers)]
    
    influencers = pd.DataFrame({
        'id': influencer_ids,
        'name': [f"Influencer_{i}" for i in range(num_influencers)],
        'category': [random.choice(categories) for _ in range(num_influencers)],
        'gender': [random.choice(genders) for _ in range(num_influencers)],
        'follower_count': [int(np.random.exponential(scale=100000) + 5000) for _ in range(num_influencers)],
        'platform': [random.choice(platforms) for _ in range(num_influencers)],
        'engagement_rate': [round(random.uniform(1.0, 10.0), 2) for _ in range(num_influencers)]
    })
    
    # Generate posts data (400 posts)
    num_posts = 400
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    posts = pd.DataFrame({
        'id': [str(uuid.uuid4()) for _ in range(num_posts)],
        'influencer_id': [random.choice(influencer_ids) for _ in range(num_posts)],
        'platform': [random.choice(platforms) for _ in range(num_posts)],
        'date': [start_date + timedelta(days=random.randint(0, 180)) for _ in range(num_posts)],
        'url': [f"https://example.com/post_{i}" for i in range(num_posts)],
        'caption': [f"Check out this amazing product! #{random.choice(brands).lower()} #healthkart" for _ in range(num_posts)],
        'reach': [int(np.random.exponential(scale=50000) + 1000) for _ in range(num_posts)],
        'likes': [int(np.random.exponential(scale=5000) + 100) for _ in range(num_posts)],
        'comments': [int(np.random.exponential(scale=200) + 10) for _ in range(num_posts)],
        'brand': [random.choice(brands) for _ in range(num_posts)]
    })
    
    # Add product to posts
    for i in range(len(posts)):
        brand = posts.loc[i, 'brand']
        posts.loc[i, 'product'] = random.choice(products[brand])
    
    # Generate tracking data (2000 transactions)
    num_tracking = 2000
    
    # Assign influencers to campaigns with varying performance
    campaigns = []
    campaign_influencers = {}
    
    for brand in brands:
        for i in range(3):  # 3 campaigns per brand
            campaign_name = f"{brand}_Campaign_{i+1}"
            campaigns.append(campaign_name)
            
            # Select 5-10 random influencers for this campaign
            campaign_influencers[campaign_name] = random.sample(influencer_ids, random.randint(5, 10))
    
    tracking_data = pd.DataFrame({
        'id': [str(uuid.uuid4()) for _ in range(num_tracking)],
        'source': [random.choice(['Influencer', 'Organic', 'Paid_Social', 'Direct']) for _ in range(num_tracking)],
        'campaign': [random.choice(campaigns) for _ in range(num_tracking)],
        'influencer_id': [None for _ in range(num_tracking)],
        'user_id': [f"user_{i}" for i in range(num_tracking)],
        'brand': [None for _ in range(num_tracking)],
        'product': [None for _ in range(num_tracking)],
        'date': [start_date + timedelta(days=random.randint(0, 180)) for _ in range(num_tracking)],
        'orders': [random.randint(1, 3) for _ in range(num_tracking)],
        'revenue': [round(random.uniform(500, 5000), 2) for _ in range(num_tracking)]
    })
    
    # Set influencer_id only for 'Influencer' source
    for i in range(len(tracking_data)):
        if tracking_data.loc[i, 'source'] == 'Influencer':
            campaign = tracking_data.loc[i, 'campaign']
            brand = campaign.split('_')[0]
            tracking_data.loc[i, 'brand'] = brand
            tracking_data.loc[i, 'influencer_id'] = random.choice(campaign_influencers.get(campaign, [None]))
            if tracking_data.loc[i, 'influencer_id']:
                tracking_data.loc[i, 'product'] = random.choice(products[brand])
        else:
            brand = random.choice(brands)
            tracking_data.loc[i, 'brand'] = brand
            tracking_data.loc[i, 'product'] = random.choice(products[brand])
    
    # Generate payouts data
    payouts = []
    
    for influencer_id in influencer_ids:
        influencer_posts = posts[posts['influencer_id'] == influencer_id]
        
        # Skip influencers with no posts
        if len(influencer_posts) == 0:
            continue
        
        basis = random.choice(payment_basis)
        
        if basis == "Post":
            rate = round(random.uniform(5000, 20000), 2)
            orders = 0
            total_payout = rate * len(influencer_posts)
        elif basis == "Order":
            rate = round(random.uniform(100, 500), 2)
            influencer_orders = tracking_data[
                (tracking_data['influencer_id'] == influencer_id) & 
                (tracking_data['source'] == 'Influencer')
            ]['orders'].sum()
            orders = influencer_orders
            total_payout = rate * orders if orders > 0 else 0
        else:  # Hybrid
            post_rate = round(random.uniform(2000, 10000), 2)
            order_rate = round(random.uniform(50, 200), 2)
            influencer_orders = tracking_data[
                (tracking_data['influencer_id'] == influencer_id) & 
                (tracking_data['source'] == 'Influencer')
            ]['orders'].sum()
            orders = influencer_orders
            total_payout = (post_rate * len(influencer_posts)) + (order_rate * orders)
        
        payouts.append({
            'id': str(uuid.uuid4()),
            'influencer_id': influencer_id,
            'basis': basis,
            'rate': rate,
            'posts': len(influencer_posts),
            'orders': orders,
            'total_payout': total_payout
        })
    
    payouts_df = pd.DataFrame(payouts)
    
    return influencers, posts, tracking_data, payouts_df
# Function to calculate metrics
def calculate_metrics(influencers, posts, tracking_data, payouts):
    metrics = {}
    
    # Filter only influencer-attributed data
    influencer_data = tracking_data[tracking_data['source'] == 'Influencer']
    
    # Total revenue from influencer campaigns
    influencer_revenue = influencer_data['revenue'].sum()
    metrics['total_influencer_revenue'] = influencer_revenue
    
    # Total spend on influencers
    total_spend = payouts['total_payout'].sum()
    metrics['total_spend'] = total_spend
    
    # Overall ROAS
    metrics['overall_roas'] = influencer_revenue / total_spend if total_spend > 0 else 0
    
    # Total posts
    metrics['total_posts'] = len(posts)
    
    # Total influencers
    metrics['total_influencers'] = len(influencers)
    
    # Average revenue per influencer
    metrics['avg_revenue_per_influencer'] = influencer_revenue / metrics['total_influencers'] if metrics['total_influencers'] > 0 else 0
    
    # Engagement metrics
    total_reach = posts['reach'].sum()
    total_likes = posts['likes'].sum()
    total_comments = posts['comments'].sum()
    
    metrics['total_reach'] = total_reach
    metrics['engagement_rate'] = ((total_likes + total_comments) / total_reach) * 100 if total_reach > 0 else 0
    
    return metrics

# Function to calculate incremental ROAS
def calculate_incremental_roas(tracking_data, payouts):
    # Baseline conversion rate from non-influencer channels
    non_influencer_data = tracking_data[tracking_data['source'] != 'Influencer']
    baseline_revenue = non_influencer_data['revenue'].sum()
    baseline_users = len(non_influencer_data['user_id'].unique())
    baseline_rev_per_user = baseline_revenue / baseline_users if baseline_users > 0 else 0
    
    # Group by influencer to calculate incremental value
    influencer_data = tracking_data[tracking_data['source'] == 'Influencer']
    influencer_results = []
    
    for influencer_id, group in influencer_data.groupby('influencer_id'):
        if influencer_id is None:
            continue
            
        # Calculate actual revenue
        actual_revenue = group['revenue'].sum()
        users_reached = len(group['user_id'].unique())
        
        # Calculate expected revenue based on baseline
        expected_revenue = baseline_rev_per_user * users_reached
        
        # Calculate incremental revenue
        incremental_revenue = actual_revenue - expected_revenue
        
        # Calculate spend on this influencer
        influencer_spend = payouts[payouts['influencer_id'] == influencer_id]['total_payout'].sum()
        
        # Calculate incremental ROAS
        incremental_roas = incremental_revenue / influencer_spend if influencer_spend > 0 else 0
        
        influencer_results.append({
            'influencer_id': influencer_id,
            'actual_revenue': actual_revenue,
            'expected_revenue': expected_revenue,
            'incremental_revenue': incremental_revenue,
            'spend': influencer_spend,
            'incremental_roas': incremental_roas
        })
    
    return pd.DataFrame(influencer_results)

# Function to prepare data for visualization
def prepare_brand_performance(tracking_data, posts, payouts, influencers):
    # Filter for influencer data
    influencer_tracking = tracking_data[tracking_data['source'] == 'Influencer'].copy()
    
    # Group by brand and calculate metrics
    brand_performance = influencer_tracking.groupby('brand').agg({
        'revenue': 'sum',
        'orders': 'sum',
        'influencer_id': 'nunique'
    }).reset_index()
    
    brand_performance.columns = ['brand', 'revenue', 'orders', 'num_influencers']
    
    # Add spend per brand
    brand_spend = []
    for brand in brand_performance['brand']:
        # Get influencers who posted for this brand
        brand_posts = posts[posts['brand'] == brand]
        brand_influencers = brand_posts['influencer_id'].unique()
        
        # Calculate total spend for these influencers
        total_brand_spend = payouts[payouts['influencer_id'].isin(brand_influencers)]['total_payout'].sum()
        brand_spend.append(total_brand_spend)
    
    brand_performance['spend'] = brand_spend
    brand_performance['roas'] = brand_performance['revenue'] / brand_performance['spend']
    brand_performance['roas'] = brand_performance['roas'].replace([np.inf, -np.inf], 0)
    
    return brand_performance

# Function to get top influencers by performance
def get_top_influencers(influencers, incremental_roas_data, n=10):
    if incremental_roas_data.empty:
        return pd.DataFrame()
        
    # Merge influencer data with ROAS data
    influencer_performance = pd.merge(
        influencers,
        incremental_roas_data,
        left_on='id',
        right_on='influencer_id',
        how='inner'
    )
    
    if influencer_performance.empty:
        return pd.DataFrame()
        
    # Sort by incremental ROAS and get top N
    top_influencers = influencer_performance.sort_values('incremental_roas', ascending=False).head(n)
    
    return top_influencers

# Function to get influencer persona insights
def get_persona_insights(influencers, incremental_roas_data):
    if incremental_roas_data.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    # Merge influencer data with ROAS data
    influencer_performance = pd.merge(
        influencers,
        incremental_roas_data,
        left_on='id',
        right_on='influencer_id',
        how='inner'
    )
    
    if influencer_performance.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    # Group by category and calculate average metrics
    category_performance = influencer_performance.groupby('category').agg({
        'incremental_roas': 'mean',
        'actual_revenue': 'mean',
        'incremental_revenue': 'mean',
        'spend': 'mean',
        'influencer_id': 'count'
    }).reset_index()
    
    category_performance.columns = ['category', 'avg_roas', 'avg_revenue', 'avg_incremental_revenue', 'avg_spend', 'count']
    
    # Group by platform and calculate average metrics
    platform_performance = influencer_performance.groupby('platform').agg({
        'incremental_roas': 'mean',
        'actual_revenue': 'mean',
        'incremental_revenue': 'mean',
        'spend': 'mean',
        'influencer_id': 'count'
    }).reset_index()
    
    platform_performance.columns = ['platform', 'avg_roas', 'avg_revenue', 'avg_incremental_revenue', 'avg_spend', 'count']
    
    return category_performance, platform_performance

# Load or generate data
def load_data():
    if "data_loaded" in st.session_state and st.session_state["data_loaded"]:
        return (
            st.session_state["influencers"],
            st.session_state["posts"],
            st.session_state["tracking_data"],
            st.session_state["payouts"]
        )
    else:
        # Fallback to synthetic data if no upload yet
        influencers, posts, tracking_data, payouts = generate_synthetic_data()
        return influencers, posts, tracking_data, payouts

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2d6a9f;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2d6a9f;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f7f7f7;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 0.9rem;
        color: #777;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d6a9f;
    }
    .info-text {
        font-size: 0.9rem;
        color: #555;
    }
    .highlight {
        color: #2d6a9f;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Main app
def main():
    st.markdown('<div class="main-header">HealthKart Influencer Campaign Dashboard</div>', unsafe_allow_html=True)
    
    from PIL import Image

    with st.sidebar:
        try:
            img = Image.open(r"D:\My_Project\HealthKartDashboard\Assets\LOGO.png")
            st.image(img, caption="🧪 Test Image", width=200)
        except Exception as e:
            st.error(f"Image load error: {e}")

        
        uploaded_influencers = st.file_uploader("Upload Influencers Data (CSV)", type=['csv'])
        uploaded_posts = st.file_uploader("Upload Posts Data (CSV)", type=['csv'])
        uploaded_tracking = st.file_uploader("Upload Tracking Data (CSV)", type=['csv'])
        uploaded_payouts = st.file_uploader("Upload Payouts Data (CSV)", type=['csv'])
        
        if uploaded_influencers and uploaded_posts and uploaded_tracking and uploaded_payouts:
            try:
                # Read uploaded CSVs
                influencers = pd.read_csv(uploaded_influencers)
                posts = pd.read_csv(uploaded_posts)
                tracking_data = pd.read_csv(uploaded_tracking)
                payouts = pd.read_csv(uploaded_payouts)

                # Store into session_state
                st.session_state["influencers"] = influencers
                st.session_state["posts"] = posts
                st.session_state["tracking_data"] = tracking_data
                st.session_state["payouts"] = payouts
                st.session_state["data_loaded"] = True

                st.success("✅ Data uploaded successfully!")
                st.rerun()  # 🔁 Rerun to use new data immediately

            except Exception as e:
                st.error(f"❌ Error reading files: {e}")


        else:
            st.info("Upload all data files or use synthetic data")
            
            if st.button("Generate Synthetic Data"):
                # Generate synthetic data
                influencers, posts, tracking_data, payouts = generate_synthetic_data()
                
                # Store in session state
                st.session_state['influencers'] = influencers
                st.session_state['posts'] = posts
                st.session_state['tracking_data'] = tracking_data
                st.session_state['payouts'] = payouts
                st.session_state['data_loaded'] = True
                
                st.success("Synthetic data generated!")
        
        # Filters Section
        st.markdown("### Filters")
        
        # Get data for filters
        influencers, posts, tracking_data, payouts = load_data()
        
        if influencers is not None:
            # Brand filter
            available_brands = sorted(posts['brand'].unique())
            selected_brands = st.multiselect("Brand", available_brands, default=available_brands)
            
            # Platform filter
            available_platforms = sorted(posts['platform'].unique())
            selected_platforms = st.multiselect("Platform", available_platforms, default=available_platforms)
            
            # Category filter
            available_categories = sorted(influencers['category'].unique())
            selected_categories = st.multiselect("Influencer Category", available_categories, default=available_categories)
            
            # Date range filter
            min_date = pd.to_datetime(tracking_data['date']).min().date()
            max_date = pd.to_datetime(tracking_data['date']).max().date()
            
            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            # Apply filters to session state
            st.session_state['selected_brands'] = selected_brands
            st.session_state['selected_platforms'] = selected_platforms
            st.session_state['selected_categories'] = selected_categories
            st.session_state['date_range'] = date_range
        
        # Export section
        st.markdown("### Export Data")
        
        export_type = st.selectbox("Export Format", ["CSV", "Excel"])
        
        if st.button("Export Dashboard Data"):
            if influencers is not None:
                # Create Excel or CSV with all the data
                if export_type == "Excel":
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        influencers.to_excel(writer, sheet_name='Influencers', index=False)
                        posts.to_excel(writer, sheet_name='Posts', index=False)
                        tracking_data.to_excel(writer, sheet_name='Tracking Data', index=False)
                        payouts.to_excel(writer, sheet_name='Payouts', index=False)
                    
                    output.seek(0)
                    
                    # Download button
                    st.download_button(
                        label="Download Excel",
                        data=output,
                        file_name=f"healthkart_influencer_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:  # CSV
                    # Create CSVs
                    influencer_csv = influencers.to_csv(index=False).encode('utf-8')
                    posts_csv = posts.to_csv(index=False).encode('utf-8')
                    tracking_csv = tracking_data.to_csv(index=False).encode('utf-8')
                    payouts_csv = payouts.to_csv(index=False).encode('utf-8')
                    
                    # Download buttons for each CSV
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download Influencers CSV",
                            data=influencer_csv,
                            file_name=f"healthkart_influencers_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                        st.download_button(
                            label="Download Posts CSV",
                            data=posts_csv,
                            file_name=f"healthkart_posts_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    with col2:
                        st.download_button(
                            label="Download Tracking CSV",
                            data=tracking_csv,
                            file_name=f"healthkart_tracking_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                        st.download_button(
                            label="Download Payouts CSV",
                            data=payouts_csv,
                            file_name=f"healthkart_payouts_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
    # Apply filters to data
    influencers, posts, tracking_data, payouts = load_data()
    
    if influencers is not None and 'selected_brands' in st.session_state:
        # Filter posts
        filtered_posts = posts[
            (posts['brand'].isin(st.session_state['selected_brands'])) &
            (posts['platform'].isin(st.session_state['selected_platforms']))
        ]
        
        # Filter influencers
        filtered_influencers = influencers[
            (influencers['category'].isin(st.session_state['selected_categories'])) &
            (influencers['id'].isin(filtered_posts['influencer_id']))
        ]
        
        # Filter tracking data
        if len(st.session_state['date_range']) == 2:
            start_date, end_date = st.session_state['date_range']
            filtered_tracking = tracking_data[
                (tracking_data['brand'].isin(st.session_state['selected_brands'])) &
                (pd.to_datetime(tracking_data['date']).dt.date >= start_date) &
                (pd.to_datetime(tracking_data['date']).dt.date <= end_date)
            ]
        else:
            filtered_tracking = tracking_data[
                tracking_data['brand'].isin(st.session_state['selected_brands'])
            ]
        
        # Filter payouts for the filtered influencers
        filtered_payouts = payouts[payouts['influencer_id'].isin(filtered_influencers['id'])]
        
        # Calculate metrics based on filtered data
        metrics = calculate_metrics(filtered_influencers, filtered_posts, filtered_tracking, filtered_payouts)
        incremental_roas_data = calculate_incremental_roas(filtered_tracking, filtered_payouts)
        brand_performance = prepare_brand_performance(filtered_tracking, filtered_posts, filtered_payouts, filtered_influencers)
        top_influencers = get_top_influencers(filtered_influencers, incremental_roas_data)
        category_performance, platform_performance = get_persona_insights(filtered_influencers, incremental_roas_data)
        
        # Dashboard Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Campaign Overview", "Influencer Analysis", "ROI & ROAS", "Payouts Tracking"])
        
        #-------------------------
        # Tab 1: Campaign Overview
        #-------------------------
        with tab1:
            # Top metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Total Influencer Revenue</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">₹{metrics["total_influencer_revenue"]:,.2f}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Total Spend</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">₹{metrics["total_spend"]:,.2f}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Overall ROAS</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{metrics["overall_roas"]:.2f}x</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Total Posts</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{metrics["total_posts"]:,}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="sub-header">Brand Performance</div>', unsafe_allow_html=True)
            
            # Brand performance chart
            if not brand_performance.empty:
                fig_brand = px.bar(
                    brand_performance,
                    x='brand',
                    y='revenue',
                    text_auto='.2s',
                    title='Revenue by Brand',
                    color='roas',
                    color_continuous_scale='Viridis',
                    hover_data=['orders', 'num_influencers', 'spend', 'roas']
                )
                fig_brand.update_layout(height=400)
                st.plotly_chart(fig_brand, use_container_width=True)
            else:
                st.info("No brand performance data available with the current filters.")
            
            # Campaign timeline
            st.markdown('<div class="sub-header">Campaign Timeline</div>', unsafe_allow_html=True)
            
            # Prepare data for timeline
            campaign_timeline = filtered_tracking[filtered_tracking['source'] == 'Influencer'].copy()
            campaign_timeline['date'] = pd.to_datetime(campaign_timeline['date'])
            
            if not campaign_timeline.empty:
                timeline_data = campaign_timeline.groupby([pd.Grouper(key='date', freq='W'), 'campaign']).agg({
                    'revenue': 'sum'
                }).reset_index()
                
                fig_timeline = px.line(
                    timeline_data,
                    x='date',
                    y='revenue',
                    color='campaign',
                    title='Weekly Campaign Revenue Over Time',
                    markers=True
                )
                fig_timeline.update_layout(height=400)
                st.plotly_chart(fig_timeline, use_container_width=True)
            else:
                st.info("No campaign timeline data available with the current filters.")
            
            # Campaign performance table
            st.markdown('<div class="sub-header">Campaign Performance Details</div>', unsafe_allow_html=True)
            
            if not filtered_tracking[filtered_tracking['source'] == 'Influencer'].empty:
                campaign_performance = filtered_tracking[filtered_tracking['source'] == 'Influencer'].groupby('campaign').agg({
                    'revenue': 'sum',
                    'orders': 'sum',
                    'user_id': 'nunique'
                }).reset_index()
                
                campaign_performance.columns = ['Campaign', 'Revenue', 'Orders', 'Unique Users']
                campaign_performance['Avg Order Value'] = campaign_performance['Revenue'] / campaign_performance['Orders']
                campaign_performance = campaign_performance.sort_values('Revenue', ascending=False)
                
                st.dataframe(
                    campaign_performance.style.format({
                        'Revenue': '₹{:,.2f}',
                        'Avg Order Value': '₹{:,.2f}'
                    }),
                    use_container_width=True,
                    height=400
                )
            else:
                st.info("No campaign performance data available with the current filters.")
        
        #---------------------------
        # Tab 2: Influencer Analysis
        #---------------------------
        with tab2:
            st.markdown('<div class="sub-header">Top Performing Influencers</div>', unsafe_allow_html=True)
            
            if not top_influencers.empty:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig_top = px.bar(
                        top_influencers,
                        x='name',
                        y='incremental_roas',
                        color='platform',
                        title='Top Influencers by Incremental ROAS',
                        text_auto='.2f',
                        hover_data=['category', 'follower_count', 'actual_revenue', 'spend']
                    )
                    fig_top.update_layout(height=450)
                    st.plotly_chart(fig_top, use_container_width=True)
                
                with col2:
                    st.markdown('<div class="info-text">These influencers have generated the highest incremental ROAS, meaning they drive revenue beyond baseline expectations. They represent the most efficient use of your influencer marketing budget.</div>', unsafe_allow_html=True)
                    
                    # Show top influencer details
                    top_influencer = top_influencers.iloc[0]
                    
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Top Performer</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{top_influencer["name"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-text">Platform: <span class="highlight">{top_influencer["platform"]}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-text">Category: <span class="highlight">{top_influencer["category"]}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-text">Followers: <span class="highlight">{top_influencer["follower_count"]:,}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-text">Incremental ROAS: <span class="highlight">{top_influencer["incremental_roas"]:.2f}x</span></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Influencer engagement metrics
                st.markdown('<div class="sub-header">Influencer Engagement Analysis</div>', unsafe_allow_html=True)
                
                # Prepare data for scatter plot
                influencer_engagement = pd.merge(
                    filtered_influencers,
                    filtered_posts.groupby('influencer_id').agg({
                        'reach': 'sum',
                        'likes': 'sum',
                        'comments': 'sum'
                    }).reset_index(),
                    left_on='id',
                    right_on='influencer_id',
                    how='inner'
                )
                
                if not influencer_engagement.empty:
                    # Calculate engagement rate
                    influencer_engagement['engagement_rate'] = ((influencer_engagement['likes'] + influencer_engagement['comments']) / influencer_engagement['reach']) * 100
                    
                    fig_engagement = px.scatter(
                        influencer_engagement,
                        x='follower_count',
                        y='engagement_rate',
                        size='reach',
                        color='platform',
                        hover_name='name',
                        title='Engagement Rate vs. Follower Count',
                        labels={
                            'follower_count': 'Follower Count',
                            'engagement_rate': 'Engagement Rate (%)'
                        },
                        log_x=True
                    )
                    fig_engagement.update_layout(height=500)
                    st.plotly_chart(fig_engagement, use_container_width=True)
                else:
                    st.info("No influencer engagement data available with the current filters.")
                
                # Influencer table with details
                st.markdown('<div class="sub-header">Influencer Details</div>', unsafe_allow_html=True)
                
                # Merge influencer data with ROAS data
                influencer_table = pd.merge(
                    filtered_influencers,
                    incremental_roas_data,
                    left_on='id',
                    right_on='influencer_id',
                    how='inner'
                )
                
                if not influencer_table.empty:
                    # Select columns to display
                    display_columns = [
                        'name', 'platform', 'category', 'follower_count',
                        'actual_revenue', 'incremental_revenue', 'spend', 'incremental_roas'
                    ]
                    
                    # Rename columns for better display
                    column_names = {
                        'name': 'Name',
                        'platform': 'Platform',
                        'category': 'Category',
                        'follower_count': 'Followers',
                        'actual_revenue': 'Revenue',
                        'incremental_revenue': 'Incremental Revenue',
                        'spend': 'Spend',
                        'incremental_roas': 'Inc. ROAS'
                    }
                    
                    display_df = influencer_table[display_columns].rename(columns=column_names)
                    
                    st.dataframe(
                        display_df.sort_values('Inc. ROAS', ascending=False).style.format({
                            'Followers': '{:,.0f}',
                            'Revenue': '₹{:,.2f}',
                            'Incremental Revenue': '₹{:,.2f}',
                            'Spend': '₹{:,.2f}',
                            'Inc. ROAS': '{:.2f}x'
                        }),
                        use_container_width=True,
                        height=400
                    )
                else:
                    st.info("No influencer details available with the current filters.")
            else:
                st.info("No top influencer data available with the current filters.")
                
        #---------------------------
        # Tab 3: ROI & ROAS Analysis
        #---------------------------
        with tab3:
            st.markdown('<div class="sub-header">Incremental ROAS Analysis</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            # Category performance
            with col1:
                if not category_performance.empty:
                    fig_category = px.bar(
                        category_performance.sort_values('avg_roas', ascending=False),
                        x='category',
                        y='avg_roas',
                        title='Average ROAS by Influencer Category',
                        text_auto='.2f',
                        color='avg_roas',
                        color_continuous_scale='Viridis'
                    )
                    fig_category.update_layout(height=400)
                    st.plotly_chart(fig_category, use_container_width=True)
                else:
                    st.info("No category performance data available with the current filters.")
            
            # Platform performance
            with col2:
                if not platform_performance.empty:
                    fig_platform = px.bar(
                        platform_performance.sort_values('avg_roas', ascending=False),
                        x='platform',
                        y='avg_roas',
                        title='Average ROAS by Platform',
                        text_auto='.2f',
                        color='avg_roas',
                        color_continuous_scale='Viridis'
                    )
                    fig_platform.update_layout(height=400)
                    st.plotly_chart(fig_platform, use_container_width=True)
                else:
                    st.info("No platform performance data available with the current filters.")
            
            # ROI by brand
            st.markdown('<div class="sub-header">ROI by Brand and Campaign</div>', unsafe_allow_html=True)
            
            if not brand_performance.empty:
                fig_roi = px.bar(
                    brand_performance.sort_values('roas', ascending=False),
                    x='brand',
                    y=['revenue', 'spend'],
                    title='Revenue vs Spend by Brand',
                    barmode='group'
                )
                
                # Add ROAS as a line on secondary y-axis
                fig_roi.add_scatter(
                    x=brand_performance['brand'],
                    y=brand_performance['roas'],
                    mode='lines+markers',
                    name='ROAS',
                    yaxis='y2'
                )
                
                # Update layout for secondary y-axis
                fig_roi.update_layout(
                    yaxis2=dict(
                        title='ROAS',
                        overlaying='y',
                        side='right'
                    ),
                    height=500,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig_roi, use_container_width=True)
                
                # Campaign ROI table
                st.markdown('<div class="sub-header">Campaign ROI Details</div>', unsafe_allow_html=True)
                
                # Get campaign data
                campaign_data = filtered_tracking[filtered_tracking['source'] == 'Influencer'].groupby('campaign').agg({
                    'revenue': 'sum',
                    'orders': 'sum',
                    'influencer_id': 'nunique'
                }).reset_index()
                
                # Add spend data
                campaign_spend = []
                for campaign in campaign_data['campaign']:
                    # Extract brand
                    brand = campaign.split('_')[0]
                    
                    # Get influencers in this campaign
                    campaign_influencers = filtered_tracking[
                        (filtered_tracking['campaign'] == campaign) & 
                        (filtered_tracking['source'] == 'Influencer')
                    ]['influencer_id'].unique()
                    
                    # Calculate spend
                    campaign_spend_value = filtered_payouts[
                        filtered_payouts['influencer_id'].isin(campaign_influencers)
                    ]['total_payout'].sum()
                    
                    campaign_spend.append(campaign_spend_value)
                
                campaign_data['spend'] = campaign_spend
                campaign_data['roas'] = campaign_data['revenue'] / campaign_data['spend']
                campaign_data['roas'] = campaign_data['roas'].replace([np.inf, -np.inf], 0)
                
                # Rename columns for display
                campaign_data.columns = ['Campaign', 'Revenue', 'Orders', 'Influencers', 'Spend', 'ROAS']
                
                # Sort and display
                campaign_table = campaign_data.sort_values('ROAS', ascending=False)
                
                st.dataframe(
                    campaign_table.style.format({
                        'Revenue': '₹{:,.2f}',
                        'Spend': '₹{:,.2f}',
                        'ROAS': '{:.2f}x'
                    }),
                    use_container_width=True,
                    height=400
                )
            else:
                st.info("No ROI data available with the current filters.")
        
        #---------------------------
        # Tab 4: Payouts Tracking
        #---------------------------
        with tab4:
            st.markdown('<div class="sub-header">Influencer Payout Tracking</div>', unsafe_allow_html=True)
            
            # Payout summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Total Payout Amount</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">₹{filtered_payouts["total_payout"].sum():,.2f}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Average Payout per Influencer</div>', unsafe_allow_html=True)
                avg_payout = filtered_payouts["total_payout"].mean() if len(filtered_payouts) > 0 else 0
                st.markdown(f'<div class="metric-value">₹{avg_payout:,.2f}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Influencers Paid</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{len(filtered_payouts):,}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Payout by type
            st.markdown('<div class="sub-header">Payout by Payment Basis</div>', unsafe_allow_html=True)
            
            if not filtered_payouts.empty:
                payout_by_basis = filtered_payouts.groupby('basis').agg({
                    'total_payout': 'sum',
                    'influencer_id': 'count'
                }).reset_index()
                
                payout_by_basis.columns = ['Payment Basis', 'Total Payout', 'Number of Influencers']
                
                fig_payout = px.pie(
                    payout_by_basis,
                    values='Total Payout',
                    names='Payment Basis',
                    title='Distribution of Payouts by Payment Basis',
                    hole=0.4
                )
                fig_payout.update_layout(height=400)
                st.plotly_chart(fig_payout, use_container_width=True)
                
                # Payout details
                st.markdown('<div class="sub-header">Influencer Payout Details</div>', unsafe_allow_html=True)
                
                # Merge influencer info with payouts
                payout_details = pd.merge(
                    filtered_payouts,
                    filtered_influencers[['id', 'name', 'platform', 'category', 'follower_count']],
                    left_on='influencer_id',
                    right_on='id',
                    how='left'
                )
                
                # Select columns for display
                payout_display = payout_details[[
                    'name', 'platform', 'category', 'follower_count',
                    'basis', 'rate', 'posts', 'orders', 'total_payout'
                ]]
                
                payout_display.columns = [
                    'Name', 'Platform', 'Category', 'Followers',
                    'Payment Basis', 'Rate', 'Posts', 'Orders', 'Total Payout'
                ]
                
                st.dataframe(
                    payout_display.sort_values('Total Payout', ascending=False).style.format({
                        'Followers': '{:,.0f}',
                        'Rate': '₹{:,.2f}',
                        'Total Payout': '₹{:,.2f}'
                    }),
                    use_container_width=True,
                    height=400
                )
                
                # Cost efficiency analysis
                st.markdown('<div class="sub-header">Cost Efficiency Analysis</div>', unsafe_allow_html=True)
                
                # Merge payout data with revenue data
                efficiency_data = pd.merge(
                    payout_details,
                    incremental_roas_data[['influencer_id', 'actual_revenue', 'incremental_revenue', 'incremental_roas']],
                    on='influencer_id',
                    how='left'
                )
                
                # Calculate cost per engagement
                post_engagement = filtered_posts.groupby('influencer_id').agg({
                    'likes': 'sum',
                    'comments': 'sum',
                    'reach': 'sum'
                }).reset_index()
                
                efficiency_data = pd.merge(
                    efficiency_data,
                    post_engagement,
                    left_on='influencer_id',
                    right_on='influencer_id',
                    how='left'
                )
                
                efficiency_data['total_engagements'] = efficiency_data['likes'] + efficiency_data['comments']
                efficiency_data['cost_per_engagement'] = efficiency_data['total_payout'] / efficiency_data['total_engagements']
                efficiency_data['cost_per_reach'] = efficiency_data['total_payout'] / efficiency_data['reach']
                efficiency_data['revenue_per_post'] = efficiency_data['actual_revenue'] / efficiency_data['posts']
                
                # Filter out rows with potential division by zero issues
                efficiency_data = efficiency_data.replace([np.inf, -np.inf], np.nan).dropna(
                    subset=['cost_per_engagement', 'cost_per_reach', 'revenue_per_post', 'incremental_roas']
                )
                
                if not efficiency_data.empty:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_cost = px.scatter(
                            efficiency_data,
                            x='cost_per_engagement',
                            y='incremental_roas',
                            size='follower_count',
                            color='platform',
                            hover_name='name',
                            title='Cost per Engagement vs. Incremental ROAS',
                            labels={
                                'cost_per_engagement': 'Cost per Engagement (₹)',
                                'incremental_roas': 'Incremental ROAS'
                            },
                            log_x=True
                        )
                        st.plotly_chart(fig_cost, use_container_width=True)
                    
                    with col2:
                        fig_rev = px.scatter(
                            efficiency_data,
                            x='revenue_per_post',
                            y='cost_per_reach',
                            size='follower_count',
                            color='platform',
                            hover_name='name',
                            title='Revenue per Post vs. Cost per Reach',
                            labels={
                                'revenue_per_post': 'Revenue per Post (₹)',
                                'cost_per_reach': 'Cost per Reach (₹)'
                            },
                            log_x=True,
                            log_y=True
                        )
                        st.plotly_chart(fig_rev, use_container_width=True)
                else:
                    st.info("Insufficient data for cost efficiency analysis with the current filters.")
            else:
                st.info("No payout data available with the current filters.")

# Run the app
if __name__ == "__main__":
    main()
