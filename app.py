import streamlit as st
# Import pandas to load the analytics
import pandas as pd 
import json
import datetime 

from tiktok import  get_data, get_username_profile, get_username_posts, get_socialmedia_value, get_socialvalue_cpv, get_socialvalue

dict_data_campaign = []

a = st.sidebar.radio('Selecciona una red social:', ['Tiktok', 'Instagram'])

if a == 'Instagram':
    impressions = st.text_input('Cuantas impresiones?', value = "")
    likes = st.text_input('Cuantos likes?', value = "")
    comments = st.text_input('Cuantos comentarios?', value = "")
    saved_posts = st.text_input('Cuantos saved posts?', value = "")
    calc_btn = st.button('Calcular SMV')
    if calc_btn:
        smv = get_socialmedia_value(impressions,likes,comments,saved_posts)
        sv = get_socialvalue(impressions,likes,impressions)
        sm1,sm2,sm3 = st.columns(3)
        sm4, sm5, sm6 = st.columns(3)
        sm7, sm8, sm9 = st.columns(3)
        sm1.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
        sm2.metric('Social Media Value  Min','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
        sm3.metric('Social Media Value  Max','$ ' + "{:,}".format(sv['maximum_value']))
        sm4.metric('Social Media Value  Max CPV','$ ' + "{:,}".format(sv['max_val_cpv']))
        sm5.metric('Social Media Value  Max CPL','$ ' + "{:,}".format(sv['max_val_cpl']))
        sm6.metric('Social Media Value  Max CPM','$ ' + "{:,}".format(sv['max_val_cpm']))
        sm7.metric('Social Media Value  Min CPV','$ ' + "{:,}".format(sv['min_val_cpv']))
        sm8.metric('Social Media Value  Min CPL','$ ' + "{:,}".format(sv['min_val_cpl']))
        sm9.metric('Social Media Value  Min CPM','$ ' + "{:,}".format(sv['min_val_cpm']))


if a == 'Tiktok':
    #Input
    hashtag = st.text_input('Escribe el hashtag de tu campaña', value = "")

    colb1, colb2, colb3 = st.columns([1,1,1])

    with colb1:
        hashtag_btn = st.button('Buscar Hashtag')
    with colb2:
        username_btn = st.button('Buscar Username')

    #Boton
    if hashtag_btn:
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
            met9, met10, met11= st.columns(3)
            met2.metric('Views',"{:,}".format(df['video_play_count'].sum()))
            met3.metric('Comments',"{:,}".format(df['video_comment_count'].sum()))
            met4.metric('Shares',"{:,}".format(df['video_share_count'].sum()))
            met5.metric('Likes',"{:,}".format(df['video_digg_count'].sum()))
            met1.metric('Tiktokers', "{:,}".format(df['author_username'].nunique()))
            met6.metric('Followers', "{:,}".format(df['author_follower_count'].sum()))
            met7.metric('Engagement', "{:,}".format(campaign_engagement))
            met8.metric('Engagement Rate', campaign_engagement_rate + '%')
            smv = get_socialmedia_value(df['author_follower_count'].sum()*.05,df['video_digg_count'].sum(),df['video_comment_count'].sum(),0)
            sv = get_socialvalue(df['video_play_count'].sum(),df['video_digg_count'].sum(),df['author_follower_count'].sum()*.08)
            met9.metric('Expected Cost CPM','$ ' + "{:,}".format(round(sv['avg_val_cpm'],2)))
            met10.metric('Expected Cost CPV','$ ' + "{:,}".format(round(sv['min_val_cpv'],2)))
            met11.metric('Expected Cost SMV','$ ' + "{:,}".format(round(smv['result'],2)))

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
            
    if username_btn:
        print(hashtag)
        dict_test = get_username_profile(hashtag)
        dict_test = dict_test['userInfo']
        authorStats = dict_test['stats']
        col1, col2 = st.columns(2)
        with col1:
            st.image(dict_test['user']['avatarMedium'])
            st.write('por @' + hashtag) 
            st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
            st.write('❤️ ' + "{:,}".format(authorStats['heart']))
            st.write('videos ' + "{:,}".format(authorStats['videoCount']))
        dict_posts = get_username_posts(dict_test['user']['secUid'])
        dict_videos = dict_posts['itemList']
        for k in dict_videos:
            stats = k['stats']
            authorStats = k['authorStats']
            videoInfo = k['video']
            date = datetime.datetime.fromtimestamp(k['createTime'])
            date_str = date.strftime('%Y-%m-%d %H:%M:%S')
            dict_data= {
                    'tiktok_video_id' : k['video']['id'],
                    'video_digg_count':stats['diggCount'],
                    'video_share_count':stats['shareCount'],
                    'video_comment_count':stats['commentCount'],
                    'video_play_count':stats['playCount'],
                    'author_username':k['author']['uniqueId'],
                    'author_following_count': authorStats['followingCount'],
                    'author_follower_count': authorStats['followerCount'],
                    'author_heart_count': authorStats['heartCount'],
                    'publication_date':date_str
                }

            dict_data_campaign.append(dict_data)
            
        with col2:
            followers = authorStats['followerCount']
            df = pd.DataFrame(dict_data_campaign)
            df['engagement'] = df['video_digg_count'] + df['video_comment_count'] + df['video_share_count'] + df['video_play_count']
            df['engagement_rate'] = df['engagement'] / df['author_follower_count']
            st.metric('Avg Video Plays', "{:,}".format(round(df['video_play_count'].mean(),2)))
            st.metric('Avg Engagement', "{:,}".format(round(df['engagement'].mean(),2)))
            st.metric('Avg Engagement Rate', "{:.2f}".format(df['engagement_rate'].mean()*100) + "%")
            st.metric('Medio Engagement Rate', "{:.2f}".format(df['engagement_rate'].median()*100) + "%")
            if followers > 500000:
                if df['engagement_rate'].median() > 0.15:
                    new_title = f'<p style="font-family:sans-serif; color:Green; font-size: 42px;">ER EXCELENTE</p>'
                elif df['engagement_rate'].median() > 0.10:
                    new_title = f'<p style="font-family:sans-serif; color:Gray; font-size: 42px;">ER PROMEDIO</p>'
                else:
                    new_title = f'<p style="font-family:sans-serif; color:Red; font-size: 42px;">ER MALO</p>'
            else:
                if df['engagement_rate'].median() > 0.20:
                    new_title = f'<p style="font-family:sans-serif; color:Green; font-size: 42px;">ER EXCELENTE</p>'
                elif df['engagement_rate'].median() > 0.15:
                    new_title = f'<p style="font-family:sans-serif; color:Gray; font-size: 42px;">ER PROMEDIO</p>'
                else:
                    new_title = f'<p style="font-family:sans-serif; color:Red; font-size: 42px;">ER MALO</p>'
            st.markdown(new_title, unsafe_allow_html=True)
            smv = get_socialmedia_value(df['author_follower_count'].mean()*.1,df['video_digg_count'].median(),df['video_comment_count'].median(),df['video_share_count'].median())
            st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
            smcpv = get_socialvalue_cpv(df['video_play_count'].median())
            st.metric('Social Media Value CPV Min','$ ' + "{:,}".format(round(smcpv['minimum_value'],2)))
            st.metric('Social Media Value CPV Max','$ ' + "{:,}".format(round(smcpv['maximum_value'],2)))
        st.title('Las últimas publicaciones')
        colv1, colv2, colv3, colv4 = st.columns(4)
        colv5, colv6, colv7, colv8 = st.columns(4)
        colv9, colv10, colv11, colv12 = st.columns(4)
        if 'itemList' not in dict_posts:
            st.write(f'No se encontraron publicaciones con el hashtag {hashtag}')
        else:
            dict_videos = dict_posts['itemList']
            count = 0
            for k in dict_videos:
                stats = k['stats']
                authorStats = k['authorStats']
                videoInfo = k['video']
                date = datetime.datetime.fromtimestamp(k['createTime'])
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                engagement = stats['shareCount'] + stats['commentCount'] + stats['diggCount'] + stats['playCount']
                engagement_rate =  "{:.2f}".format(engagement / authorStats['followerCount']*100)
                count = count + 1
                sv = get_socialvalue(stats['playCount'],stats['diggCount'],authorStats['followerCount']*0.1)
                smv = get_socialmedia_value(authorStats['followerCount']*.2,stats['diggCount'],stats['commentCount'],stats['shareCount'])
                if count == 1:
                    with colv1:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 2:
                    with colv2:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 3:
                    with colv3:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 4:
                    with colv4:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 5:
                    with colv5:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 6:
                    with colv6:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 7:
                    with colv7:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 8:
                    with colv8:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 9:
                    with colv9:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 10:
                    with colv10:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 11:
                    with colv11:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                if count == 12:
                    with colv12:
                        st.video(videoInfo['playAddr'])
                        st.write('Fecha Publicación: ' + date)
                        st.write('por @' + k['author']['uniqueId'])
                        st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
                        st.write('❤️ ' + "{:,}".format(stats['diggCount']))
                        st.write('▶️ ' + "{:,}".format(stats['playCount']))
                        st.write('💬 ' + "{:,}".format(stats['shareCount'] + stats['commentCount']))
                        st.write('ER ' +engagement_rate + '%')
                        st.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                        st.metric('Social Media Value ','$ ' + "{:,}".format(round(sv['minimum_value'],2)))

