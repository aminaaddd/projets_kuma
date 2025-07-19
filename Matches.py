import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
from mplsoccer import PyPizza
import matplotlib.pyplot as plt



st.set_page_config(page_title="Match results", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif !important;
    }

    section[data-testid="stSidebar"] {
        font-family: 'Poppins', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #2c3e50;
    }
    .stDataFrame, .stTable {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)



instat_max_value = 600

df = pd.read_excel("utils/06_09_2021_matches_Algeria.xlsx")
df = df.dropna(how="all") 

df["Opponent"] = df["Opponent"].str.replace("vs ", "", regex=False)
df["Opponent"] = df["Opponent"].str.replace("@ ", "", regex=False)
df = df[df["Opponent"].notna() & (df["Opponent"].str.strip() != "")]

# ====== TABLE OF SELECTIONS ======
st.title("Match Performance Dashboard")

colonnes_affichage = ['Opponent', 'Score']
df_display = df[colonnes_affichage].copy()
df_display.insert(0, "Select", [False]*len(df_display))

edited = st.data_editor(
    df_display,
    use_container_width=True,
    num_rows="fixed",
    hide_index=True,
    key="table_select"
)
selected_rows = edited[edited["Select"] == True]

# ====== INSTATS ======
if not selected_rows.empty:
    selected_rows = selected_rows.merge(df[["Opponent", "InStat Index"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Shots"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Goals"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Shots on target"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Shots wide"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Blocked shots"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Shots on post / bar"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Challenges in defence won, %"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Challenges in attack won, %"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Air challenges won, %"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Ball possession, %"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Fouls"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Yellow cards"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Red cards"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Corners"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Offsides"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Penalties"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Penalties\n scored"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "Free-kick shots"]], on="Opponent", how="left")
    selected_rows = selected_rows.merge(df[["Opponent", "% scored free kick shots"]], on="Opponent", how="left")



    selected_rows["Goals"] = pd.to_numeric(selected_rows["Goals"], errors="coerce")
    selected_rows["InStat Index"] = pd.to_numeric(selected_rows["InStat Index"], errors="coerce")

    with st.container():
        st.markdown("""
            <div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <h4>InStat Performance Score</h4>
            </div>
        """, unsafe_allow_html=True)

    cols = st.columns(len(selected_rows))

    for i, (_, row) in enumerate(selected_rows.iterrows()):
        instat = row["InStat Index"]
        opponent = row["Opponent"]

        with cols[i]:
            fig = go.Figure(data=[go.Pie(
                labels=["InStat", "Rest"],
                values=[instat, instat_max_value - instat],
                hole=0.6,
                marker_colors=["green", "lightgray"],
                textinfo='none'
            )])

            fig.update_layout(
                showlegend=False,
                title_text=f"<b>{opponent}</b>",
                title_font_size=16,
                title_x=0.1,  
                annotations=[dict(text=str(instat), x=0.5, y=0.5, font_size=20, showarrow=False)],
                margin=dict(t=50, b=5, l=5, r=5),  
                height=250,
                width=250
            )
            st.plotly_chart(fig)

    
   # ====== CATEGORIES ======
    categories = {
        "Shots": "#27ae60",       
        "Passes": "#2980b9",      
        "Challenges": "#c0392b",       
        "Pressing": "#16a085",    
        "Possession": "#8e44ad",  
        "Fouls": "#d35400"        
    }

    st.markdown("### Select a category")

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Shots"

    cols = st.columns(len(categories))

    for i, (cat, color) in enumerate(categories.items()):
        with cols[i]:
            if st.button(cat, key=f"btn_{cat}", use_container_width=True):
                st.session_state.selected_category = cat

            if st.session_state.selected_category == cat:
                st.markdown(f"""
                    <style>
                    div[data-testid="stButton"][key="btn_{cat}"] button {{
                        background-color: {color};
                        color: white;
                        border: 2px solid black;
                        border-radius: 10px;
                        font-weight: bold;
                        padding: 10px 16px;
                    }}
                    </style>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <style>
                    div[data-testid="stButton"][key="btn_{cat}"] button {{
                        background-color: white;
                        color: black;
                        border: 2px solid {color};
                        border-radius: 10px;
                        font-weight: bold;
                        padding: 10px 16px;
                    }}
                    </style>
                """, unsafe_allow_html=True)

    selected = st.session_state.selected_category

    
    if selected == "Shots":
        
        # shots (goals)

        selected_rows["Goals"] = pd.to_numeric(selected_rows["Goals"], errors="coerce")
        bar_chart = alt.Chart(selected_rows).mark_bar(opacity=0.6).encode(
            x=alt.X("Opponent:N", sort="-y", axis=alt.Axis(labelAngle=-45, title="Opponent")),
            y=alt.Y("Shots:Q", title="Shots"),
            color=alt.Color("Goals:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="Goals")),
            tooltip=["Opponent", "Shots", "Goals"]
        ).properties(
            width=600,
            height=400,
            title="Total Shots"
        )

        st.altair_chart(bar_chart, use_container_width=True)
            
        shot_columns = ["Shots on target", "Shots wide", "Blocked shots", "Shots on post / bar"]

        selected_rows[shot_columns] = selected_rows[shot_columns].apply(pd.to_numeric, errors="coerce")
        
        # ==== shot types

        green_gradient = ["#67ABE2", "#416AC4", "#160F58", "#8581BE"]
        fig_shots = px.bar(
            selected_rows,
            x="Opponent",
            y=["Shots on target", "Shots wide", "Blocked shots", "Shots on post / bar"],
            title="Shots Distribution per Opponent",
            barmode="group",
            color_discrete_sequence=green_gradient,
            opacity=0.6
        )
        fig_shots.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_shots, use_container_width=True)
        
        #
        with st.expander("Corners / Offsides"):

            st.dataframe(selected_rows[["Opponent", "Corners", "Offsides"]], hide_index=True)
            
        with st.expander("Penalties"):

            st.dataframe(selected_rows[["Opponent", "Penalties", "Penalties\n scored"]], hide_index=True)
        
        with st.expander("Free-kick"):

            st.dataframe(selected_rows[["Opponent", "Free-kick shots", "% scored free kick shots"]], hide_index=True)

        
        # Expected goals
        selected_rows["xG (Expected goals)"] = pd.to_numeric(df["xG (Expected goals)"], errors="coerce")
        selected_rows["Opponent's xG"] = pd.to_numeric(df["Opponent's xG"], errors="coerce")
        selected_rows["Date"] = pd.to_datetime(df["Date"]) 

        fig = px.line(
            selected_rows,
            x="Date",
            y=["xG (Expected goals)", "Opponent's xG"],
            title="Expected Goals vs Opponent's xG Over Time",
            markers=True,
            hover_data={"Opponent": True, "Date": True}
        )
        fig.update_layout(
            xaxis_title="Match Date",
            yaxis_title="Expected Goals",
            legend_title="Metric",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True),
            colorway=["#2C3E50", "#6CA0DC"]
        )
        st.plotly_chart(fig, use_container_width=True)
        
        
    if selected == "Passes":
        
        # Accurate /key passes 
        
        fig = px.bar(
            df,
            x="Opponent",
            y=["Accurate passes", "Key passes"],
            barmode="group",
            title="Pass Comparison per Opponent",
            color_discrete_sequence=["#2980b9", "#f39c12"],
            hover_data={"Goals": True},
            opacity=0.6
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Opponent",
            yaxis_title="Number of passes",
            xaxis_tickangle=-45,
            legend_title="Pass type",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    
    if selected == "Challenges":

        st.markdown("### Duels Won by Type")

        challenge_cols = [
            'Challenges in defence won, %',
            'Challenges in attack won, %',
            'Air challenges won, %'
        ]


        if not all(col in selected_rows.columns for col in challenge_cols):
            st.error("Required columns for duels are missing")
        else:
            for col in challenge_cols:
                selected_rows[col] = selected_rows[col].astype(str).str.replace('%', '').str.strip()
                selected_rows[col] = pd.to_numeric(selected_rows[col], errors="coerce")

            params = ["Defense", "Attack", "Aerial"]
            slice_colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

            challenge_cols = [
                'Challenges in defence won, %',
                'Challenges in attack won, %',
                'Air challenges won, %'
            ]
            fig_radar = go.Figure()


            for i, row in selected_rows.iterrows():
                values = [row[col] for col in challenge_cols]
                if any(pd.isna(values)):
                    continue       

                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=params,
                    fill='toself',
                    name=row["Opponent"],
                    opacity=0.4  
                ))

            if not fig_radar.data:
                st.warning("No complete data available")
            else:
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100])
                    ),
                    showlegend=True,
                    title="Comparison of Duels Won (%)",
                    height=600,
                    template="plotly_white"
                )
                st.plotly_chart(fig_radar, use_container_width=True, key="radar_challenges_all")

        
    if selected == "Possession":
        
        # Ball possession (%)

        fig = px.bar(
            selected_rows,
            y="Opponent",
            x="Ball possession, %",
            orientation='h',
            text="Ball possession, %",
            title="Ball Possession",
            color="Opponent",
            color_discrete_sequence=px.colors.qualitative.Set2,
            opacity=0.6
        )

        fig.update_traces(textposition='inside')
        fig.update_layout(
            xaxis_title="Ball possession (%)",
            yaxis_title="Opponent",
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)
        
    
    if selected == "Fouls":
        
        # Total fouls
        
        fig = px.bar(
            selected_rows,
            x="Opponent",
            y="Fouls",
            color="Opponent",
            title="Number of Fouls per Opponent",
            color_discrete_sequence=px.colors.qualitative.Set2,
            opacity=0.6
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Opponent",
            yaxis_title="Number of Fouls",
            showlegend=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
        
        
        st.dataframe(selected_rows[["Opponent", "Yellow cards", "Red cards"]], hide_index=True)
        
   










            
        

        






