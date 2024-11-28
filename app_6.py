import pandas as pd
import pulp
import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ShiftScheduler import ShiftScheduler
import matplotlib.pyplot as plt


st.sidebar.title("データのアップロード")

secect_file_cal=st.sidebar.file_uploader("カレンダー")
secect_file_staff=st.sidebar.file_uploader("スタッフ")

st.title("シフトスケジューリングアプリ")

tab_titles=["カレンダー情報","スタッフ情報","シフト表作成"]
tab1,tab2,tab3=st.tabs(tab_titles)

with tab1:
    st.header("カレンダー情報") 
    if secect_file_cal is not None:
        df_cal=pd.read_csv(secect_file_cal)
        st.write(df_cal)

with tab2:
    st.header("スタッフ情報")
    if secect_file_staff is not None:
        df_staff=pd.read_csv(secect_file_staff)
        st.write(df_staff)

with tab3:
    st.header("シフト表作成")
    if secect_file_staff is None:
        st.write("スタッフ情報をアップロードしてください")
    if secect_file_cal is None:
        st.write("カレンダー情報をアップロードしてください")

    if secect_file_staff is not None:
        if secect_file_cal is not None:
    
            if st.button("最適化実行"):
                ss=ShiftScheduler()
                ss.set_data(df_staff,df_cal)
                ss.build_model()
                ss.solve()
                print(ss.sch_df)
            
                st.write("シフト数の充足確認")
                df_sif=ss.sch_df.copy()
                df_sif=df_sif.T
                df_sif_sum=df_sif.sum()
                #st.write(df_sif_sum)
                plt.bar(df_sif_sum.index.values.tolist(),df_sif_sum)
                st.pyplot()
                
            
                st.write("スタッフの希望の確認")
                df_st_num=ss.sch_df.copy()
                df_st_num_sum=df_st_num.sum()
                plt.bar(df_st_num_sum.index.values.tolist(),df_st_num_sum)
                st.pyplot()
            
                st.write("責任者の合計シフト数の充足確認")
                maneger_list=df_staff.copy()
                maneger_list=maneger_list[maneger_list["責任者フラグ"]==1]
                maneger_list=maneger_list["スタッフID"].unique().tolist()
                m_df=df_st_num.T[maneger_list]
                m_df=m_df.T
                m_df_sum=m_df.sum()
                plt.bar(m_df_sum.index.values.tolist(),m_df_sum)
                st.pyplot()
                
                st.download_button(
                label="シフト表をダウンロード",
                data=ss.sch_df.to_csv().encode("utf-8"),
                file_name="output.csv",
                mime="text/csv",
                )
                