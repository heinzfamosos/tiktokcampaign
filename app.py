import streamlit as st
# Import pandas to load the analytics
import pandas as pd 
import json

from tiktok import  get_data

dict_data_campaign = []

#Input
hashtag = st.text_input('Escribe el hashtag de tu campaña', value = "")

#Boton
if st.button('Buscar'):
    print(hashtag)
    dict_test = get_data(hashtag)
    if 'itemList' not in dict_test:
        st.write(f'No se encontraron publicaciones con el hashtag {hashtag}')
    else:
        dict_videos = dict_test['itemList']
        dict_authors = dict_test['userList']
        for k in dict_videos:
            stats = dict_videos[k]['stats']
            authorStats = dict_videos[k]['authorStats']
            dict_data= {
                'tiktok_video_id' : k,
                'video_digg_count':stats['diggCount'],
                'video_share_count':stats['shareCount'],
                'video_comment_count':stats['commentCount'],
                'video_play_count':stats['playCount'],
                'author_username':dict_videos[k]['author'],
                'author_following_count': authorStats['followingCount'],
                'author_follower_count': authorStats['followerCount'],
                'author_heart_count': authorStats['heartCount']
            }

            dict_data_campaign.append(dict_data)

        df = pd.DataFrame(dict_data_campaign)
        df['engagement'] = df['video_digg_count'] + df['video_comment_count'] + df['video_share_count'] + df['video_play_count']
        df['engagement_rate'] = df['engagement'] / df['author_follower_count']
        st.title('Resultados de la campaña')
        campaign_engagement = df['video_play_count'].sum() + df['video_share_count'].sum() +df['video_comment_count'].sum() + df['video_digg_count'].sum()
        campaign_engagement_rate =  "{:.2f}".format(campaign_engagement / df['author_follower_count'].sum()*100)
        met2, met3, met4, met5 = st.columns(4)
        met1, met6, met7, met8 = st.columns(4)
        met2.metric('Views',"{:,}".format(df['video_play_count'].sum()))
        met3.metric('Comments',"{:,}".format(df['video_comment_count'].sum()))
        met4.metric('Shares',"{:,}".format(df['video_share_count'].sum()))
        met5.metric('Likes',"{:,}".format(df['video_digg_count'].sum()))
        met1.metric('Tiktokers', "{:,}".format(df['author_username'].nunique()))
        met6.metric('Followers', "{:,}".format(df['author_follower_count'].sum()))
        met7.metric('Engagement', "{:,}".format(campaign_engagement))
        met8.metric('Engagement Rate', campaign_engagement_rate + '%')
        st.title('Las publicaciones')
        count = 0
        colv1, colv2, colv3, colv4 = st.columns(4)
        colv5, colv6, colv7, colv8 = st.columns(4)
        colv9, colv10, colv11, colv12 = st.columns(4)
        colv13, colv14, colv15, colv16 = st.columns(4)
        for k in dict_videos:
            stats = dict_videos[k]['stats']
            authorStats = dict_videos[k]['authorStats']
            videoInfo = dict_videos[k]['video']
            engagement = stats['shareCount'] + stats['commentCount'] + stats['diggCount'] + stats['playCount']
            engagement_rate =  "{:.2f}".format(engagement / authorStats['followerCount']*100)
            count = count + 1
            if count == 1:
                with colv1:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 2:
                with colv2:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 3:
                with colv3:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 4:
                with colv4:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 5:
                with colv5:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 6:
                with colv6:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 7:
                with colv7:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 8:
                with colv8:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 9:
                with colv9:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 10:
                with colv10:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 11:
                with colv11:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 12:
                with colv12:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 13:
                with colv13:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 14:
                with colv14:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 15:
                with colv15:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')
            if count == 16:
                with colv16:
                    st.video(videoInfo['playAddr'])
                    st.write('por @' + dict_videos[k]['author'])
                    st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                    st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                    st.write('▶️ ' + "{:,}".format(stats['playCount']))
                    st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                    st.write('ER ' +engagement_rate + '%')


                    
                    

        st.title('Los TikTokers')
        count = 0
        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8 = st.columns(4)
        col9, col10, col11, col12 = st.columns(4)
        for j in dict_authors:
            count = count + 1
            if count == 1:
                with col1:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 2:
                with col2:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 3:
                with col3:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 4:
                with col4:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 5:
                with col5:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 6:
                with col6:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 7:
                with col7:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 8:
                with col8:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 9:
                with col9:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 10:
                with col10:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 11:
                with col11:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
            if count == 12:
                with col12:
                    st.write(dict_authors[j]['nickname'])
                    st.image(dict_authors[j]['avatarMedium'])
                    st.write('por @' + j)
        


