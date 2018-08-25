<template>
    <div class="confirm" v-if="show_confirm">
      <div class="content-block">
        <div class="title-content">{{title.title}}</div>
        <div class="sc-btn">
          <input type="button" class="cancel" value="取消" @click="cancelConfirm"/>
          <input type="button" class="submit" value="确认" @click="confirm() "/>
        </div>
      </div>
    </div>
</template>

<script>
    import {deleteFolder} from "../api/action";

    export default {
        name: "confirm_box",
      props:['title'],
      data(){
          return {
            show_confirm:false
          }
      },
      methods:{
        cancelConfirm(){
          this.show_confirm=false
          document.body.style.overflow='auto'
        },
        showConfirm(){
          this.show_confirm=true
          document.body.style.overflow='hidden'
        },
        confirm(){
          console.log('delete')
          console.log(this.title)
          deleteFolder(this.title.id).then(()=>{
            this.$store.state.user.collect_his.splice(this.title.index,1)
          })
          this.cancelConfirm()
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
