# HealthKart Influencer Campaign Dashboard

A comprehensive dashboard to track and visualize the ROI of influencer marketing campaigns for HealthKart.

## Overview

This dashboard helps HealthKart track and analyze the performance of influencer marketing campaigns across various social platforms. It provides insights into campaign performance, influencer ROI, incremental ROAS, and payout tracking.

## Features

- **Campaign Performance Tracking**: Monitor revenue, orders, and engagement metrics across different campaigns
- **Influencer Analysis**: Identify top-performing influencers and analyze their impact on sales
- **ROI & ROAS Calculation**: Calculate both standard and incremental Return on Ad Spend
- **Payout Tracking**: Track payments to influencers by post or by order
- **Filtering**: Filter data by brand, product, influencer category, platform, and date range
- **Data Visualization**: Interactive charts and tables for better insights
- **Export Functionality**: Export data to CSV or Excel formats

## Assumptions

1. **Incrementality Calculation**: The incremental value is calculated by comparing influencer-driven conversions to baseline conversion rates from non-influencer channels.
2. **Data Structure**: 
   - Influencers are categorized by platform, follower count, and content category
   - Posts are tracked with engagement metrics (reach, likes, comments)
   - Orders are tracked with attribution to specific campaigns and influencers
   - Payouts can be based on post count, order count, or a hybrid model
3. **Attribution**: Direct attribution is assigned when a user comes from an influencer link/code

## Data Model

The dashboard uses four primary datasets:

1. **Influencers**: Contains details about each influencer including their platform, category, and follower count
2. **Posts**: Tracks each post made by influencers with metrics like reach, likes, and comments
3. **Tracking Data**: Records order and revenue data attributed to each influencer and campaign
4. **Payouts**: Tracks payment information for each influencer based on their contract type

## Setup Instructions

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   streamlit run app.py
   ```

3. Upload your data or use the synthetic data generation feature for testing

## Using the Dashboard

- Use the sidebar filters to focus on specific brands, platforms, or time periods
- Navigate between tabs to explore different aspects of the influencer marketing performance
- Export data using the export buttons in the sidebar

## Key Metrics Explained

- **ROAS (Return on Ad Spend)**: Revenue / Spend
- **Incremental ROAS**: (Actual Revenue - Expected Revenue) / Spend
- **Expected Revenue**: Based on baseline conversion rates from non-influencer channels
- **Cost per Engagement**: Total Spend / (Likes + Comments)
- **Cost per Reach**: Total Spend / Total Reach