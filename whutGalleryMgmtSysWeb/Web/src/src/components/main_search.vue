<template>
  <div>
    <div class="search" ref="search">
      <div class="classify" @mouseenter="showClassifyCard" @mouseleave="unShowClassifyCard"><i></i>分类
        <ul ref="classify_card">
          <li v-for="(item,index) in classify" @click="setSearch(item.name)">{{item.name}}</li>
        </ul>
      </div>
      <input id="search" type="text" placeholder="请输入关键字查询"  @keyup.enter="startSearch" v-model="search_content" ref="search_input" autocomplete="none"/>
      <label for="search" class="label" @click="startSearch"></label>
    </div>
    <div class="search-top" ref="search" v-if="set_top">
      <div class="classify" @mouseenter="showClassifyCard1" @mouseleave="unShowClassifyCard1"><i></i>分类
        <ul ref="classify_card1">
          <li v-for="item in classify" @click="setSearch(item.name)">{{item.name}}</li>
        </ul>
      </div>
      <input id="search1" type="text" placeholder="请输入关键字查询"  @keyup.enter="startSearch" v-model="search_content"/>
      <label for="search1" class="label" @click="startSearch"></label>
    </div>
  </div>

</template>

<script>
    export default {
        name: "main_search",
      data(){
          return {
            search_content:'',
            set_top:false
          }
      },
      computed:{
        classify(){
          return this.$store.state.imageGroup.title
        }
      },
      mounted(){
         window.addEventListener('scroll',this.setSearchTop)
      },
      methods:{
        showClassifyCard1(){
          this.$refs.classify_card1.style.display='block'
        },
        unShowClassifyCard1(){
          this.$refs.classify_card1.style.display='none'
        },
        showClassifyCard(){
          this.$refs.classify_card.style.display='block'
        },
        unShowClassifyCard(){
          this.$refs.classify_card.style.display='none'
        },
        startSearch(){
          if(!this.search_content){
            this.$refs.search_input.style.border='0.0625rem solid #ff0000'
            return
          }else this.$refs.search_input.style.border='0.0625rem solid #cecece'
          const {href}=this.$router.resolve({
              name:'search_result',
            params:{search_content:this.search_content}
          })
          window.open(href,'_blank')
        },
        setSearch(text){
          this.search_content=text;
        },
        setSearchTop(){
          if(document.documentElement.scrollTop>160)
           this.set_top=true
          else
           this.set_top=false
        }
      }
    }
</script>

<style scoped>
  .search{
    height: 3.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin: 1.5rem 0;
  }
  .search-top{
    height: 5rem;
    padding: 0.75rem 0;
    background: #fff;
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 2;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .classify{
    height: 100%;
    width: 6rem;
    background: #eaeaea;
    position: relative;
    font-size: 1.25rem;
    padding:0 1rem;
    line-height: 2.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  .classify i{
    display: inline-block;
    height: 1.25rem;
    width: 1.125rem;
    background: url(../assets/sort.png) no-repeat center;
    background-size: 100% 100%;
    margin-right: 0.25rem;
  }
  .classify ul{
    display: none;
    z-index: 2;
    position: absolute;
    top: 3.5rem;
    left: 0;
    font-size: 1.25rem;
    background: #fff;
    width:7.5rem;
    height: 12rem;
    box-shadow:0 0 4px #9B9B9B ;
  }
  .classify li{
    height: 3rem;
    line-height: 3rem;
  }
  .classify li:hover{
    color: #9ad3e2;
  }
  #search,#search1{
    font-size: 1.25rem;
    height: 100%;
    border: 0.0625rem solid #cecece;
    width: 40.5625rem;
    text-indent: 1.5rem;
    background: #fff;
  }
  .label{
    width: 6rem;
    height: 100%;
    background:url(../assets/search_white.png) no-repeat center #9dd4e3;
    background-size:37.5%;
    cursor: pointer;
  }
</style>
