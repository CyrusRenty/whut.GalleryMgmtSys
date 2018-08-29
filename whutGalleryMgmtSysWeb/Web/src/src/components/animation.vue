<template>
    <div class="animation">
      <div class="test">
      </div>
      <div class="test1"></div>
    </div>
</template>

<script>
    export default {
        name: "animation",
      created(){
          document.body.style.overflow='hidden'
      }
    }
</script>

<style scoped>
  .animation{
    position: fixed;
    height: 100%;
    width: 100%;
    background: rgba(0,0,0,.5);
    top: 0;
    left: 0;
    z-index: 1;
  }
  /*.test{*/
    /*animation: first 5s;*/
    /*-webkit-animation: first 5s;*/
    /*-moz-animation: first 5s;*/
    /*width: 10rem;*/
    /*height: 10rem;*/
    /*border-radius: 50%;*/
    /*padding: 2rem;*/
    /*background: #000;*/
  /*}*/
  /*@keyframes first {*/
    /*from{*/
      /*background: #000;*/
      /*-webkit-transform: rotate(0deg);*/
    /*}*/
    /*to{background: #9ad3e2;*/
      /*-webkit-transform: rotate(180deg);*/
    /*}*/
  /*}*/
  .test {
    font-size: 20px;
    margin: 80px 50px;
    float: left;
    width: 1em;
    height: 1em;
    border-radius: 50%;
    position: relative;
    text-indent: -9999em;
    -webkit-animation: load3 1.3s infinite linear;
    animation: load3 1.3s infinite linear;
  }
  @-webkit-keyframes load3 {
    0%,
    100% {
      box-shadow: 0 -3em 0 0.2em #9ad3e2, 2em -2em 0 0 #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 -0.5em #9ad3e2,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 -0.5em #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 0 #9ad3e2;
    }
    12.5% {
      box-shadow: 0 -3em 0 0 #9ad3e2, 2em -2em 0 0.2em #9ad3e2,
      3em 0 0 0 #9ad3e2, 2em 2em 0 -0.5em ,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 -0.5em #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    25% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 0 #9ad3e2,
      3em 0 0 0.2em #9ad3e2, 2em 2em 0 0 #9ad3e2,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 -0.5em #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    37.5% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 0 #9ad3e2, 2em 2em 0 0.2em #9ad3e2,
      0 3em 0 0 #9ad3e2, -2em 2em 0 -0.5em #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    50% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 0 #9ad3e2,
      0 3em 0 0.2em #9ad3e2, -2em 2em 0 0 #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    62.5% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 -0.5em #9ad3e2,
      0 3em 0 0 #9ad3e2, -2em 2em 0 0.2em #9ad3e2,
      -3em 0 0 0 #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    75% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 -0.5em #9ad3e2,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 0 #9ad3e2,
      -3em 0 0 0.2em #9ad3e2, -2em -2em 0 0 #9ad3e2;
    }
    87.5% {
      box-shadow: 0 -3em 0 0 #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 -0.5em #9ad3e2,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 0 #9ad3e2,
      -3em 0 0 0 #9ad3e2, -2em -2em 0 0.2em #9ad3e2;
    }
  }
  @keyframes load3 {
    0%,
    100% {
      box-shadow: 0 -3em 0 0.2em #9ad3e2, 2em -2em 0 0 #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 -0.5em #9ad3e2,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 -0.5em #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 0 #9ad3e2;
    }
    12.5% {
      box-shadow: 0 -3em 0 0 #9ad3e2, 2em -2em 0 0.2em #9ad3e2,
      3em 0 0 0 #9ad3e2, 2em 2em 0 -0.5em ,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 -0.5em #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    25% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 0 #9ad3e2,
      3em 0 0 0.2em #9ad3e2, 2em 2em 0 0 #9ad3e2,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 -0.5em #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    37.5% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 0 #9ad3e2, 2em 2em 0 0.2em #9ad3e2,
      0 3em 0 0 #9ad3e2, -2em 2em 0 -0.5em #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    50% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 0 #9ad3e2,
      0 3em 0 0.2em #9ad3e2, -2em 2em 0 0 #9ad3e2,
      -3em 0 0 -0.5em #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    62.5% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 -0.5em #9ad3e2,
      0 3em 0 0 #9ad3e2, -2em 2em 0 0.2em #9ad3e2,
      -3em 0 0 0 #9ad3e2, -2em -2em 0 -0.5em #9ad3e2;
    }
    75% {
      box-shadow: 0 -3em 0 -0.5em #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 -0.5em #9ad3e2,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 0 #9ad3e2,
      -3em 0 0 0.2em #9ad3e2, -2em -2em 0 0 #9ad3e2;
    }
    87.5% {
      box-shadow: 0 -3em 0 0 #9ad3e2, 2em -2em 0 -0.5em #9ad3e2,
      3em 0 0 -0.5em #9ad3e2, 2em 2em 0 -0.5em #9ad3e2,
      0 3em 0 -0.5em #9ad3e2, -2em 2em 0 0 #9ad3e2,
      -3em 0 0 0 #9ad3e2, -2em -2em 0 0.2em #9ad3e2;
    }
  }
</style>
