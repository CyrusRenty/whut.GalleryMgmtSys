<template>
  <div class="footer clear">
    <div class="footer-left">
      <div v-for="list in lists" class="list">
        <h3>{{list[0].text}}</h3>
        <a v-for="item in list[1]" :href="item.href" class="footer-item">{{item.text}}</a>
      </div>
      <div>
      </div>
      <div class="footer-right"></div>
    </div>

    <div class="footer-right">
      <h3>联系客服</h3>
      <a><i class="icon-phone"></i>400-9987011</a>
      <a><i class=" icon-location"></i>武汉理工大学具体地址具体地址</a>
    </div>
  </div>
</template>

<script>
  export default {
    name: "tslg_footer",
    data(){
      return {
        lists:{
          list1:[{text:'常用链接'},[{text:'校园官方',href:'#'},{text:'教务处',href:'#'},{text:'账号|密码',href:'#'},{text:'版权投诉',href:'#'}]],
          list2:[{text:'关于图库'},[{text:'关于我们',href:'#'},{text:'加入我们',href:'#'},{text:'心系图库',href:'#'},{text:'举办活动',href:'#'}]],
          list3:[{text:'常见问题'},[{text:'成为签约摄影师',href:'#'},{text:'登录注册',href:'#'},{text:'账号|密码',href:'#'},{text:'版权投诉',href:'#'}]],
        },
        contact:['联系客服',['400-9987011','武汉理工大学具体地址具体地址具体地址']]
      }
    },
    computed:{
      items:function () {

      },
    }
  }
</script>

<style lang="scss" scoped>
  $word:#e9e9e9;

  .footer{
    width: 100%;
    background-color:#3d3d42;
    padding: 6.5rem 0;
    a{
      color: $word;
    }
  }
  .footer .footer-left{
    display: inline-block;
    float:left;
    padding-left: 6rem;
  }
  .footer .footer-right{
    display: inline-block;
    float:right;
    padding-right: 11.125rem;
    text-align: left;
  }
  .footer .list{
    box-sizing:border-box;
    float: left;
    padding: 0 8.875rem 0 0;
    text-align: left;
  }
  .footer .footer-item{
    display: block;
    text-decoration: none;
    margin-bottom: 1rem;
  }
  .footer-right a{
    display: flex;
    align-items:center;
    font-size:1.125rem;
    margin-bottom:1rem;
  }
  .footer-right i{
    margin-right:0.5rem;
    width: 1.125rem;
    height: 1.125rem;
    background-size:100% 100%;
    display: inline-block;
  }

  .footer h3{
    font-size: 1.25rem;
    margin: 0;
    padding-top: 0;
    padding-bottom: 2rem;
    color:$word;
  }

  .icon-phone{
    background:url(../../assets/Phone.png);
  }
  .icon-location{
    background:url(../../assets/Location.png) center;
    width:1rem !important;
  }
</style>
