import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

st.set_page_config(page_title="Serie A Dashboard", layout="wide", initial_sidebar_state="expanded", page_icon="⚽")

st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #181818;
        color: #f5f6fa;
    }
    .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2 {
        background-color: #181818 !important;
        color: #f5f6fa !important;
    }
    .stDataFrame, .stTable {
        background-color: #222 !important;
        color: #f5f6fa !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def load_seriea_data():
    data_path = os.path.join('Datasets', 'Cleaned Datasets', 'Serie_A_Stats_Italy.csv')
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df = df[df['year'] >= (df['year'].max() - 4)]
        return df
    return None

def seriea_overview(df):
    matches_per_year = df.groupby('year').size()
    teams_per_year = df.groupby('year')['team'].nunique()
    avg_gf = df.groupby('year')['gf'].mean()
    avg_ga = df.groupby('year')['ga'].mean()
    avg_poss = df.groupby('year')['poss'].mean()
    overview_table = pd.DataFrame({
        'Năm': matches_per_year.index,
        'Số trận': matches_per_year.values,
        'Số đội': teams_per_year.values,
        'TB bàn thắng (GF)': avg_gf.round(2).values,
        'TB bàn thua (GA)': avg_ga.round(2).values,
        'TB kiểm soát bóng (%)': avg_poss.round(2).values
    })
    return overview_table, matches_per_year, avg_gf, avg_ga, avg_poss

def plotly_bar_line(matches_per_year, goals_per_year):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=matches_per_year.index, y=matches_per_year.values, name='Số trận', marker_color='#00b894'))
    fig.add_trace(go.Scatter(x=goals_per_year.index, y=goals_per_year.values, name='Tổng bàn thắng', mode='lines+markers', marker_color='#d63031'))
    fig.update_layout(
        barmode='group',
        title='Số trận & Tổng bàn thắng theo năm',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
        xaxis=dict(title='Năm', color='#f5f6fa'),
        yaxis=dict(title='Số trận', color='#f5f6fa'),
        yaxis2=dict(title='Tổng bàn thắng', overlaying='y', side='right', color='#f5f6fa')
    )
    return fig

def plotly_pie(result_counts):
    fig = px.pie(
        names=result_counts.index,
        values=result_counts.values,
        color_discrete_sequence=['#4CAF50','#FFC107','#F44336']
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        title='Tỷ lệ Thắng/Hòa/Thua',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
    )
    return fig

def plotly_hist(series, title, color, xlabel):
    fig = px.histogram(series, nbins=20, color_discrete_sequence=[color])
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title='Số trận',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
    )
    return fig

def plotly_team_stats(team_stats):
    fig = px.bar(team_stats, x='team', y=['win','draw','lose'],
                 title='Thành tích các đội (Win/Draw/Lose)',
                 color_discrete_sequence=['#4CAF50','#FFC107','#F44336'])
    fig.update_layout(
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
        barmode='group',
        xaxis_title='Đội',
        yaxis_title='Số trận',
    )
    return fig

def plotly_line(points_by_date):
    fig = px.line(points_by_date, x=points_by_date.index, y=points_by_date.values, title='Tích lũy điểm theo thời gian', markers=True)
    fig.update_layout(
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
        xaxis_title='Ngày',
        yaxis_title='Tổng điểm tích lũy',
    )
    return fig

def plotly_scatter(df, x, y, color, title, xlabel, ylabel):
    fig = px.scatter(df, x=x, y=y, color=color, title=title)
    fig.update_layout(
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
        xaxis_title=xlabel,
        yaxis_title=ylabel,
    )
    return fig

def plotly_box(df, x, y, title):
    fig = px.box(df, x=x, y=y, title=title, color=x, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
    )
    return fig

def plotly_heatmap(pivot, title):
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='YlGnBu',
        colorbar=dict(title='Winrate')
    ))
    fig.update_layout(
        title=title,
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
    )
    return fig

def plotly_bar(df, x, y, title, color='#00b894'):
    fig = px.bar(df, x=x, y=y, title=title, color_discrete_sequence=[color])
    fig.update_layout(
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
    )
    return fig

def plotly_grouped_bar(df, x, y, color, title):
    fig = px.bar(df, x=x, y=y, color=color, barmode='group', title=title)
    fig.update_layout(
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='#f5f6fa',
    )
    return fig

st.title("Serie A Dashboard")
df = load_seriea_data()
tab1, tab2 = st.tabs(["Thống kê", "Dự đoán"])
with tab1:
    if df is not None:
        overview_table, matches_per_year, avg_gf, avg_ga, avg_poss = seriea_overview(df)
        st.subheader("Tổng quan 5 mùa gần nhất")
        st.dataframe(overview_table, use_container_width=True, hide_index=True)
        goals_per_year = df.groupby('year')['gf'].sum()
        st.plotly_chart(plotly_bar_line(matches_per_year, goals_per_year), use_container_width=True)
        result_counts = df['result'].value_counts()
        st.plotly_chart(plotly_pie(result_counts), use_container_width=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(plotly_hist(df['gf'].dropna(), 'Phân bố số bàn thắng (GF)', 'blue', 'Bàn thắng/trận'), use_container_width=True)
        with col2:
            st.plotly_chart(plotly_hist(df['sh'].dropna(), 'Phân bố số cú sút (sh)', 'orange', 'Số cú sút/trận'), use_container_width=True)
        with col3:
            st.plotly_chart(plotly_hist(df['xg'].dropna(), 'Phân bố xG', 'green', 'xG/trận'), use_container_width=True)
        team_stats = df.groupby('team').agg(
            matches=('result', 'count'),
            win=('result', lambda x: (x=='W').sum()),
            draw=('result', lambda x: (x=='D').sum()),
            lose=('result', lambda x: (x=='L').sum()),
            goals=('gf', 'sum'),
            points=('result', lambda x: (x=='W').sum()*3 + (x=='D').sum())
        ).reset_index()
        team_stats['winrate'] = (team_stats['win'] / team_stats['matches'] * 100).round(2)
        st.subheader("Thành tích các đội bóng")
        st.dataframe(team_stats, use_container_width=True, hide_index=True)
        st.plotly_chart(plotly_team_stats(team_stats), use_container_width=True)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.sort_values('date')
        df['points'] = df['result'].map({'W':3, 'D':1, 'L':0})
        points_by_date = df.groupby('date')['points'].sum().cumsum()
        st.plotly_chart(plotly_line(points_by_date), use_container_width=True)
        top5_xg = df.groupby('team')[['xg','gf']].sum().sort_values('xg', ascending=False).head(5).reset_index()
        fig_top5 = go.Figure()
        fig_top5.add_trace(go.Bar(x=top5_xg['team'], y=top5_xg['xg'], name='xG', marker_color='#00b894'))
        fig_top5.add_trace(go.Bar(x=top5_xg['team'], y=top5_xg['gf'], name='GF', marker_color='#d63031'))
        fig_top5.update_layout(
            barmode='group',
            title='Top 5 đội có xG cao nhất vs số bàn thật',
            plot_bgcolor='#181818',
            paper_bgcolor='#181818',
            font_color='#f5f6fa',
        )
        st.plotly_chart(fig_top5, use_container_width=True)
        st.plotly_chart(plotly_scatter(df, 'xg', 'gf', 'team', 'So sánh xG vs GF', 'xG', 'Bàn thắng (GF)'), use_container_width=True)
        if 'captain' in df.columns:
            captain_counts = df['captain'].value_counts().head(10)
            st.subheader('Top đội trưởng ra sân nhiều nhất')
            st.bar_chart(captain_counts, use_container_width=True)
        formation_counts = df['formation'].value_counts().head(10)
        st.subheader('Top 10 sơ đồ chiến thuật phổ biến')
        st.bar_chart(formation_counts, use_container_width=True)
        if 'opp_formation' in df.columns:
            pivot = pd.pivot_table(df, values='result', index='formation', columns='opp_formation', aggfunc=lambda x: (x=='W').mean())
            st.subheader('Tỷ lệ thắng theo formation và opp formation')
            st.plotly_chart(plotly_heatmap(pivot, 'Tỷ lệ thắng theo formation và opp formation'), use_container_width=True)
        venue_stats = df.groupby('venue').agg(
            avg_gf=('gf','mean'),
            avg_xg=('xg','mean'),
            avg_points=('points','mean')
        ).reset_index()
        st.subheader('Thống kê theo sân (venue)')
        st.dataframe(venue_stats, use_container_width=True, hide_index=True)
        st.plotly_chart(plotly_box(df, 'venue', 'gf', 'Phân bố bàn thắng (GF) theo venue'), use_container_width=True)
        st.plotly_chart(plotly_box(df, 'venue', 'xg', 'Phân bố xG theo venue'), use_container_width=True)
        venue_result = df.groupby(['venue','result']).size().unstack(fill_value=0).reset_index()
        venue_result_melt = venue_result.melt(id_vars='venue', var_name='result', value_name='count')
        st.plotly_chart(plotly_grouped_bar(venue_result_melt, 'venue', 'count', 'result', 'Kết quả theo venue'), use_container_width=True)
        df['g-xg'] = df['gf'] - df['xg']
        df['g/sh'] = df['gf'] / df['sh'].replace(0,np.nan)
        df['g/sot'] = df['gf'] / df['sot'].replace(0,np.nan)
        df['sot%'] = df['sot'] / df['sh'].replace(0,np.nan)
        eff_team = df.groupby('team').agg({'g-xg':'mean','g/sh':'mean','g/sot':'mean','sot%':'mean'}).sort_values('g-xg',ascending=False).reset_index()
        st.subheader('Hiệu quả ghi bàn của các đội')
        st.dataframe(eff_team, use_container_width=True, hide_index=True)
        st.plotly_chart(plotly_scatter(df, 'xg', 'g-xg', 'team', 'Hiệu quả ghi bàn: g-xg vs xg', 'xG', 'g-xg'), use_container_width=True)
        top_eff = eff_team.head(5)
        fig_top_eff = go.Figure()
        fig_top_eff.add_trace(go.Bar(x=top_eff['team'], y=top_eff['g/sh'], name='g/sh', marker_color='#00b894'))
        fig_top_eff.add_trace(go.Bar(x=top_eff['team'], y=top_eff['g/sot'], name='g/sot', marker_color='#fdcb6e'))
        fig_top_eff.update_layout(
            barmode='group',
            title='Top đội hiệu suất dứt điểm cao',
            plot_bgcolor='#181818',
            paper_bgcolor='#181818',
            font_color='#f5f6fa',
        )
        st.plotly_chart(fig_top_eff, use_container_width=True)
        if 'referee' in df.columns:
            ref_stats = df.groupby('referee').agg(
                matches=('result','count'),
                winrate=('result', lambda x: (x=='W').mean()*100)
            ).sort_values('matches',ascending=False).head(10).reset_index()
            st.subheader('Top 10 trọng tài bắt nhiều trận nhất')
            st.dataframe(ref_stats, use_container_width=True, hide_index=True)
            st.plotly_chart(plotly_bar(ref_stats, 'referee', 'matches', 'Top 10 trọng tài bắt nhiều trận nhất', color='#636e72'), use_container_width=True)
        if 'attendance' in df.columns:
            att_stats = df.groupby('team')['attendance'].mean().sort_values(ascending=False).head(10)
            st.subheader('Trung bình attendance theo đội')
            st.bar_chart(att_stats, use_container_width=True)
            att_win = df.groupby('team').agg({'attendance':'mean','result': lambda x: (x=='W').mean()*100}).reset_index()
            st.plotly_chart(plotly_scatter(att_win, 'attendance', 'result', None, 'Correlation attendance và winrate', 'Attendance', 'Winrate (%)'), use_container_width=True)
        overperform = df.groupby('team').agg({'xg':'mean','result': lambda x: (x=='W').mean()*100})
        overperform = overperform.sort_values(['result','xg'], ascending=[False,True]).head(5).reset_index()
        fig_over = go.Figure()
        fig_over.add_trace(go.Bar(x=overperform['team'], y=overperform['result'], name='Winrate', marker_color='#00b894'))
        fig_over.add_trace(go.Bar(x=overperform['team'], y=overperform['xg'], name='xG', marker_color='#d63031', yaxis='y2'))
        fig_over.update_layout(
            title='Top đội overperform (xG thấp, winrate cao)',
            plot_bgcolor='#181818',
            paper_bgcolor='#181818',
            font_color='#f5f6fa',
            yaxis2=dict(overlaying='y', side='right', title='xG')
        )
        st.plotly_chart(fig_over, use_container_width=True)
        choke = df.groupby('team').agg({'xg':'mean','result': lambda x: (x=='W').mean()*100})
        choke = choke.sort_values(['xg','result'], ascending=[False,True]).head(5).reset_index()
        fig_choke = go.Figure()
        fig_choke.add_trace(go.Bar(x=choke['team'], y=choke['xg'], name='xG', marker_color='#fdcb6e'))
        fig_choke.add_trace(go.Bar(x=choke['team'], y=choke['result'], name='Winrate', marker_color='#636e72', yaxis='y2'))
        fig_choke.update_layout(
            title='Top đội choke (xG cao, winrate thấp)',
            plot_bgcolor='#181818',
            paper_bgcolor='#181818',
            font_color='#f5f6fa',
            yaxis2=dict(overlaying='y', side='right', title='Winrate')
        )
        st.plotly_chart(fig_choke, use_container_width=True)
        formation_win = df.groupby('formation').agg({'result': lambda x: (x=='W').mean()*100})
        formation_win = formation_win.sort_values('result', ascending=False).head(10).reset_index()
        st.plotly_chart(plotly_bar(formation_win, 'formation', 'result', 'Tỷ lệ thắng theo formation'), use_container_width=True)
        venue_win = df.groupby('venue').agg({'result': lambda x: (x=='W').mean()*100}).reset_index()
        st.plotly_chart(plotly_bar(venue_win, 'venue', 'result', 'Tỷ lệ thắng theo venue', color='#fdcb6e'), use_container_width=True)
        if 'gk' in df.columns and 'xga' in df.columns and 'ga' in df.columns:
            gk_stats = df.groupby('gk').agg({'xga':'mean','ga':'mean'}).dropna()
            gk_stats['save_eff'] = gk_stats['xga'] - gk_stats['ga']
            best_gk = gk_stats.sort_values('save_eff', ascending=True).head(5).reset_index()
            fig_gk = go.Figure()
            fig_gk.add_trace(go.Bar(x=best_gk['gk'], y=best_gk['xga'], name='xGA', marker_color='#00b894'))
            fig_gk.add_trace(go.Bar(x=best_gk['gk'], y=best_gk['ga'], name='GA', marker_color='#d63031'))
            fig_gk.update_layout(
                barmode='group',
                title='Top thủ môn cứu thua tốt nhất (xGA thấp hơn GA)',
                plot_bgcolor='#181818',
                paper_bgcolor='#181818',
                font_color='#f5f6fa',
            )
            st.plotly_chart(fig_gk, use_container_width=True)
    else:
        st.warning("Không tìm thấy dữ liệu Serie A.") 