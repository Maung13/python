from re import T
from altair.vegalite.v4.api import value
from numpy import number
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

def get_dftb_n():
    dftb_n = pd.read_json("kode_negara_lengkap.json")
    return dftb_n.set_index("alpha-3")
try:
    df = get_UNS_data()
    dfj = get_name_data()
    dfn = get_df()
    dfn_s = get_df()
    dfjn = get_dfj()
    dftb = get_df()
    dftb_n = get_dftb_n()
    dftk = get_df()
    dftk_n = get_dftb_n()
    dftn = get_df()
    dftn_n = get_dftb_n()
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
        result = result.produksi
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

    st.header("Informasi Produk Terbesar")
    p_tahun = st.selectbox(
        "Silahkan Pilih Tahun", list(tahun),key = "p_tahun"
    )
    if p_tahun != 0:
        dftb = dftb[(dftb['tahun'] == p_tahun)]
        dftb.sort_values(by=['produksi'],inplace=True,ascending=False)
        result_dftb = dftb.head(1)
        angka = result_dftb['produksi']
        angkas = angka.values[0]
        angkas = str(angkas)
        kode_negara_dftb = result_dftb.kode_negara
        kode_negara_dftb = kode_negara_dftb.values[0]
        kode_negara_dftb = str(kode_negara_dftb)
        dftb_n = dftb_n.loc[kode_negara_dftb]
        st.write("Nama Lengkap Negara : " + dftb_n.name)
        st.write("Kode Negara : " + kode_negara_dftb)
        st.write("Region Negara : " + dftb_n.region)
        st.write("Sub-Region Negara : " + dftb_n['sub-region'])
        st.write("Produksi :" + angkas) 
    st.header("Informasi Produk Terkecil")
    p_tahun_k = st.selectbox(
        "Silahkan Pilih Tahun", list(tahun),key = "p_tahun_k"
    )
    if p_tahun_k != 0:
        dftk = dftk[(dftk['tahun'] == p_tahun_k)]
        dftk = dftk[(dftk['produksi'] != 0)]
        dftk.sort_values(by=['produksi'],inplace=True,ascending=True)
        result_dftk = dftk.head(1)
        angkak = result_dftk['produksi']
        angkaks = angkak.values[0]
        angkaks = str(angkaks)
        kode_negara_dftk = result_dftk.kode_negara
        kode_negara_dftk = kode_negara_dftk.values[0]
        kode_negara_dftk = str(kode_negara_dftk)
        dftk_n = dftk_n.loc[kode_negara_dftk]
        st.write("Nama Lengkap Negara : " + dftk_n.name)
        st.write("Kode Negara : " + kode_negara_dftk)
        st.write("Region Negara : " + dftk_n.region)
        st.write("Sub-Region Negara : " + dftk_n['sub-region'])
        st.write("Produksi :" + angkaks)
    st.header("Informasi Produksi Nol") 
    p_tahun_n = st.selectbox(
        "Silahkan Pilih Tahun", list(tahun),key = "p_tahun_n"
    )
    if p_tahun_n != 0:
        dftn = dftn[(dftn['tahun'] == p_tahun_n)]
        dftn = dftn[(dftn['produksi']== 0)]
        a = dftn.reset_index(drop=True)  
        number_of_rows = len(a)
        number_of_rows = str(number_of_rows)
        st.write("Banyak Negara : " + number_of_rows)
        dftn_n = dftn_n.loc[dftn['kode_negara']]
        c = dftn_n.drop(columns=['alpha-2','iso_3166-2','intermediate-region','region-code','sub-region-code','intermediate-region-code'])
        b = c.reset_index(drop=True)
        st.write(b)
    st.header("Informasi Detail")
    countries1 = st.selectbox(
        "Silahkan Pilih Negara", list(dfj.index),key="country"
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