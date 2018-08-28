<template>
    <div class="rank">
      <tslg_header/>
      <div class="rank-nav">
        <div class="rank-item" v-for="(item,index) in rank_items" >
          <div class="title" @mouseenter="showDownload(index)" @mouseleave="showDownload(-1)" :class="{on:index===on_item}" >{{item.title}}
          <ul v-if="index<2&&index===show_list"><li v-for="(item1,index1) in item.list" @click="setTitle(item1,index)">{{item1}}</li></ul>
          </div><i v-if="index<2"></i>
          </div>
      </div>
    </div>
</template>

<script>
  // <iframe src='https://view.officeapps.live.com/op/view.aspx?src=http%3A%2F%2Fonqow625k.bkt.clouddn.com%2FMySQL%25E7%25B4%25A2%25E5%25BC%2595.pptx' width='100%' height='100%' frameborder='1'>
  // </iframe>
  import tslg_header from '../../components/body/tslg_header'
  import {getRankImage} from "../../api/user";
    export default {
        name: "index",
      components:{
          tslg_header
      },
      data(){
        return {
          rank_items:[{title:'周下载量排行',list:['周下载量排行','月下载量排行','总下载量排行']},
            {title:'周收藏量排行',list:['周收藏量排行','月收藏量排行','总收藏量排行']},
            {title:'总关注量排行'}],
          show_list:-1,
          on_item:0
        }
      },
      methods:{
        showDownload(index){
          this.show_list=index
        },
        setTitle(item,index){
          this.on_item=index
          this.rank_items[index].title=item
          let params=''
          if(index===0){
            params='?ordering=-download_nums'
            switch(item){
              case '周下载量排行':{
                params=params+'&time=week'
                break
              }
              case '月下载量排行':{
                params=params+'&time=month'
                break
              }
              case '总下载量排行':{
                break
              }
            }
          }
          switch(item){
            case '':
          }
          getRankImage()
        }
      }
    }
</script>

<style lang="scss" scoped>
  @import "../../styles/variables";
  .rank{
    min-height: 60rem;
    background: $bg;
  }
  .rank-nav{
    width: 100%;
    height: 4rem;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: $xls;
    background: #fff;
  }
  .rank-item{
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    margin: 0 1.375rem;
    color: $f-light;
    cursor: pointer;
    &:hover{
      color: $f-deep;
    }
  }
  .rank-item >.title{
    height: 100%;
    line-height: 4rem;
  }
  .rank-item >i{
    display: inline-block;
    background: url(../../assets/pull_down.png);
    margin: 0.1rem 0 0 0.5rem;
    height: 0.6rem;
    width: 1rem;
    -webkit-background-size: 100% 100%;
    background-size: 100% 100%;
  }
  .title >ul{
    position: absolute;
    z-index: 2;
    right: .5rem;
    top: 4rem;
    width: 105%;
    color: $f-deep;
    font-size: $ls;
    background: #fff;
    box-shadow: 0 1px 2px $f-light;
    li{
      margin: 0.75rem 0;
      line-height: 2rem;
      &:hover{
        color:$normal;
      }
    }
  }
  .on{
    border-bottom: 0.125rem solid #000;
  }
</style>
