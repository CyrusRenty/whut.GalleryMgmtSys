<template>
  <div class="slide-show" @mouseover="clear" @mouseout="run">
    <div class="slide-img">
      <transition-group name="slide-trans">
        <li v-for="(photo,index) in slides" :key="index" v-if="index===nowIndex"><a target="_blank" :href="photo.url"><img :src="photo.image"></a> </li>
      </transition-group>
    </div>
    <span @click="goto(prevIndex)" @mouseover="showArrow('arrow_left')" @mouseleave="hideArrow('arrow_left')" class="slide-btn slide-pre"><i ref="arrow_left" class="arrow-left arrow" ></i></span>
    <span @click="goto(nextIndex)" @mouseover="showArrow('arrow_right')" @mouseleave="hideArrow('arrow_right')" class="slide-btn slide-next"><i ref='arrow_right' class="arrow-right arrow"></i></span>
    <div class="center-box"><div class="relative-box">
      <ul class="slide-pages">
        <li v-for="(item, index) in slides" @click="goto(index)">
          <a :class="{'on':true,'a-st': index === nowIndex}"></a>
          </li>
      </ul>
    </div>
    </div>
  </div>
</template>

<script>
  import {getBanner} from "../api/get";
    export default {
        name: "Lgts_lunbo",
      data:function () {
        return{
          nowIndex:0,
          slides:[],
          isShow: true,
          inv:2000
        }
      },
      created() {
          if(!this.slides.length)
        getBanner().then((res)=>{
          this.slides=[...res.data]
        })
      },
      methods:{
        goto (index) {
          this.isShow = false
          setTimeout(() => {
            this.nowIndex = index
            this.isShow = true
          }, 10)
        },
        run () {
          this.invId = setInterval(() => {
            this.goto(this.nextIndex)
          }, this.inv)
        },
        clear () {
          clearInterval(this.invId)
        },
        showArrow (item) {
          this.$refs[`${item}`].style['display'] = 'inline-block'
        },
        hideArrow (item) {
          this.$refs[`${item}`].style['display'] = 'none'
        }
      },
      mounted:function () {
        this.run();
      },
      computed:{
        prevIndex () {
          if (this.nowIndex === 0) {
            return this.slides.length - 1
          }
          else {
            return this.nowIndex - 1
          }
        },
        nextIndex () {
          if (this.nowIndex === this.slides.length - 1) {
            return 0
          }
          else {
            return this.nowIndex + 1
          }
        }
      }
    }
</script>

<style lang="scss" scoped>
  @import "../styles/variables";
  ul.slide-pages {
    border-radius: 50%;
  }
  ul.slide-pages {
    padding:0;
  }
  .slide-btn{
    cursor: pointer;
    width:3rem;
    height: 100%;
    position: absolute;
    margin: 0 3rem;
    display: flex;
    align-items: center;
  }
  .slide-btn:hover{

  }
  .slide-pre{
    left: 0;
    /*left:calc(0px / 2);*/
    /*top: calc(50% - 100px / 2);*/
  }
  .slide-next{
    right: 0;
    /*right:calc(0px / 2);*/
    /*top: calc(50% - 100px / 2);*/
  }
  .arrow{
    display: none;
    /*display: inline-block;*/
    width:2.5rem;
    height: 3rem;
  }
  .arrow:hover{
    display: inline-block;
  }
  .arrow-left{
    background: url(../assets/Arrow_left.png);
    background-size: cover;
    -webkit-background-size: cover;
  }
  .arrow-right{
    background:url(../assets/Arrow_right.png);
    background-size: cover;
    -webkit-background-size: cover;
  }
  .slide-trans-enter-active,.slide-trans-leave-active {
    transition: opacity 1s;
  }
  .slide-trans-enter,.slide-trans-leave-active {
    opacity: 0;
  }

  .slide-show {
    position: relative;
    width: 100%;
    height: 25rem;
    overflow: hidden;
  }
  @media screen and (max-width: 700px){
    .slide-show{
      height: 20rem;
    }
  }
  .slide-img {
    width: 100%;
  }
  .slide-img img {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
  }
  .center-box{
    position: absolute;
    bottom: 0.625rem;
    left:50%;
  }
  .relative-box{
    position: relative;
  }
  .slide-pages {
    position: relative;
    left:-50%;
  }
  .slide-pages li {
    display: inline-block;
    padding: 0 0.1875rem;
    cursor: pointer;
    color: #fff;
  }
  /*.slide-pages li .on {
    text-decoration: underline;
  }*/
  .on {
    background-color: #4c4c4c;
    width: 0.625rem;
    height: 0.625rem;
    border-radius: 0.625rem;
    display: inline-block;
  }
  .a-st{
    background-color: $normal;
  }
</style>
