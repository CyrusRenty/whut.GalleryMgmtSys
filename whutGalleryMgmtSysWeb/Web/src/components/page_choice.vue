<template>
  <div class="choice-page" v-if="page_nums>1">
    <div class="cell" @click="choicePage(cur_page-1)"><i class="right"></i></div>
    <div class="cell" v-if="show_first" @click="choicePage(1)">1</div>
    <div class="cell" v-if="show_first">...</div>
    <div v-for="(item,index) in page" v-if="index<6&&item<=page_nums" class="cell" @click="choicePage(item)" :class="{'active_page':item===cur_page}" ref="pages">{{item}}</div>
    <div class="cell" v-if="show_last">...</div>
    <div class="cell" v-if="show_last" @click="choicePage(page_nums)">{{page_nums}}</div>
    <div class="cell" @click="choicePage(cur_page+1)"><i class="left"></i></div>
  </div>
</template>

<script>
    export default {
        name: "page_choice",
      props:['page_nums'],
      data(){
          return {
            cur_page:1,
            show_first:false,
            show_last:false,
            page:[1,2,3,4,5,6],
          }
      },
      computed:{
        // page_num(){
        //   return Math.ceil(this.$store.state.imageGroup.search_count/8)
        // }
      },
      methods:{
        choicePage(item){
          if(item<=0||item>this.page_num)
            return
          this.$emit('cur_page',item)
          this.cur_page=item
          document.documentElement.scrollTop=0
          if(this.page_num>7){
            let page_num=this.page_num
            if(item===1){
              this.page=[1,2,3,4,5,6]
              this.show_first=false
            }
            if(item>=6){
              if((page_num-item)>2){
                this.show_first=true
                this.page=[item-2,item-1,item,item+1,item+2]
                this.show_last=true
              }else{
                this.show_last=false
              }
            }
            if(item===page_num){
              this.page=[page_num-5,page_num-4,page_num-3,page_num-2,page_num-1,page_num]
              this.show_last=false
            }
          }
        }
      }
    }
</script>

<style lang="scss" scoped>
  @import "../styles/variables";
  .choice-page{
    height:3rem;
    display:flex;
    justify-content:center;
    margin-bottom:5rem;
  }
  .cell{
    width:3rem;
    height:3rem;
    border:0.0625rem solid #cecece;
    background:#fff;
    font-size:1.5rem;
    margin:0 .375rem;
    cursor:pointer;
    color: #9b9b9b;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .cell:active{
    background:$normal;
  }
  .active{
    color:$normal;
  }
  .active_page{
    background:$normal;
    color:#4a4a4a;
  }
  .choice-page i{
    display:block;
    width: 1.25rem;
    height: 1.25rem;
    -webkit-background-size:100% 100%;
    background-size: 100% 100%;
    background: url(../assets/right_arrow.png) no-repeat center;
  }
  .right{
    transform: rotate(180deg);
    margin-left: .3rem;
  }
  .left{
    margin-right: .3rem;;
  }

</style>
