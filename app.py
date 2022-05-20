import streamlit as st
# Import pandas to load the analytics
import pandas as pd 
import json
import datetime
import requests

from utils import coalesce
from tiktok import  get_data, get_username_profile, get_username_posts, get_socialmedia_value, get_socialvalue_cpv, get_socialvalue, post_data, post_data_campaign
from instagram import create_update_task_ig, get_task_update_profile_data_ig, get_profile_data_ig, get_feed_posts_data_ig, create_update_task_location, get_task_update_location_data_ig, get_location_data_ig

dict_data_campaign = []

a = st.sidebar.radio('Selecciona una red social:', ['Tiktok', 'Instagram'])

if a == 'Instagram':

    ig_radio = st.radio('Opciones:', ['SMV', 'Analisis'])
    
    if ig_radio == 'Analisis':
        username = st.text_input('Username que se va a analizar', value = "")
        buscar_btn = st.button('Analizar')
        if buscar_btn:
            sm1,sm2,sm3 = st.columns(3)
            data_resp = get_task_update_profile_data_ig(username)
            search_status = data_resp['data']['status']
            if search_status == 'finished':
                profile_data = get_profile_data_ig(username)
                profile_data = profile_data['data']
                last_location = profile_data['latest_location_id']
                posts_data = get_feed_posts_data_ig(username)
                dict_posts_df = []
                st.title('Instagram Profile')
                col1, col2 = st.columns(2)
                with col1:
                    response = requests.get(profile_data['profile_photo_url_hd'])
                    st.image(response.content)
                    st.write('@' + profile_data['username']) 
                with col2:    
                    st.write('Followers ' + "{:,}".format(profile_data['followers_count']))
                    st.write('Following ' + "{:,}".format(profile_data['followings_count']))
                    st.write('Link in bio ' + coalesce(profile_data['external_url'],''))
                    st.write('Posts ' + "{:,}".format(profile_data['posts_count']))
                    st.metric('Verificado?', profile_data['is_verified'])
                    st.metric('Privado?', profile_data['is_private'])
                
                st.title('Metricas')
                posts_data = posts_data['data']
                posts = posts_data['items']
                for post in posts:
                    dict_post = {
                        'post_id': post['id'],
                        'likes': post['likes_count'],
                        'comments': post['comments_count'],
                        'video_views': post['video_views_count'],
                        'created_time': post['created_time'],
                        'is_video': post['is_video'],
                        'location_id': post['location_id'],
                        'media_url': post['attached_media_display_url']
                    }
                    dict_posts_df.append(dict_post)
                df = pd.DataFrame(dict_posts_df)
                df = df.sort_values(by='created_time', ascending=False)
                df['engagement'] = df['comments'] + df['likes']
                df['engagement_rate'] = df['engagement'] / profile_data['followers_count']
                sm1,sm2,sm3, sm4 = st.columns(4)
                sm1.metric('Posts', df['post_id'].nunique())
                sm1.metric('Avg Comments', "{:,}".format(round(df['comments'].mean(),2)))
                sm1.metric('Avg Likes', "{:,}".format(round(df['likes'].mean(),2 )))
                sm1.metric('Avg Engagement', "{:,}".format(round(df['engagement'].mean(),2)))
                sm1.metric('Avg Engagement Rate', "{:,}".format(round(df['engagement_rate'].mean()*100,2))+'%')
                sm2.metric('Video Posts', df[df['is_video']==True]['post_id'].nunique())
                sm2.metric('Avg Comments Video', "{:,}".format(round(df[df['is_video']==True]['comments'].mean(),2)))
                sm2.metric('Avg Likes Video', "{:,}".format(round(df[df['is_video']==True]['likes'].mean(),2 )))
                sm2.metric('Avg Video View', "{:,}".format(round(df[df['is_video']==True]['video_views'].mean(),2)))
                sm2.metric('Avg Engagement Rate', "{:,}".format(round(df[df['is_video']==True]['engagement'].sum()*100 / df[df['is_video']==True]['video_views'].sum(),2))+'%')
                sm3.metric('Image Posts', df[df['is_video']==False]['post_id'].nunique())
                sm3.metric('Avg Comments Post', "{:,}".format(round(df[df['is_video']==False]['comments'].mean(),2)))
                sm3.metric('Avg Likes Post', "{:,}".format(round(df[df['is_video']==False]['likes'].mean(),2)))
                sm3.metric('Avg Engagement', "{:,}".format(round(df[df['is_video']==False]['engagement'].mean(),2)))
                sm3.metric('Avg Engagement Rate', "{:,}".format(round(df[df['is_video']==False]['engagement_rate'].mean()*100,2))+'%')
                smv = get_socialmedia_value(profile_data['followers_count']*.3,df['likes'].mean(), df['comments'].mean(),0)
                sm4.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))
                sv = get_socialvalue(coalesce(df[df['is_video']==True]['video_views'].mean(),0),df['likes'].mean(), profile_data['followers_count']*.3)
                sm4.metric('Social Media Value  Min CPV','$ ' + "{:,}".format(round(sv['min_val_cpv'],2)))
                sm4.metric('Social Media Value  Min CPL','$ ' + "{:,}".format(round(sv['min_val_cpl'],2)))
                sm4.metric('Social Media Value  Min CPM','$ ' + "{:,}".format(round(sv['min_val_cpm'],2)))
                sm4.metric('Social Media Value  Min','$ ' + "{:,}".format(round(sv['minimum_value'],2)))
                st.title('Publicaciones')
                cp1, cp2, cp3, cp4 = st.columns(4)
                for index, row in df.iterrows():
                    if index < 12:
                        response = requests.get(row['media_url'])
                        if index % 4 == 3:
                            cp1.image(response.content)
                            cp1.write('Fecha publicacion: ' + str(row['created_time']) )
                            cp1.write('Likes: ' + str(row['likes'])  )
                            cp1.write('Comments: ' + str(row['comments']) )
                            cp1.write('Engagement Rate: ' + str(round(row['engagement_rate']*100,2)) + '%')
                            smv = get_socialmedia_value(profile_data['followers_count']*.3,row['likes'], row['comments'],0)
                            cp1.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result'])) 
                        if index % 4 == 2:
                            cp2.image(response.content)
                            cp2.write('Fecha publicacion: ' + str(row['created_time']) )
                            cp2.write('Likes: ' + str(row['likes'])  )
                            cp2.write('Comments: ' + str(row['comments']) )
                            cp2.write('Engagement Rate: ' + str(round(row['engagement_rate']*100,2)) + '%')
                            smv = get_socialmedia_value(profile_data['followers_count']*.3,row['likes'], row['comments'],0)
                            cp2.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))  
                        if index % 4 == 1:
                            cp3.image(response.content)
                            cp3.write('Fecha publicacion: ' + str(row['created_time']) )
                            cp3.write('Likes: ' + str(row['likes'])  )
                            cp3.write('Comments: ' + str(row['comments']) )
                            cp3.write('Engagement Rate: ' + str(round(row['engagement_rate']*100,2)) + '%')
                            smv = get_socialmedia_value(profile_data['followers_count']*.3,row['likes'], row['comments'],0)
                            cp3.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))  
                        if index % 4 == 0:
                            cp4.image(response.content)
                            cp4.write('Fecha publicacion: ' + str(row['created_time']) )
                            cp4.write('Likes: ' + str(row['likes'])  )
                            cp4.write('Comments: ' + str(row['comments']) )
                            cp4.write('Engagement Rate: ' + str(round(row['engagement_rate']*100,2)) + '%')
                            smv = get_socialmedia_value(profile_data['followers_count']*.3,row['likes'], row['comments'],0)
                            cp4.metric('Social Media Value IG','$ ' + "{:,}".format(smv['result']))  
                            

                        

                st.title('Locations')
                if df['location_id'].nunique() > 0:
                    dict_loc_df = []
                    location_list = df[df['location_id'].isna() == False]['location_id'].unique()
                    for location in location_list:
                        loc_data_resp = get_task_update_location_data_ig(location)
                        loc_search_status = loc_data_resp['data']['status']
                        if loc_search_status == 'finished':
                            loc_data = get_location_data_ig(location)
                            loc_data = loc_data['data']
                            dict_loc = {
                                'location_id': loc_data['id'],
                                'lat': loc_data['latitude'],
                                'lon': loc_data['longitude']
                            }
                            dict_loc_df.append(dict_loc)
                        elif loc_search_status == 'unknown':
                            create_update_task_location(location)

                    loc_df = pd.DataFrame(dict_loc_df)
                    st.map(loc_df)
                    st.write(loc_df)    
                   
            elif search_status == 'unknown':
                create_update_task_ig(username)
                st.write(f'Se esta analizando la información de {username}')
            else:
                st.write('La solicitud esta en status ' + search_status)
            
        
        

    if ig_radio == 'SMV':
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

            dict_data_c = {
                'campaign_hashtag':hashtag,
                'tiktokers':int(df['author_username'].nunique()),
                'tiktok_videos': int(df['tiktok_video_id'].nunique()),
                'total_video_plays': df['video_play_count'].sum(),
                'avg_video_plays': df['video_play_count'].mean(),
                'median_video_plays':df['video_play_count'].median(),
                'total_video_comments': df['video_comment_count'].sum(),
                'avg_video_comments': df['video_comment_count'].mean(),
                'median_video_comments':df['video_comment_count'].median(),
                'total_video_shares': df['video_share_count'].sum(),
                'avg_video_shares': df['video_share_count'].mean(),
                'median_video_shares':df['video_share_count'].median(),
                'total_video_likes': df['video_digg_count'].sum(),
                'avg_video_likes': df['video_digg_count'].mean(),
                'median_video_likes':df['video_digg_count'].median(),
                'total_followers':df['author_follower_count'].sum(),
                'avg_followers':df['author_follower_count'].mean(),
                'median_followers':df['author_follower_count'].median(),
                'total_engagement':campaign_engagement,
                'avg_engagement':df['engagement'].mean(),
                'median_engagement': df['engagement'].median(),
                'total_engagement_rate': campaign_engagement_rate,
                'avg_engagement_rate': df['engagement_rate'].mean(),
                'avg_engagement_rate': df['engagement_rate'].mean(),
                'median_engagement_rate': df['engagement_rate'].median(),
                'social_media_value_mv': round(sv['minimum_value'],2),
                'social_media_value':round(smv['result'],2),
                'social_media_value_cpm': round(sv['avg_val_cpm'],2),
                'social_media_value_cpv': round(sv['min_val_cpv'],2),
                'social_media_value_cpl': round(sv['min_val_cpl'],2),
            }
            print(dict_data_c)
            test = post_data_campaign(dict_data_c)

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
        secUid = dict_test['user']['secUid']
        is_verified = dict_test['user']['verified']
        authorStats = dict_test['stats']
        col1, col2 = st.columns(2)
        with col1:
            st.image(dict_test['user']['avatarMedium'])
            st.write('por @' + hashtag) 
            st.write('Followers ' + "{:,}".format(authorStats['followerCount']))
            st.write('❤️ ' + "{:,}".format(authorStats['heart']))
            st.write('videos ' + "{:,}".format(authorStats['videoCount']))
            st.metric('Verificado?', is_verified)
        dict_posts = get_username_posts(secUid)
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
            dict_data = {
                'tiktok_username':hashtag,
                'tiktok_followers':followers,
                'tiktok_videos': authorStats['videoCount'],
                'avg_video_plays': df['video_play_count'].mean(),
                'median_video_plays':df['video_play_count'].median(),
                'avg_engagement':df['engagement'].mean(),
                'median_engagement': df['engagement'].median(),
                'avg_engagement_rate': df['engagement_rate'].mean(),
                'median_engagement_rate': df['engagement_rate'].median(),
                'social_media_value_cpv': round(smcpv['minimum_value'],2),
                'social_media_value':round(smv['result'],2),
                'tiktok_secUid': secUid,
                'is_verified': is_verified
            }
            test = post_data(dict_data)
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

