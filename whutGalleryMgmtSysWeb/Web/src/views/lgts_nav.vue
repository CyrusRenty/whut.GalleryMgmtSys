<template>
  <div class="nav-wrap">
    <ul class="item-wrap">
      <li :class="{nav1_active:nIndex===index1,nav_item:true}" v-for="(item,index1) in nav_items" :key="index1" @mouseleave="mouseOutNav1(item)" @mouseenter="mouseInNav1(item,index1)" >
        <a  contenteditable="false" class="nav1-a" ref="title">{{item.text}}</a>
        <ul class="second-nav" v-if="item.isShow">
          <li v-for="(second_item,index2) in item.second_nav" :class="{nav2_item:true,nav2_active:mIndex===index2}" :key="index2" @mouseenter="mouseInSecond(index2)" @click="getTypeImage(second_item.text,index1,index2)"><a class="">{{second_item.text}}</a></li>
        </ul>
      </li>
    </ul>

    <div class="navR-wrap" >
      <div :class="{nav1_active:on_right_nav,left_nav:true}" @mouseleave="mouseOutNavR" @mouseenter="mouseInNavR"><a class="nav1-a active" ref="titleL">{{title}}</a>
        <ul v-if="on_right_nav" class="navR_item" >
          <li  v-for="(item,index) in sort_items" :key="index" :class="{nav2_item:true,nav2_active:rIndex===index}" @mouseenter="mouseInNavRItem(index)" @click="getOrderImage(item)">
            <a>{{item}}</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "lgts_nav",
    data:function () {
      return {
        nav_items:[
          {text:'菁菁校园',isShow:false,second_nav:[{text:'菁菁校园',id:1},{text:'校园风景',id:4},{text:'校园活动',id:5},{text:'学子风采',id:6}]},
          {text:'摄影艺术',isShow:false,second_nav:[{text:'摄影艺术',id:2},{text:'生活',id:2},{text:'风景',id:3},{text:'人物',id:1}]},
          {text:'办公创意',isShow:false,second_nav:[{text:'办公创意',id:3},{text:'PPT',id:7},{text:'简历',id:8}]},
          {text:'平面设计',isShow:false,second_nav:[{text:'平面设计',id:4},{text:'PS',id:9},{text:'手绘',id:10},{text:'合成',id:11}]}
        ],
        sort_items:['最新上传','最早上传','点赞最多','收藏最多'],
        nIndex:-1,
        mIndex:-1,
        rIndex:-1,
        on_right_nav:false,
        title:'最新上传',
        last_active:-1,
        now_active:0
      }
    },
    methods:{
      mouseInNav1(item,index) {
        this.nIndex=index;
        item.isShow=true
      },
      mouseOutNav1(item){
        item.isShow=!item.isShow;
        this.nIndex=-1;
        this.mIndex=-1
      },
      mouseInSecond(index){
        this.mIndex=index
      },
      mouseInNavR(){
        this.on_right_nav=!this.on_right_nav
      },
      mouseInNavRItem(index){
        this.rIndex=index
      },
      mouseOutNavR(){
        this.rIndex=-1;
        this.on_right_nav=false;
      },
      getTypeImage(data,index,index2){
        this.$store.commit('SET_SEARCH_CONTEXT','')
        if(this.last_active!==-1&&this.last_active!==index){
          this.nav_items[this.last_active].text=this.nav_items[this.last_active].second_nav[0].text;
          this.$refs.title[this.last_active].style.color='#4a4a4a'
        }
        this.$refs.titleL.style.color='#4a4a4a';
        this.title=this.sort_items[0];
        this.nav_items[index].text=this.nav_items[index].second_nav[index2].text;
        this.$refs.title[index].style.color='#9ad3e2';
        this.last_active=index;
        let id=this.nav_items[index].second_nav[index2].id
        // console.log(id);
        this.$store.commit('SET_CONTINUE',true);
        this.$store.commit('SET_STATUS','special');
        if(index2===0)
          this.$store.commit('SET_NEXT_SEARCH',`/big_group/${id}/?page=1`);
        else this.$store.commit('SET_NEXT_SEARCH',`/group/${id}/?page=1`);
        this.$store.commit('SET_IMAGEGROUP');
        this.$store.dispatch('setImageGroupT').then(()=>{
          if(!this.$store.state.imageGroup.image.length)
            this.$store.commit('SET_NO_RESULT',true)
          else this.$store.commit('SET_NO_RESULT',false)
        })
      },
      getOrderImage(data){
        this.$store.commit('SET_SEARCH_CONTEXT','');
        let last_active=this.last_active;
        if(last_active!==-1){
          this.nav_items[last_active].text=this.nav_items[last_active].second_nav[0].text;
          this.$refs.title[last_active].style.color='#4a4a4a'
        }
        this.$refs.titleL.style.color='#9ad3e2';
        this.$store.commit('SET_STATUS','normal');
        this.$store.commit('SET_CONTINUE',true);
        this.title=data;
        let type;
        switch(data){
          case '最新上传':{
            type='add_time';
            break
          }
          case '最早上传':{
            type='-add_time';
            break
          }
          case '点赞最多':{
            type='like_nums';
            break
          }
          case '收藏最多':{
            type='collection_nums';
            break
          }
        }
        this.$store.commit('SET_STATUS','normal');
        this.$store.commit('SET_MAIN_NEXT_PAGE',`ordering=${type}&page=1`);
        this.$store.commit('SET_IMAGEGROUP');
        this.$store.dispatch('setImageGroupI').then(()=>{
          if(!this.$store.state.imageGroup.image.length)
            this.$store.commit('SET_NO_RESULT',true)
          else this.$store.commit('SET_NO_RESULT',false)
        }
        )
      }
    },
  }
</script>

<style scoped>

  a{
    height: 100%;
    display: block;
    font-size: 1.375rem;
    color: #4a4a4a;
    cursor:pointer
  }
  .nav-wrap{
    display: flex;
    width: 100%;
    justify-content: center;
    padding: 0 6rem;
    height: 5rem;
    background: #fff;
  }
  ul{
    padding:0;
    margin: 0;
  }
  .item-wrap{
    width: 42rem;
    display: flex;
    height: 100%;
  }
  .nav1_active a{
    color:#9ad3e2;
  }
  .nav_item{
    line-height: 5rem;
    width: 25%;
    display: flex;
    flex-direction: column;
    position: relative;
    height: 100%;
  }
  .nav1-a:after{
    display: inline-block;
    content: '';
    background: url(../assets/pull_down.png);
    margin: 0.1rem 0 0 0.2rem;
    height: 0.6rem;
    width: 1rem;
    -webkit-background-size: 100% 100%;
    background-size: 100% 100%;
  }

  .second-nav{
    width: 100%;
    flex-direction: column;
    position: absolute;
    z-index: 11;
    top: 5rem;
    background-color: white;
  }
  .nav2_item{
    margin: 0 -1px;
    height: 5rem;
    background:white;
    line-height: 5rem;
    border-bottom: 1px solid #e9e9e9;
  }
  .nav2_item a{
    color: black;
  }
  .nav2_active a{
    color: #5bc3dc;
  }
  .navR-wrap{
    position: absolute;
    right: 6rem;
    display: flex;
    justify-content: flex-end;
  }
  .navR-wrap .active{
    color:#9ad3e2;
  }
  .left_nav{  /* 1 */
    width: 10.5rem;
    height: 100%;
    font-size: 1.375rem;
    line-height: 5rem;
    margin-left:-1px;
  }
  .navR_item{
    width: 100%;
    position: relative;
    z-index: 11;
  }
  @media screen and (max-width:700px  ){
    .nav-wrap{
      display: none;
    }
    .navR-wrap{
      position: relative;
      width: 20%;
      right: 0;
    }
  }
</style>
