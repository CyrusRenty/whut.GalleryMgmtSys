<template>
    <div id="main-image" v-if="nav_items.length">
      <div v-for="(item,index) in nav_items" class="main-item-box" >
        <div class="title-wrap">
           <a @click="goBCates(item.name,index)">{{item.name}}</a><a v-for="(item_title,title_index) in item.kids" @click="goSCates(item_title.name,index,title_index)">{{item_title.name}}</a>
          <a class="more" @click="goBCates(item.name,index)">更多 ></a>
        </div>
        <div class="main-image clear" >
          <div v-for="(item_image,image_index) in item.image" class="image-box image-item" >
            <div class="image-content" :style="{'background-image':`url(${item_image.image})`}">
              <div class="image-up" @click="showImageInfo(item_image.id)">
                <div class="btn-warp clear">
                  <div class="collect-btn" :class="{'btn-active':item_image.if_collect}" @click.stop="showCollect(item_image)" title="收藏">
                    <img class="btn-img" :src="item_image.if_collect?collect:unCollect">
                    <span class="btn-span">{{item_image.collection_nums}}</span>
                  </div>
                  <div class="like-btn" :class="{'btn-active':item_image.if_like}" @click.stop="setLike(item_image.id,index,image_index)" title="点赞">
                    <img class="btn-img"  :src="item_image.if_like?like:unlike">
                    <span class="btn-span">{{item_image.like_nums}}</span>
                  </div>
                </div>
                <a  class="download-warp"  :href="item_image.image.split('.400x300')[0]" @click.stop="setDownload(item_image.id)" :download="item_image.name" title="点击下载">
                  <img  class="download-img" src="../assets/download.svg">
                  <span class="download-span">下载</span>
                </a>
              </div>
            </div>
            <div class="photo-info">
              <div class="works">
                <div class="works-name">{{item_image.name}}</div>
                <div class="works-type">{{item_image.cates}}</div>
              </div>
              <div class="author">
                <i class="user-image" :style="{'background-image':`url(${item_image.user.image})`}" @click="getInOtherUser(item_image.user.id)" @mouseenter="showPersonCard(index*10+image_index)" @mouseleave="showPersonCard" :title="'进入'+item_image.user.username+'的主页'"></i>
                <div class="author-name">{{item_image.user.username}}</div>
                <div  @click="setFollow(item_image)"><div class="unFollow follow" v-if="!item_image.if_follow" title="关注">+关注</div><div class="followed follow" v-if="item_image.if_follow" title="取消关注">已关注</div></div>
              </div>
            </div>
            <div class="author-detail" v-if="show_person_card===index*10+image_index">
              <div class="author-big-pic" :style="{'background-image':`url(${item_image.user.image})`}">
              </div>
              <span class="person-card-name">{{item_image.user.username}}</span>
              <div class="products-and-fans">
                <div class="nums-info author-products">
                  <span class="nums-info-title">作品</span>
                  <span class="author-nums">{{item_image.user.upload_nums}}</span>
                </div>
                <div class="nums-info author-fans">
                  <span class="nums-info-title">粉丝</span>
                  <span class="author-nums">{{item_image.user.fan_nums}}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  import {setTitle} from "../utils/user";
  import {setFollow, setLike, setUnFollow, setUnLike} from "../api/action";
  import {getInOtherUser, setDownload, setImageInfo} from "../utils/user";
  import {getTitle, getTypeImage} from "../api/get";
    export default {
        name: "main_image",
      data(){
          return {
            //nav_items:[],
            image_items:[],
            like:require('../assets/image_like.png'),
            unlike:require('../assets/image_unlike.png'),
            collect:require('../assets/image_collect.png'),
            unCollect:require('../assets/image_unCollect.png'),
            show_person_card:-1
          }
      },
      computed:{
          nav_items(){
            return this.$store.state.imageGroup.title
          },
      },
      created(){
      },
      mounted(){
      },
      methods:{
        setLike(id,index,image_index){
          let item=this.nav_items[index].image[image_index]
          let data=new FormData();
          data.append('image',id)
          data.append('user',this.$store.state.user.userInfo.id)
          if(!item.if_like){
            setLike(data).then((res)=>{
              item.if_like=res.data.id
              item.like_nums++
            }).catch((error)=>{
              console.log(error)
            })
          }else{
            setUnLike(item.if_like).then(()=>{
              item.if_like=false
              item.like_nums--
            })
          }
        },
        showCollect(item){
          //设置操作图片的id
          this.$store.commit('SET_IMAGE_ID',item.id);
          this.$store.commit('SET_COLLECT_ITEM',item)
          this.$store.commit('SET_COLLECT_LIST',item.id);
          this.$store.commit('SET_COLLECT_SHOW');
          document.body.style.overflow='hidden';
        },
        setDownload(id){
          setDownload(id)
        },
        showImageInfo(id){
          setImageInfo(id)
        },
        showPersonCard(index){
          this.show_person_card=index
        },
        setFollow(item){
          let data=new FormData();
          data.append('follow',item.user.id)
          data.append('fan',this.$store.state.user.userInfo.id)
          if(!item.if_follow){
            setFollow(data).then((res)=>{
               this.actionFollow(item.user.id,res.data.id)
            })
          }else{
            setUnFollow(item.if_follow).then(()=>{
               this.actionFollow(item.user.id,false)
            })
          }
        },
        actionFollow(id1,id2){
          let length=this.nav_items.length
          for(let i=0;i<length;i++){
            let length=this.nav_items[i].image.length
            let image=this.nav_items[i].image
            for(let j=0;j<length;j++){
              if(image[j].user.id===id1)
                image[j].if_follow=id2
            }
          }
        },
        getInOtherUser(id){
          getInOtherUser(id)
        },
        goSCates(item,index,index1){
          let s_index=[index,index1]
          console.log(s_index)
          let cate={
            cate:item,
            index:s_index
          }
          console.log(cate)
          const {href}=this.$router.resolve({
           path:'cates',
            query:{
              cate:item,
              index:s_index
            }
          })
          window.open(href,'_blank')
        },
        goBCates(item,index){
          let s_index=[index]
          console.log(s_index)
          const {href}=this.$router.resolve({
            path:'cates',
            query:{
              cate:item,
              index:s_index
            }
          })
          window.open(href,'_blank')
        }
      }
    }
</script>

<style lang="scss" scoped>
  @import "../styles/variables";
  #main-image{
    width: 111rem;
    margin: 3.75rem auto 5rem;
    background: $bg;
    min-height: 80rem;
  }
  .main-item-box{
    text-align: left;
    height: 35.32rem;
    margin-bottom: 3.75rem;
    background: $bg;
  }
  .title-wrap{
    margin-left: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .title-wrap a{
    margin-right: 3rem;
    font-size: 1.25rem;
    color: #9b9b9b;
    cursor: pointer;
    &:hover{
      color: $normal;
    }
  }
  .title-wrap a:nth-child(1){
    font-weight: 600;
    font-size: 1.5rem;
    color: #4a4a4a;
  }
  .title-wrap{
    .more{
      float: right;
      margin-right: 1.5rem;
      display: flex;
      align-items: center;
      /*<!--&:after{-->*/
        /*<!--content: '';-->*/
        /*<!--background: url(../assets/pull_down.png);-->*/
        /*<!--background-size: 100% 100%;-->*/
        /*<!--width: 1rem;-->*/
        /*<!--height: .5rem;-->*/
        /*<!-- -webkit-transform: rotate(-90deg);-->*/
        /*<!--transform: rotate(-90deg);-->*/
        /*<!--display: inline-block;-->*/
        /*<!--margin-left: .2rem;-->*/
        /*<!--margin-top: .1rem;-->*/
      /*<!--}-->*/
    }
  }
  .image-box{
    background: #fefefe;
    width:24.75rem;
    height: 32.32rem;
    float: left ;
    margin: 0 1.5rem;
    box-shadow:0 0 4px #9B9B9B ;
  }
  .image-content{
    width: 100%;
    height: 18.54rem;
    background: no-repeat center;
    background-size: cover;
    position: relative;
  }
  .image-content .image-up{
    width: 100%;
    height: 100%;
    position: absolute;
    z-index: 1;
    background: rgba(0,0,0,.6);
    opacity: 0;
    cursor: pointer;
    &:hover{
      opacity: 1;
    }
  }
  .image-name{
    font-size: 1.25rem;
    padding: .9rem 1.5rem;
  }
   .btn-warp{
    position:absolute;
    display: inline-block;
    z-index:3;
    top: 1.68rem;
    right: 1.375rem;
  }
   .btn-span{
    padding-left: 0.3215rem;
    float: right;
  }
   .download-span{
     font-size: $xsx;
     font-weight: 600;
     font-family: 'HiraginoSansGB';
  }
  .user-image,.author-big-pic{
    background: no-repeat center;
    -webkit-background-size: cover;
    background-size: cover;
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
