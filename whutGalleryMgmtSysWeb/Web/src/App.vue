<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'App',
  mounted(){
    let client_width=document.documentElement.clientWidth*16/1920;
    let font_size=client_width+'px';
    console.log(document.documentElement.clientWidth)
    let scroll_width=this.getScrollWidth()
    let item_width=((document.documentElement.clientWidth-scroll_width)/client_width-21)/4
   // document.getElementsByTagName('html')[0].style.fontSize=font_size;
    console.log(font_size)
  },
  methods:{
     getScrollWidth() {
        var noScroll, scroll, oDiv = document.createElement("DIV");
        oDiv.style.cssText = "position:absolute; top:-1000px; width:100px; height:100px; overflow:hidden;";
        noScroll = document.body.appendChild(oDiv).clientWidth;
        oDiv.style.overflowY = "scroll";
        scroll = oDiv.clientWidth;
        document.body.removeChild(oDiv);
        return noScroll-scroll;
      }
  }
}
</script>

<style>
  *{
    -webkit-tap-highlight-color:rgba(0,0,0,0);
    -webkit-text-size-adjust: none;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }
#app {
  font-family:'MicrosoftYaHeiUI','Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #4a4a4a;
}
  a{
    text-decoration: none;
    color: #4a4a4a;
  }
  input{
    outline: none;
    border: none;
  }
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
  }

  input[type="number"] {
    -moz-appearance: textfield;
  }
  img{
    cursor: pointer;
  }
  textarea{
    font-family: Arial;
    font-weight: 400;
    outline: none;
  }
</style>
