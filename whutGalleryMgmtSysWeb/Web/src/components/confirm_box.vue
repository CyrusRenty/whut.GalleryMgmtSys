<template>
    <div class="confirm" v-if="show_confirm">
      <div class="content-block">
        <div class="title-content">{{title}}</div>
        <div class="sc-btn">
          <input type="button" class="cancel" value="取消" @click="cancelConfirm"/>
          <input type="button" class="submit" value="确认" @click="confirm"/>
        </div>
      </div>
    </div>
</template>

<script>
    import {deleteFolder} from "../api/action";

    export default {
        name: "confirm_box",
      data(){
          return {
            show_confirm:false,
            title:''
          }
      },
      methods:{
        deletePage(){
          this.show_confirm=false;
          document.documentElement.style.overflow='auto'
        },
        showConfirm(str){
          this.show_confirm=true;
          this.title=str;
          document.documentElement.style.overflow='hidden'
        },
        confirm(){
          this.$emit('confirm',true)
          this.deletePage()
        },
        cancelConfirm(){
          this.$emit('confirm',false)
          this.deletePage()
        }
      }
    }
</script>

<style scoped>
  .confirm{
    height: 100%;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    background: rgba(0,0,0,.6);
    z-index: 3;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .content-block{
    width: 30rem;
    height: 10rem;
    background:#fff;
    border-radius: .5rem;
  }
  .title-content{
    width: 100%;
    height: 5rem;
    font-size: 1.4rem;
    line-height: 5rem;
  }
  .sc-btn input{
    height: 2.5rem;
  }
</style>
