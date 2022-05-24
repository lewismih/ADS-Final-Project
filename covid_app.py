# -- Import various libraries required
import requests
import json
import streamlit as st
import pandas as pd
import numpy as np
from st_card_component_2 import card_component
from PIL import Image
import matplotlib.pyplot as plt
import calendar
import seaborn as sns
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

st.set_page_config(page_title='Latest Covid News Kenya', page_icon='📢', layout='wide')


# -- DATA COLLECTION SECTION USING JSON from 2 independent Sources
response = requests.get(
    "https://webhooks.mongodb-stitch.com/api/client/v2.0/app/covid-19-qppza/service/REST-API/incoming_webhook/global?country=Kenya&hide_fields=_id, country, country_code, country_iso2, country_iso3, loc, state, uid'").text
response_info = json.loads(response)

response1 = requests.get("https://api.coronatracker.com/v5/analytics/newcases/country?countryCode=KE&startDate=2020-01-22&endDate=2023-05-21").text
response_info_1 = json.loads(response1)

# ------------- List creation
covid_cases = []
for country_info in response_info:
    covid_cases.append(
        [country_info["confirmed"], country_info["deaths"], country_info["recovered"],
         country_info["confirmed_daily"],
         country_info["deaths_daily"], country_info["recovered_daily"], country_info["date"]])

covid_df = pd.DataFrame(data=covid_cases,
                        columns=["confirmed", "deaths", "recovered", "confirmed_daily", "deaths_daily",
                                 "recovered_daily", "date"])
# --
covid_cases_1 = []
for country_info in response_info_1:
    covid_cases_1.append(
        [country_info["new_recovered"], country_info["last_updated"]])

covid_df_1 = pd.DataFrame(data=covid_cases_1, columns=["new_recovered", "date"])

# ------------- Data Merging from the 2 sources

covid_df_merged = pd.merge(covid_df, covid_df_1, how='inner', on='date')

# ------------- Date Conversion
covid_df_merged["Report_Date"] = pd.to_datetime(pd.to_datetime(covid_df_merged["date"]).dt.date).dt.normalize()



# Hide Hamburger Menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# =============================================

def show_home_page():
    # -- HEADER SECTION
    tit1, tit2, tit3 = st.columns(3)
    with tit2:
        st.markdown("## Track Covid-19 Kenya")

    # -- COMPUTATIONS
    # ------------- Components Section 1
    df_covid_confirmed = covid_df_merged["confirmed"][covid_df_merged.index[-1]]
    df_covid_deaths = covid_df_merged["deaths"][covid_df_merged.index[-1]]
    df_covid_recovered = covid_df_merged["new_recovered"].sum()

    df_covid_date = covid_df_merged["Report_Date"].dt.strftime('%d-%m-%Y')[covid_df_merged.index[-1]]

    df_covid_new_confirmed = (covid_df_merged["confirmed_daily"][covid_df_merged.index[-1]])
    df_covid_new_deaths = (covid_df_merged["deaths_daily"][covid_df_merged.index[-1]])
    df_covid_new_recovered = (covid_df_merged["new_recovered"][covid_df_merged.index[-1]])

    # ------------- Components Section 2
    df_covid_recovery_rate = np.round(((df_covid_recovered / df_covid_confirmed) * 100), decimals=2)
    df_covid_fatality_rate = np.round(((df_covid_deaths / df_covid_confirmed) * 100), decimals=2)

    # ------------- Components Section 3
    df_covid_monthly = \
        covid_df_merged.groupby([covid_df_merged.Report_Date.dt.year, covid_df_merged.Report_Date.dt.month])[
            'confirmed_daily'].mean().unstack(level=0)

    # -- SECTION 1
    st.info(f"Kenya's Covid-19 Report: {df_covid_date}")

    reg1, reg2, reg3 = st.columns(3)
    with reg1:
        card_component(
            title=f"{df_covid_confirmed}",
            subtitle="Total Confirmed Cases",
            body=f"{df_covid_new_confirmed} new cases",
            link="#"
        )
    with reg2:
        card_component(
            title=f"{df_covid_recovered}",
            subtitle="Total Recovered Cases",
            body=f"{df_covid_new_recovered} new recovered",
            link="#"
        )
    with reg3:
        card_component(
            title=f"{df_covid_deaths}",
            subtitle="Total Confirmed Deaths",
            body=f"{df_covid_new_deaths} new fatalities",
            link="#"
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # -- Section 2
    st.markdown("## Mortality Report")

    reg01, reg02, reg03, reg04, reg05 = st.columns([0.95, 0.95, 0.2, 0.95, 0.95])

    with reg01:
        plt.clf()
        pie_1_labels = ['Recovered', 'Active']
        pie_1_values = df_covid_recovered, (df_covid_confirmed - df_covid_recovered)

        series = pd.Series(pie_1_values, index=pie_1_labels, name="")
        series.plot.pie(figsize=(4, 4), autopct='%.2f%%', explode=(0.1, 0), shadow=False,
                        counterclock=True, startangle=90, textprops={'fontsize': 14});
        circle = plt.Circle(xy=(0, 0), radius=.75, facecolor='white')
        plt.gca().add_artist(circle)
        st.pyplot(plt.gcf())

    with reg02:
        st.markdown("<h5 style='text-align: center; color: white;'>Recovery Rate</h5>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: yellow;'> {df_covid_recovery_rate}%</h1>",
                    unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center; color: white;'>of the Total Cases</h6>", unsafe_allow_html=True)

    with reg03:
        st.markdown("&#124;", unsafe_allow_html=True)
        st.markdown("&#124;", unsafe_allow_html=True)
        st.markdown("&#124;", unsafe_allow_html=True)
        st.markdown("&#124;", unsafe_allow_html=True)
        st.markdown("&#124;", unsafe_allow_html=True)
        st.markdown("&#124;", unsafe_allow_html=True)
        st.markdown("&#124;", unsafe_allow_html=True)

    with reg04:
        plt.clf()
        pie_2_labels = ['Deceased', 'Alive']
        pie_2_values = df_covid_deaths, (df_covid_confirmed - df_covid_deaths)

        series = pd.Series(pie_2_values, index=pie_2_labels, name="")
        series.plot.pie(figsize=(4, 4), autopct='%.2f%%', explode=(0.1, 0), shadow=False,
                        counterclock=False, startangle=90, textprops={'fontsize': 14});
        circle = plt.Circle(xy=(0, 0), radius=.75, facecolor='white')
        plt.gca().add_artist(circle)
        st.pyplot(plt.gcf())

    with reg05:
        st.markdown("<h5 style='text-align: center; color: white;'>Fatality Rate</h5>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: yellow;'> {df_covid_fatality_rate}%</h2>",
                    unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: center; color: white;'>of the Total Cases</h6>", unsafe_allow_html=True)

    # -- Mid Section
    image = Image.open("stylings/Home-banner-3.jpg")
    st.image(image, use_column_width="always", width="none")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # -- Section 3
    st.markdown("## Covid Overview in Kenya ")

    with st.container():
        ix = list(range(0, len(df_covid_monthly.columns), 10))
        with sns.axes_style("darkgrid"):
            for i in ix:
                plt.figure(figsize=(12, 4))
                data = df_covid_monthly.iloc[:, i:i + 10]
                sns.lineplot(data=data, markers=True, dashes=False)

                plt.xticks(np.arange(1, 13), calendar.month_name[1:13], rotation=30)
                plt.ylim(0, 1500)
                plt.xlabel('Month')
                plt.ylabel('Confirmed Covid Cases Monthly')
                plt.title(f"Monthly Covid Cases Comparison\n in Kenya since 2020")
                st.pyplot(plt.gcf())

    # ---- ACKNOWLEDGEMENTS ----
    with st.container():
        st.write("---")
        st.write(
            "COVID Data Sources: WHO, JHU CSSE, CDC, ECDC, NHC of the PRC, DXY, QQ, and various international media")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def show_about_page():

    # -- Lottie Animation
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # -- Local CSS Used
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("stylings/style.css")

    # ---- LOAD ASSETS ----
    lottie_coding = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_u8gtxfrn.json")
    lottie_coding_1 = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ekseupwg.json")

    # ---- HEADER SECTION ----
    sect1, sect2 = st.columns(2)

    with sect1:
        st.subheader("Hi, I am Lewis :confetti_ball:")

        # ---- Mid Section ----
        st.title("A Data Analyst From Kenya.")
        st.write(
            "I am a Data Science enthusiast who seeks to help others to make the right data-driven decisions, from data"
            " that is already readily available to them.")
        st.write(
            "I can help translate data into valuable and comprehensible insights effective in business and non "
            "business settings."
        )

    with sect2:
        st_lottie(lottie_coding, height=300, key="coding")

    # ---- CONTACT ----
    with st.container():
        st.write("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("")
        with col2:
            st.header("Get In Touch below...")
        with col3:
            st.write("")

        contact_form = """
        <form action="https://formsubmit.co/lewismih@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
        left_column, right_column = st.columns(2)
        with left_column:
            st_lottie(lottie_coding_1, height=300, key="mailing")
        with right_column:
            st.markdown(contact_form, unsafe_allow_html=True)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

def show_news_page():

    # Lottie Animation
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # ---- LOAD ASSETS ----
    lottie_coding = load_lottieurl("https://assets10.lottiefiles.com/private_files/lf30_48xXx3.json")

    # ---- HEADER SECTION ----
    tit1, tit2, tit3 = st.columns([3, 6, 3])
    with tit2:
        st.markdown("## M.O.H. Kenya - News Feed")

    # ---- News Feeder
    with st.container():
        st.write("---")

    sect1, sect2 = st.columns(2)
    with sect1:
        components.html(
            "<a class=\"twitter-timeline\" data-width=\"1200\" data-height=\"500\" data-theme=\"light\" "
            "href=\"https://twitter.com/MOH_Kenya?ref_src=twsrc%5Etfw\">Tweets by MOH_Kenya</a> <script async "
            "src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>", width=None, height=500)

    with sect2:
        st.markdown("### Be in the Know...")
        st.write(
            "- Stay on top of Kenya latest Covid-19 highlights and developments on the ground with Kenya's - Ministry "
            "of Health facts based updates."
        )
        st.write("- Use the panel on the left to scroll and read present/past updates."
                 )

        st_lottie(lottie_coding, height=300, key="coding")

    st.write("---")


# =================

selected_menu = option_menu(None,
                        ["Home", "News", "About"],
                        icons=['house', 'cloud-upload', "list-task"],
                        menu_icon="cast", default_index=0, orientation="horizontal")

if selected_menu == 'Home':
    show_home_page()
if selected_menu == 'News':
    show_news_page()
if selected_menu == 'About':
    show_about_page()

# ==================================


