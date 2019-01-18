<template>
    <transition name="fade">
      <div v-if="show_hint" class="hint-box" @click="clearAll">
        <div class="hint-content">{{title}}</div>
      </div>

    </transition>
</template>

<script>
    export default {
        name: "hint",
      props:{
        duration:{
         default:2500
        }
        },
      data(){
          return{
            show_hint:false,
            title:''
          }
      },
      methods:{
          showHint(title){
            this.show_hint=true;
            this.title=title;
            setTimeout(()=>{
              this.show_hint=false
            },this.duration)
          },
        clearAll(){
            this.show_hint=false
        }
      }
    }
</script>

<style lang="scss" scoped>
  @import "../styles/variables";
  .hint-box{
    position: fixed;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: 2;
  }
  .hint-content{
    margin: 4rem auto 0;
    max-width: 30rem;
    min-height: 8rem;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: .5rem;
    -webkit-box-shadow: 0 0 1px #9b9b9b;
    -moz-box-shadow: 0 0 1px #9b9b9b;
    box-shadow: 0 4px 8px rgba(0,0,0,.15);
    color: $f-deep;
    background: $normal;
    font-size: 1.5rem;
    padding: 1rem 1.6rem;
  }
  .fade-enter-active,.fade-leave-active{
    -webkit-transition: opacity .5s;
    -moz-transition: opacity .5s;
    -o-transition: opacity .5s;
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0
  }
</style>
