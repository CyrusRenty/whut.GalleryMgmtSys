<template>
  <div class="main-image clear width" v-if="photos">
  <div class="image-item " v-for="(photo,index) in photos" :key="index" ref="image_item">
    <div v-if="$router.currentRoute.name==='ranking_list'" :class="{rank:true,first:index+1+(cur_page-1)*8===1,second:index+1+(cur_page-1)*8===2,third:index+1+(cur_page-1)*8===3}">{{index+1+(cur_page-1)*8}}</div>
    <div  class="item-content" :style="{'background-image':'url(' + photo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">
      <div class="info" @click="showImageInfo(photo.id)" title="点击查看详情">
        <div class="btn-warp clear">
          <div class="collect-btn clear" :class="{'btn-active':photo.if_collect}" @click.stop="showCollect(photo.id,index)" title="收藏">
            <img class="btn-img" :src="photo.if_collect?collect:unCollect">
            <span class="btn-span">{{photo.collection_nums}}</span>
          </div>
          <div class="like-btn" :class="{'btn-active':photo.if_like}" @click.stop="setLike(photo.id,index)" title="点赞">
            <img class="btn-img"  :src="photo.if_like?like:unlike">
          <span class="btn-span">{{photo.like_nums}}</span>
          </div>
        </div>
        <a class="download-warp"  :href="photo.image.split('.400x300')[0]" @click.stop="setDownload(photo.id)" :download="photo.name" title="点击下载">
          <img  class="download-img" src="../../assets/download.svg">
          <span class="download-span">下载</span>
        </a>
      </div>
    </div>
    <div class="photo-info">
    <div class="works">
      <div class="works-name">{{photo.name}}</div>
      <div class="works-type">{{photo.cates}}</div>
    </div>
    <div class="author">
      <i class="user-image" :style="{'background-image':'url(' + photo.user.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }" @click="getInOtherUser(photo.user.id)" @mouseenter="showPersonCard(index)" @mouseleave="showPersonCard" :title="'进入'+photo.user.username+'的主页'"></i>
      <div class="author-name floatL">{{photo.user.username}}</div>
      <div  @click="setFollow(photo.user.id,index)"><div class="unFollow follow" v-if="!photo.if_follow" title="关注">+关注</div><div class="followed follow" v-if="photo.if_follow" title="取消关注">已关注</div></div>
    </div>
    </div>
    <div class="author-detail" v-if="show_person_card===index">
      <div class="author-big-pic" :style="{'background-image':'url(' + photo.user.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">
      </div>
      <span class="person-card-name">{{photo.user.username}}</span>
      <div class="products-and-fans">
        <div class="nums-info author-products">
          <span class="nums-info-title">作品</span>
          <span class="author-nums">{{photo.user.upload_nums}}</span>
        </div>
        <div class="nums-info author-fans">
          <span class="nums-info-title">粉丝</span>
          <span class="author-nums">{{photo.user.fan_nums}}</span>
        </div>
      </div>
    </div>
  </div>
    <div v-if="no_result">
      <img src="../../assets/noResult.png" class="no-result-img">
      <p class="no-result-word">没有找到符合条件的结果</p>
    </div>
    <page_choice @cur_page="getCurPage" class="page" :page_nums="page_nums"/>
  </div>
</template>

<script>
  import {setUnLike,setFollow,setUnFollow,download} from "../../api/action";
  import mock from '../../utils/mock'
  import {checkLogin, getInOtherUser, setDownload, setImageInfo} from "../../utils/user";
  import page_choice from '../page_choice'

    export default {
      name: "image_card",
      components:{
        page_choice
      },
      data(){
        return {
          like:require('../../assets/image_like.png'),
          unlike:require('../../assets/image_unlike.png'),
          collect:require('../../assets/image_collect.png'),
          unCollect:require('../../assets/image_unCollect.png'),
          show_person_card:-1,
          sw:true,
          no_more:false,
          cur_page:1
        }
      },
      computed:{
        photos(){
          return this.$store.getters.image
        },
        no_result(){
          return this.$store.state.imageGroup.no_result
        },
        page_nums(){
          return Math.ceil(this.$store.state.imageGroup.search_count/16)
        }
       },
      methods:{
        setLike(id,index){
          if(checkLogin()){
            let data=new FormData();
            data.append('image',id)
            data.append('user',this.$store.state.user.userInfo.id)
            if(!this.photos[index].if_like){
              setLike(data).then((res)=>{
                this.photos[index].if_like=res.data.id
                this.photos[index].like_nums++
              }).catch((error)=>{
                console.log(error)
              })
            }else{
              setUnLike(this.photos[index].if_like).then(()=>{
                this.photos[index].if_like=false
                this.photos[index].like_nums--
              })
            }
          }
        },
        showCollect(id,index){
          if(checkLogin()) {
            this.$store.commit('SET_IMAGE_ID', id);
            this.$store.commit('SET_INDEX', index)
            this.$store.commit('SET_COLLECT_LIST', id);
            this.$store.commit('SET_COLLECT_SHOW');
            document.body.style.overflow = 'hidden';
          }
        },
        setFollow(id,index){
          if(checkLogin()) {
            let data = new FormData();
            data.append('follow', id)
            data.append('fan', this.$store.state.user.userInfo.id)
            if (!this.photos[index].if_follow) {
              setFollow(data).then((res) => {
                this.photos[index].if_follow = res.data.id
                this.photos.forEach((item) => {
                  if (item.user.id === id)
                    item.if_follow = res.data.id
                })
              })
            } else {
              setUnFollow(this.photos[index].if_follow).then(() => {
                this.photos[index].if_follow = false
                this.photos.forEach((item) => {
                  if (item.user.id === id)
                    item.if_follow = false
                })
              })
            }
          }
          },
        showImageInfo(id) {
          setImageInfo(id)
        },
        setDownload(id) {
          if(checkLogin())
         setDownload(id)
        },
        getInOtherUser(id){
          getInOtherUser(id)
        },
        showPersonCard(index){
          this.show_person_card=index
        },
        getCurPage(item){
          this.cur_page=item
          this.$emit('cur_page',item)
        }
        },
    }
</script>

<style lang="scss" scoped>
  .main-image{
    position: relative;
    padding-top: 3rem;
    margin: 0 auto 5rem;
    height: 153.2rem;
  }
  .floatL{
    float: left;
  }
  .search_context{
    width: 100%;
    text-align: left;
    font-size: 1.3rem;
    margin: 1rem 0;
    margin-left: 1.5rem;
    font-weight: bold;
  }
  .page{
    position: absolute;
    bottom: -5rem;
    margin-bottom: 5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }
  .rank{
    position: absolute;
    left: 0.75rem;
    top: 0;
    width: 2rem;
    height: 2rem;
    background: #4a4a4a;
    color: #fff;
    line-height: 2rem;
    font-size: 1.1rem;
    z-index: 2;
    &:after{
      content: '';
      position: absolute;
      top: 2rem;
      left: 0;
      border: solid ;
      border-width: .5rem 1rem;
      border-color: #4a4a4a transparent transparent;
    }
  }
  .first{
    background-color: #fb2640;
    &:after{
      border-color: #fb2640 transparent transparent;
    }
  }
  .second{
    background: #f5a623;
    &:after{
      border-color: #f5a623 transparent transparent;
    }
  }
  .third{
    background-color: #ffd100;
    &:after{
      border-color: #ffd100 transparent transparent;
    }
  }


/*
person-card
 */
  .author-detail{
    position: absolute;
    top:0;
    width: 100%;
    height: 27.25rem;
    background: white;
    box-shadow:0.125rem 0.125rem 0.875rem #D6D6D6;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    line-height: 3rem;
    z-index: 2;
    font-size: 1.25rem;
    font-weight: bold;
  }

  .author-detail:before{
    content: "";
    display: block;
    position: absolute;
    border: 0.75rem solid transparent;
    border-top-color: white;
    left: 2.2rem;
    bottom: -1.5rem;
  }

  .author-big-pic{
    display: inline-block;
    width: 10rem;
    height: 10rem;
    border-radius: 10rem;
  }

  .person-card-name{
    font-size: 1.5rem;
  }

  .products-and-fans{
    display: flex;
  }

  .nums-info{
    display: flex;
    flex-direction: column;
    line-height: 2rem;
    padding: 0 3rem 0;
    margin-top: 2rem;
  }

  .author-products{
    border-right: 0.125rem solid #cecece;
  }

  .nums-info-title{
    color: #9b9b9b;
  }

  .author-nums{
    font-weight: bold;
  }

</style>
