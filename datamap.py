from re import T
from altair.vegalite.v4.api import value
import streamlit as st
import pandas as pd
import altair as alt

from urllib.error import URLError

@st.cache()
def get_UNS_data():
    df = pd.read_csv("produksi_minyak_mentah.csv")
    return df.set_index("kode_negara")
def get_name_data():
    dfj = pd.read_json("kode_negara_lengkap.json")
    return dfj.set_index("name")
def get_df():
    df = pd.read_csv("produksi_minyak_mentah.csv")
    return df
def get_dfj():
    dfj = pd.read_json("kode_negara_lengkap.json")
    return dfj
try:
    df = get_UNS_data()
    dfj = get_name_data()
    dfn = get_df()
    dfn_s = get_df()
    dfjn = get_dfj()
    st.header("Produksi Minyak Mentah Suatu Negara")
    countries = st.selectbox(
        "Silahkan Pilih Negara", list(dfj.index)
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        datas = dfj.loc[countries]
        try:
            data = df.loc[datas['alpha-3']] 
            chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="tahun:T",
                y=alt.Y("produksi:Q"),
            )
            )
            st.altair_chart(chart, use_container_width=True)
        except KeyError as v:
            st.error('Data Tidak di temukan')  
    tahun = df['tahun'].drop_duplicates()
    st.header("Produksi Minyak Terbesar")
    pilih_tahun = st.selectbox(
        "Silahkan Pilih Tahun", list(tahun)
    )
    besar = st.number_input('Silahkan Input Besar Negara',value=0)
    if besar != 0 :
        dff = df[(df['tahun'] == pilih_tahun)]
        dff.sort_values(by=['produksi'],inplace=True,ascending=False)
        result = dff.head(besar)
        besar = str(besar)
        pilih_tahun = str(pilih_tahun)
        st.header("Data " + besar + " besar pada tahun " + pilih_tahun)
        st.bar_chart(result)
    st.header("Produksi Minyak Terbesar Sepanjang Masa")
    terbesar = st.number_input('Silahkan Input Besar Negara',value=0,key='abc') 
    if terbesar != 0:
        dfn = dfn.groupby(['kode_negara']).agg({'produksi': 'sum'})
        dfn.sort_values(by=['produksi'],inplace=True,ascending=False)
        results = dfn.head(terbesar)
        terbesar = str(terbesar)
        st.header("Data " + terbesar + " besar sepanjang Tahun")
        st.bar_chart(results)
    st.header("Informasi Detail")
    countries1 = st.selectbox(
        "Silahkan Pilih Negara", list(dfj.index),key="abc"
    )
    datas1 = dfj.loc[countries1]
    kode = datas1['alpha-3']
    try:
        dff_b = dfn_s[(dfn_s['kode_negara'] == datas1['alpha-3'])]
        dff_b.sort_values(by=['produksi'],inplace=True,ascending=False)
        dff_k = dfn_s[(dfn_s['kode_negara'] == datas1['alpha-3'])]
        dff_k.sort_values(by=['produksi'],inplace=True)
        dfn_s = dfn_s.groupby(['kode_negara']).agg({'produksi': 'sum'})
        dfn_s.sort_values(by=['kode_negara'],inplace=True)
        total = dfn_s.loc[kode]
        t_hasil_b = dff_b.head(1)
        t_hasil_k = dff_k.head(1)
        t_hasil_ck = dff_k.head(1)
        ck = t_hasil_ck['produksi']
        t_hasil_b = t_hasil_b['tahun']
        t_hasil_k = t_hasil_k['tahun']
        hasil_akhir_b = t_hasil_b.values[0]
        cek_angka = ck.values[0]
        hasil_akhir_b = str(hasil_akhir_b)
        hasil_akhir_k = t_hasil_k.values[0]
        hasil_akhir_k = str(hasil_akhir_k)
        total = total.values[0]
        total = str(total)
        st.write("Nama Lengkap Negara : " + datas1.name)
        st.write("Kode Negara : " + datas1['alpha-3'])
        st.write("Region Negara : " + datas1.region)
        st.write("Sub-Region Negara : " + datas1['sub-region'])
        if cek_angka == 0:
           st.write("Tahun Tidak Memproduksi : " + hasil_akhir_k)
           st.write("Total Produksi : " + total)
        else: 
            st.write("Tahun Produksi Terkecil : " + hasil_akhir_k)
            st.write("Tahun Produksi Terbesar : " + hasil_akhir_b)
            st.write("Total Produksi : " + total)
    except IndexError as I:
        st.write("Nama Lengkap Negara : " + datas1.name)
        st.write("Kode Negara : " + datas1['alpha-3'])
        st.write("Region Negara : " + datas1.region)
        st.write("Sub-Region Negara : " + datas1['sub-region'])
    except KeyError as K:
        st.write("Nama Lengkap Negara : " + datas1.name)
        st.write("Kode Negara : " + datas1['alpha-3'])
        st.write("Region Negara : " + datas1.region)
        st.write("Sub-Region Negara : " + datas1['sub-region'])
except URLError as e:
    st.error("Koneksi Internet di butuhkan")