<template>
  <div class="search_result">
    <tslg_header/>
    <div class="top-items">
     <div class="cates-choice">
       <div class="position">
         <span >当前位置：</span><span v-if="!position.length" ><span class="all">全部</span><span> > </span></span>
         <span v-for="(item,index) in position"><span class="position-item" ><span>{{item.name}}</span><a @click="deletePosition(index)" title="点击返回">×</a></span><span> > </span></span>
         <span>  {{search_content}}  </span>
         <span class="count">&nbsp;&nbsp;共{{count}}个结果</span>
       </div>
       <div class="classify">
         <span class="first-title">分类：</span><span><a @click="searchAll" ref="all">全部</a>
         <a v-for="(item,index) in cates_" @click="choiceCate(item,index)" ref="title" :class="{'active':index===aIndex}">{{item.name}}</a>
       </span>
       </div>
       <div class="format">
         <span class="first-title">格式：</span>
         <span><span v-for="item in format" class="check-item" >
           <input type="radio" :id="item" name="format" ref="format_radio" @click="choiceFormat(item)"/>
           <label :for="item">{{item}}</label>
         </span></span>
       </div>
     </div>
      <div class="order ">
        <span class="first-title">排序：</span>
        <span><a v-for="(item,index) in order" ref="order" @click="choiceOrder(item,index)">{{item}}</a></span>
        <div class="search">
          <input id="search" type="text" placeholder="请输入关键字查询"  @keyup.enter="startSearch" v-model="search" autocomplete="none"/>
          <label for="search" class="label" @click="startSearch"></label>
        </div>
      </div>
    </div>
    <image_card @cur_page="Page" :image_list="image_list" :page_nums="page_nums"/>
    <tslg_footer/>
  </div>
</template>

<script>
  import tslg_header from '../components/body/tslg_header'
  import tslg_footer from '../components/body/tslg_footer'
  import image_card from '../components/card/image_card'
  import page_choice from '../components/page_choice'
  import {getAllTitle, getTypeImage} from '../api/get'
    export default {
        name: "search_result",
      components:{
          tslg_header,
          tslg_footer,
        image_card,
        page_choice
      },
      data(){
          return {
            cates:[],
            cates_:[],
            kids:[],
            first:true,
            position:[],
            format:['全部','PNG','JPEG','PSD'],
            order:['最新上传','点赞最多','收藏最多'],
            cates_string:'',
            up_cates_string:'',
            search:'',
            aIndex:-1,
            cur_format:'',
            cur_order:'-add_time',
            image_list:[],
            page_nums:0,
            count:0
          }
      },
      computed:{
          search_content(){
            let search_content=this.$router.currentRoute.params.search_content
            if(search_content)
            return search_content
            else return ''
          },
       },
      created(){
        this.getCates()
        if(this.$router.currentRoute.params.search_content){
         this.actionDis(`images/?search=${this.search_content}&page=1`)
        }
      },
      mounted(){
        this.$refs.format_radio[0].checked=true;
        this.$refs.all.style.color='#ffd100';
        this.$refs.order[0].style.color='#ffd100'
      },
      methods:{
          getCates(){
            getAllTitle().then((res)=>{
              this.cates=this.cates_=res.data
              let query=this.$router.currentRoute.query
              if(query.index){
                for(let item of query.index)
                  this.set(this.cates_[item],item)
                this.actionDis(`images/?search=${this.search_content}&cates=${this.cates_string}&ordering=${this.cur_order}&pattern=${this.cur_format}`)
              }

            })
          },
        set(item,index){
          this.cates_string=item.name
          item.index=index
          if(this.position.length){
            if(this.position[this.position.length-1].kids){
              this.position.push(item)
            }else this.position[this.position.length-1]=item
          }else  this.position.push(item)
          if(item.kids){
            this.first=false
            this.cates_=item.kids
            this.up_cates_string=this.cates_string
          }else
            this.setColor(index)
        },
        actionDis(params){
          getTypeImage(params).then((res)=>{
            this.image_list=res.data.results;
            this.count=res.data.count;
            this.page_nums=Math.ceil(res.data.count/16)
          })
          this.cur_page=1
        },
        choiceCate(item,index){
         this.set(item,index);
          this.actionDis(`images/?search=${this.search_content}&cates=${this.cates_string}&ordering=${this.cur_order}&pattern=${this.cur_format}`)
        },
        deletePosition(index){
            let position=this.position;
            if(index===0){
              this.cates_=this.cates;
              this.cates_string=''
            }
            else{
              this.cates_=position[index-1].kids;
              this.cates_string=position[index-1].name
            }
          this.$refs.all.style.color='#ffd100';
          this.aIndex=-1
          this.position.splice(index,position.length-index)
          this.actionDis(`images/?search=${this.search_content}&cates=${this.cates_string}&ordering=${this.cur_order}&pattern=${this.cur_format}`)
        },
        searchAll(){
          this.$refs.all.style.color='#ffd100'
          this.aIndex=-1
          this.deletePosition(this.position.length-1)
        },
        setColor(index){
          this.$refs.all.style.color='#4a4a4a';
          this.aIndex=parseInt(index)
        },
        choiceFormat(item){
          if(item==="全部")
            item = ''
          this.cur_format = item;
          this.actionDis(`images/?search=${this.search_content}&page=1&cates=${this.cates_string}&pattern=${item}&ordering=${this.cur_order}`)
        },
        choiceOrder(item,index){
          for(let i=0;i<3;i++){
            this.$refs.order[i].style.color='#4a4a4a'
          }
          this.$refs.order[index].style.color='#ffd100'
          switch(item){
            case '最新上传':{
              item='-add_time';
              break
            }
            case '点赞最多':{
              item='-like_nums';
              break
            }
            case '收藏最多':{
              item='-collection_nums';
              break
            }
          }
          this.cur_order=item
          this.actionDis(`images/?search=${this.search_content}&page=1&cates=${this.cates_string}&ordering=${item}&pattern=${this.cur_format}`)
        },
        startSearch(){
          if(!this.search)
            return
          const {href}=this.$router.resolve({
            name:'search_result',
            params:{search_content:this.search}
          })
          window.open(href)
        },
        Page(item){
            this.actionDis(`images/?search=${this.search_content}&page=${item}&cates=${this.cates_string}&ordering=${this.cur_order}&pattern=${this.cur_format}`)
        },
      }
    }
</script>

<style lang="scss" scoped>
  @import "../styles/variables";
  .search_result{
    background: $bg;
  }
  .top-items{
    text-align: left;
    background: #fff;
    margin-bottom: 3rem;
  }
  .cates-choice{
    height: 10.6875rem;
    padding:1.5rem 6rem;
    border-bottom: 0.0625rem solid #e9e9e9;
  }

  /*
  position
   */
  .position{
    font-size: 1.125rem;
  }
  .position .all{
    background: $normal;
    color: #fff;
    height: 1.5625rem;
    display: inline-block;
    padding: 0 .5rem;
  }
  .position-item{
    background: $normal;
    display: inline-block;
    height: 1.5625rem;
    color: #fff;
    padding: 0 1.3rem 0 .5rem;
    position: relative;
  }
  .position-item a{
    color: #fff;
    display: inline-block;
    width: 1.3rem;
    height: 100%;
    font-size: 1.5rem;
    position: absolute;
    right: 0;
    text-align:center;
    &:hover{
      background: $hover;
    }
  }
  .position span:nth-child(1){
    margin-right: .0625rem;
  }
  .count{
    color: #ff0000;
  }
  .order{
    height: 4rem;
    padding: 0 6rem;
    border-bottom: 0.0625rem solid #e9e9e9;
    line-height:4rem;
  }
  .position,.classify,.format{
    margin-bottom: 1.5rem;
  }
  .classify,.format,.order{
    font-size: 1.25rem;
  }
  .first-title{
    font-weight: 600;
    margin-right: 2rem;
  }
  .classify a,.check-item,.order a{
    margin-right: 3rem;
  }
  .classify a:hover{
    color: $normal;
  }
  .order .search{
    float:right;
    width:46.5625rem;
    padding:.5rem 0;
    display:flex;
    justify-content:center;
    align-items:center;
  }
  #search{
    font-size: 1.25rem;
    height: 3rem;
    border: 0.0625rem solid #cecece;
    width: 40.5625rem;
    text-indent: 1.5rem;
    background: #fff;

  }
  .label{
    width: 6rem;
    height: 3rem;
    background:url(../assets/search_white.png) no-repeat center $normal;
    background-size:37.5%;
    cursor: pointer;
    &:hover{
      background-color: $hover;
    }
  }

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


  /*
  checkbox
   */
  [type="radio"]:checked,
  [type="radio"]:not(:checked)
  {
    position: absolute;
    left:-999999px;
    opacity: 0;
  }
  [type="radio"]:checked + label,
  [type="radio"]:not(:checked) + label
  {
    position: relative;
    padding-left: 1.6rem;
    cursor: pointer;
    line-height: 1.25rem;
    display: inline-block;
    color: #666;
  }
  [type="radio"]:checked + label:before,
  [type="radio"]:not(:checked) + label:before
  {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 1.125rem;
    height: 1.125rem;
    border: 0.0625rem solid #ddd;
    background: #fff;
  }
  [type="radio"]:checked + label:after,
  [type="radio"]:not(:checked) + label:after
  {
    content: '';
    width: 0.5rem;
    height: 0.5rem;
    background: $hover;
    position: absolute;
    top: 0.375rem;
    left: 0.375rem;
    -webkit-transition: all 0.2s ease;
    -moz-transition: all 0.2s ease;
    -o-transition: all 0.2s ease;
    transition: all 0.2s ease;
  }
  [type="radio"]:not(:checked) + label:after
  {
    opacity: 0;
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
    -o-transform: scale(0);
    -ms-transform: scale(0);
    transform: scale(0);
  }
  [type="radio"]:checked + label:after
  {
    opacity: 1;
    -webkit-transform: scale(1);
    -moz-transform: scale(1);
    -o-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
  }

</style>
