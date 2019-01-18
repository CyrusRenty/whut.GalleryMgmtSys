<template>
    <div class="image-info clear">
      <tslg_head/>
      <div class="warp clear">
        <div class="nav" v-if="imageInfo.cates">
          <a @click="goMain">首页</a> - <a @click="goSearch(1)">{{imageInfo.cates[0]}}</a> - <a @click="goSearch(2)">{{imageInfo.cates[1]}}</a><a v-if="imageInfo.cates[2]" @click="goSearch(3)">{{' - '+imageInfo.cates[2]}}</a><span> - 当前作品</span></div>
        <div class="top">
          <div class="t-left">
            <div><span class="name">{{imageInfo.name}}</span><span class="time">{{imageInfo.add_time}}</span></div>
            <span class="cates" v-if="imageInfo.cates">{{setCates(imageInfo.cates)}}</span>
          </div>
          <div class="t-right">
            <div class="data1">
              <img src="../assets/icon/download_empty.png"><span>{{imageInfo.download_nums}}</span>
              <img src="../assets/icon/like_empty.png"><span>{{imageInfo.like_nums}}</span>
              <img src="../assets/icon/collect_empty.png"><span>{{imageInfo.collection_nums}}</span>
            </div>
            <a class="download-a"><img src="../assets/download.svg" @click="setDownload(imageInfo.id)"><span>下载</span></a>
          </div>
        </div>
        <div class="middle clear">
          <div class="left">
          <img :src="imageInfo.image" class="image" >
          <div class="bot-btn">
            <div @click="setLike(imageInfo)" :class="{active_btn:imageInfo.if_like}">
              <img :src="imageInfo.if_like?ii_liked:ii_like">
              <span v-if="!imageInfo.if_like">点赞</span><span v-if="imageInfo.if_like">已点赞</span></div>
            <div @click="showCollect(imageInfo.id)" :class="{active_btn:imageInfo.if_collect}">
              <img :src="imageInfo.if_collect?ii_collected:ii_collect">
              <span v-if="!imageInfo.if_collect">收藏</span><span v-if="imageInfo.if_collect">已收藏</span></div>
          </div>
          <image_comment/>
        </div>
          <div class="right" ref="right">
            <div class="data2">
              <div class="image-type-wrap"><img :src="cateImage" class="image-type-img"></div>
              <div class="ul-warp">
                <ul class="data2-">
                  <li>格式</li>
                  <li>尺寸</li>
                  <li>体积</li>
                  <li>版权</li>
                </ul>
                <ul class="data2-">
                  <li>{{imageInfo.pattern}}</li>
                  <li>{{imageInfo.width}}*{{imageInfo.height}}</li>
                  <li>{{imageInfo.size}}</li>
                  <li>@{{userInfo.username}}</li>
                </ul>
              </div>
            </div>
            <div class="user-info">
              <i class="user-icon" :title="'进入'+userInfo.username+'的主页'" :style="{'background-image':'url(' + userInfo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }"  @click="getInOtherUser(userInfo.id)"></i>
              <div class="user-name">{{userInfo.username}}</div>
              <div  @click="setFollow(userInfo.id)">
                <div class="unFollow follow" v-if="!imageInfo.if_follow" title="关注">+关注</div>
                <div class="followed follow" v-if="imageInfo.if_follow" title="取消关注">已关注</div>
              </div>
            </div>
            <div class="image-desc">
              <div>图片简介</div>
              <div>{{imageInfo.desc}}</div>
            </div>
          </div>
        </div>
      </div>
      <h3>相关推荐</h3>
      <recommend :image_list="imageInfo.recommend"/>
      <tslg_footer/>
    </div>
</template>

<script>
  import {setFollow, setUnFollow, download} from "../api/action";
  import image_comment from '../components/image_comment'
  import tslg_head from '../components/body/tslg_header'
  import tslg_footer from '../components/body/tslg_footer'
  import recommend from  '../components/card/image_card'
  import { getInOtherUser, setLike, showCollect} from "../utils/user";
  import cookie from "../utils/cookie";
  import {getAllTitle} from "../api/get";
    export default {
        name: "lgts_image_info",
      components:{
          tslg_head,
        tslg_footer,
        image_comment,
        recommend
      },
      data(){
          return{
            ii_like:require('../assets/icon/like_black.png'),
            ii_liked:require('../assets/icon/like_gray.png'),
            ii_collected:require('../assets/icon/collect_gray.png'),
            ii_collect:require('../assets/icon/collect_black.png'),
            like:require('../assets/image_like.png'),
            unlike:require('../assets/image_unlike.png'),
            collect:require('../assets/image_collect.png'),
            unCollect:require('../assets/image_unCollect.png'),
            classify:{},
            cate_index:[],
            cate_string:[]
          }
      },
      created(){
        getAllTitle().then((res)=>{
          this.classify=res.data
        })
        this.$store.commit('SET_COMMENT_NEXT_PAGE',`image=${this.$store.state.imageGroup.image_id}&page=1`)
      },
      computed:{
        imageInfo(){
          return this.$store.state.imageGroup.imageInfo
        },
        userInfo(){
          return this.$store.state.imageGroup.image_userInfo
        },
        cateImage(){
          switch(this.imageInfo.pattern){
            case 'psd':
              return require('../assets/PS.png')
            case 'jpg':
              return require('../assets/JPG.png')
            case 'jpeg':
              return require('../assets/JPG.png')
            case 'png':
              return require('../assets/PNG.png')
          }
        },
      },
      mounted(){
      },
      methods:{
        setLike(item){
         setLike(item)
        },
        showCollect(id){
          showCollect(id)
            // this.$store.commit('SET_COLLECT_LIST',id);
            // this.$store.commit('SET_COLLECT_SHOW');
            // document.body.style.overflow='hidden';
        },
        setFollow(id){
          let data=new FormData();
          data.append('follow',id)
          data.append('fan',this.$store.state.user.userInfo.id)
          if(!this.imageInfo.if_follow){
            setFollow(data).then((res)=>{
              this.imageInfo.if_follow=res.data.id
            })
          }else{
            setUnFollow(this.imageInfo.if_follow).then(()=>{
              this.imageInfo.if_follow=false
            })
          }
        },
        getInOtherUser(id){
          getInOtherUser(id)
        },
        setDownload(id) {
          let data=new FormData
          data.append('image',id)
          download(data).then((res)=>{})
        },
        setCates(cates){
          return cates[cates.length-1]
        },
        goMain(){
          this.$router.push({name:'main'})
        },
        goSearch(index){
          let classify=this.classify,cates_index=[]
          for (let i=0;i<classify.length;i++){
            if(classify[i].name===this.imageInfo.cates[0]){
              cates_index.push(i)
              break
            }
          }
          if(index===1){
            this.goCates(this.imageInfo.cates[0],cates_index)
          }else {
            let kids1=this.classify[cates_index[0]].kids
            for(let i=0;i<kids1.length;i++){
              if(kids1[i].name===this.imageInfo.cates[1]){
                cates_index.push(i)
                break
              }
            }
            if(index===2){
              this.goCates(this.imageInfo.cates[1],cates_index)
            }else{
              let kids2=this.classify[cates_index[1]].kids
              for(let i=0;i<kids2.length;i++){
                if(kids2[i].name===this.imageInfo.cates[2]){
                  cates_index.push(i)
                  break
                }
              }
              this.goCates(this.imageInfo.cates[2],cates_index)
            }
          }
        },
        goCates(item,index){
          const {href}=this.$router.resolve({
            path:'/tslg/cates',
            query:{
              cate:item,
              index:index
            }
          })
          window.open(href,'_blank')
        }
      },
    }
</script>

<style lang="scss" scoped>
  @import "../styles/variables";
  .image-info{
    background: $bg;
  }
  .warp{
    width: 108rem;
    margin: 4.125rem auto 5rem;
    background: #fff;
  }
  .nav{
    text-align: left;
    background: $bg;
    font-size: 1.125rem;
    padding-bottom: .75rem;
    a{
      &:hover{
        color: $normal;
      }
    }
    span{
      color: $f-light;
    }
  }
  .top{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 7.375rem;
    background: #fff;
    border-bottom:0.0625rem solid #e9e9e9;
  }
  .top >.t-left{
    display: flex;
    flex-direction: column;
    text-align: left;
    padding-left: 3rem;
    .name{
      display: inline-block;
      margin-top: 1.5rem;
      padding-right: 1.5rem;
      font-size: 1.875rem;
      font-weight: 600;
    }
    .cates{
      display: inline-block;
      font-size: $ss;
      margin: .75rem 0 1.5rem 0;
      color: $f-light;
    }
    .time{
      color: $f-light;
      font-size: $xsx;
    }
  }
  .top >.t-right{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-right: 3rem;
    .download-a{
      display: flex;
      height: 3rem;
      width: 15rem;
      margin-left: 3rem;
      background: $normal;
      border-radius: 3rem;
      font-size: 1.1rem;
      color: #4a4a4a;
      justify-content: center;
      align-items: center;
      font-weight: 600;
      img{
        height: 1.4rem;
        margin-right: 0.3rem;
      }
      &:hover{
        background: $hover;
      }
    }
    .data1{
      display: flex;
      align-items: center;
      height: 1.5rem;
      font-size: $ms;
      img{
        width:1.2rem;
        height: 1.2rem;
      }
      span{
        margin-left: 0.25rem;
        margin-right: 1rem;
      }
    }
  }
  .left{
    width:80.25rem;
    float: left;
    background: #fff;
    .image{
      width: 100%;
      display: block;
    }
    .bot-btn{
      padding: 2.25rem 0;
      border-right: 0.0625rem solid #e9e9e9;
      border-bottom:0.0625rem solid #e9e9e9;
      display: flex;
      justify-content: center;
      div{
        width:7.5rem;
        height:3rem;
        background: $normal;
        border-radius:3rem;
        color:$f-deep;
        font-size:1.1rem;
        font-weight:600;
        display:flex;
        justify-content:center;
        align-items:center;
        cursor:pointer;
        margin-right: 1rem;
        &:hover{
          background: $hover;
        }
        img{
          width: 1.5rem;
        }
        span{
          line-height:3rem;
        }
      }
    }
  }
  .active_btn{
    background:#fff3bc !important;
    border:#e9e9e9 0.0625rem solid;
    color:#9b9b9b !important;
  }
  .right{
    display: inline-block;
    padding: 0 1.5rem;
    width: 27.75rem;
    float: left;
    background: #fff;
    .data2{
      padding-bottom:3rem ;
      border-bottom: 0.0625rem solid #e9e9e9;
    }
  }

  /*.data1{*/
    /*border-bottom: 0.0625rem solid #e9e9e9;*/
  /*}*/
  .user-info{
    border-bottom: 0.0625rem solid #e9e9e9;
    display: flex;
    align-items: center;
    flex-direction: column;
    height: 17rem;
  }
  .user-icon{
    margin-top: 3rem;
    width: 6rem;
    height: 6rem;
    cursor: pointer;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
  }
  .user-name{
    font-size:1.1rem;
    margin-top: 0.8rem;
    margin-bottom: 1.5rem;
  }
  .data1{
    text-align: left;
  }
  .works-name-wrap{
    margin-top: 2rem;
    display: flex;
    justify-content: space-between;
    margin-bottom: 1.5rem;
  }
  .works-name{
    font-size: 1.5rem;
  }
  .add-time{
    color: #9c9c9c;
    font-size: 1rem;
    line-height: 2rem;
  }
  .works-cate{
   font-size: 1.1rem;
   margin-bottom: 1.5rem;
 }
  .image-type-wrap{
    display: flex;
    justify-content: center;
    margin-top: 3rem;
    margin-bottom:1.875rem ;
  }
  .image-type-img{
    width: 4.5rem;
    height: 4.5rem;
  }
  .ul-warp{
    display: flex;
    justify-content: space-around;
    padding:0 6rem;
  }
  .data2-{
    text-align: left;
    line-height: 1.4rem;
  }

  .-btn{
    height: 3rem;
  }
  .share img{
    width: 14.5%;
  }
  .share-{
    margin: 0 20%;
  }
  .image-desc{
    margin-bottom: 2rem;
  }
  .image-desc div:nth-child(1){
    text-align: left;
    font-size: 1.2rem;
    margin-bottom: 0.7rem;
    font-weight: 600;
  }
  .image-desc div:nth-child(2){
    width: 100%;
    font-size: 1.1rem;
    line-height: 1.5rem;
    letter-spacing: 0.1rem;
    word-wrap: break-word;
    text-align: left;
  }

  h3{
    margin-left: 5rem;
    text-align: left;
  }
</style>
