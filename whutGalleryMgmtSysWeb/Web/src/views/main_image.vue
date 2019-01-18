<template>
    <div id="main-image">
      <div v-for="(item,index) in nav_items" class="main-item-box" >
        <div class="title-wrap">
           <a @click="goBCates(item.name,index)">{{item.name}}</a><a v-for="(item_title,title_index) in item.kids" @click="goSCates(item_title.name,index,title_index)">{{item_title.name}}</a>
          <a class="more" @click="goBCates(item.name,index)">更多 ></a>
        </div>
      <!--<image_card :image_list="item.image"/>-->
        <div class="main-image clear" >
          <div v-for="(item_image,image_index) in item.image" class="image-box image-item" >
            <div class="image-content" :style="{'background-image':`url(${item_image.image})`}">
              <div class="image-up" @click="showImageInfo(item_image.id)">
                <div class="btn-warp clear">
                  <div class="collect-btn" :class="{'btn-active':item_image.if_collect}" @click.stop="showCollect(item_image)" title="收藏">
                    <img class="btn-img" :src="item_image.if_collect?collect:unCollect">
                    <span class="btn-span">{{item_image.collection_nums}}</span>
                  </div>
                  <div class="like-btn" :class="{'btn-active':item_image.if_like}" @click.stop="setLike(item_image)" title="点赞">
                    <img class="btn-img"  :src="item_image.if_like?like:unlike">
                    <span class="btn-span">{{item_image.like_nums}}</span>
                  </div>
                </div>
                <a  class="download-warp"  @click.stop="setDownload(item_image)" :download="item_image.name" title="点击下载">
                  <img  class="download-img" src="../assets/download.svg">
                  <span class="download-span">下载</span>
                </a>
              </div>
            </div>
            <div class="photo-info">
              <div class="works">
                <div class="works-name">{{item_image.name}}</div>
                <div class="works-type">{{setCates(item_image.cates)}}</div>
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
      <collect ref="collect_list"/>
    </div>
</template>

<script>
  import {checkLogin, setLike, showCollect} from "../utils/user";
  import {setFollow, setUnFollow, setUnLike} from "../api/action";
  import {getInOtherUser, setDownload, setImageInfo} from "../utils/user";
  import image_card from '../components/card/image_card'
  import collect from '../components/card/collect'
  import {getMainImage, getTitle, getTypeImage} from "../api/get";
    export default {
        name: "main_image",
      components:{
          image_card,
        collect
      },
      data(){
          return {
            nav_items:[],
            image_items:[],
            like:require('../assets/image_like.png'),
            unlike:require('../assets/image_unlike.png'),
            collect:require('../assets/image_collect.png'),
            unCollect:require('../assets/image_unCollect.png'),
            show_person_card:-1,
          }
      },
      created(){
        let array=this.nav_items;
        getTitle().then((res)=>{
          array=res.data;
          for(let i=0;i<res.data.length;i++){
            array[i].image=[]
            getMainImage(`group/${array[i].id}/?page=1&num=4`).then((res)=>{
              array[i].image=res.data.results
            })
          }
          this.nav_items=array
          // store.commit('SET_TITLE',array)
        })
      },
      mounted(){
      },
      methods:{
        setLike(item){
         setLike(item)
        },
        showCollect(item){
          if(checkLogin())
          this.$refs.collect_list.showCollect(item)
        },
        setDownload(id){
          if(checkLogin())
          setDownload(id)
        },
        showImageInfo(id){
          setImageInfo(id)
        },
        showPersonCard(index){
          this.show_person_card=index
        },
        setFollow(item){
          if(checkLogin()){
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
          this.goCates(item,s_index)
        },
        goBCates(item,index){
          let s_index=[index]
          this.goCates(item,s_index)
        },
        goCates(item,index){
          const {href}=this.$router.resolve({
            path:'cates',
            query:{
              cate:item,
              index:index
            }
          })
          window.open(href,'_blank')
        },
        setCates(cates){
          let array=cates.split("、"),l_cate=[];
          for(let i=0;i<array.length;i++){
            let temp=array[i].split("/");
            l_cate.push(temp[temp.length-1])
          }
          cates=l_cate.join(" ");
          return cates
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
    background: no-repeat top;
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
