import psycopg2
import pandas.io.sql as psql
import psycopg2.extras
import streamlit as st
import pandas as pd
import io
import datetime as dt



def conn_db():
    db = psycopg2.connect(dbname = 'df2e1d8jhmevc9',
                                user = 'piksaffkzecohz',
                                password = '0cc85e0b4a6047656b5d995f637929a5a7c03d277d1ddc6253b354211a9b4150',
                                host = 'ec2-54-91-223-99.compute-1.amazonaws.com',
                                port = '5432')
    return db


st.header("SAT results panel")
conn = conn_db()
temp = psql.read_sql("""select name, email, affiliation, hs_score, erc_score, comfort_score, total_score from public.sat_results""", conn)
conn.close()
st.table(temp)
buffer = io.BytesIO()


st.header("Short overview of results")
st.write("Number of responses: " + str(len(temp)))
st.write("Average HS score: " + str(temp['hs_score'].mean()))
st.write("Average ERC score: " + str(temp['erc_score'].mean()))
st.write("Average Comfort score: " + str(temp['comfort_score'].mean()))
st.write("Average total score: " + str(temp['total_score'].mean()))


with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    temp.to_excel(writer, sheet_name='Sheet1')
    writer.save()

    st.download_button(
            label="Download SAT results",
            data=buffer,
            file_name="sat_results "+ dt.datetime.now().strftime("%Y-%m-%d") +".xlsx",
            mime="application/vnd.ms-excel"
            )





    
