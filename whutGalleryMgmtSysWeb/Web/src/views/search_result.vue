<template>
  <div class="search_result">
    <tslg_header/>
    <div class="top-items">
     <div class="cates-choice">
       <div class="position">
         <span >当前位置：</span><span v-if="!position.length" ><span class="all">全部</span><span> > </span></span>
         <span v-for="item in position"><span class="position-item" ><span>{{item}}</span><a @click="deletePosition(item)" title="点击返回">×</a></span><span> > </span></span>
         <span>  {{search_content}}  </span>
         <span class="count">&nbsp;&nbsp;共{{count}}个结果</span>
       </div>
       <div class="classify">
         <span class="first-title">分类：</span><span><a @click="searchAll" ref="all">全部</a>
         <a v-for="(item,index) in cates_" @click="choiceCate(item,index)" ref="title" :class="{'active':index===aIndex}">{{item.name}}</a>
         <!--<a v-for="item in kids" v-if="kids.length" @click="choiceCate(item)" >{{item.name}}</a>-->
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
          <input id="search" type="text" placeholder="请输入关键字查询"  @keyup.enter="startSearch" v-model="search" ref="search_input" autocomplete="none"/>
          <label for="search" class="label" @click="startSearch"></label>
        </div>
      </div>
    </div>
    <image_card/>
    <div class="choice-page">
      <div class="cell" @click="choicePage(cur_page-1)"><i class="right"></i></div>
      <div class="cell" v-if="show_first" ref="first_page" @click="choicePage(1)">1</div>
      <div class="cell" v-if="show_first">...</div>
      <div v-for="(item,index) in page" v-if="index<6&&item<=page_num" class="cell" @click="choicePage(item)" :class="{'active_page':item===cur_page}" ref="pages">{{item}}</div>
      <div class="cell" v-if="show_last">...</div>
      <div class="cell" ref="last_page" v-if="show_last" @click="choicePage(page_num)">{{page_num}}</div>
      <div class="cell" @click="choicePage(cur_page+1)"><i class="left"></i></div>
    </div>
    <tslg_footer/>
  </div>
</template>

<script>
  import tslg_header from '../components/body/tslg_header'
  import tslg_footer from '../components/body/tslg_footer'
  import image_card from '../components/card/main_image_card'
  import {setTitle} from "../utils/user";
  import {getTitle} from '../api/get'
    export default {
        name: "search_result",
      components:{
          tslg_header,
          tslg_footer,
        image_card
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
            last_kids:[],
            search:'',
            page:[1,2,3,4,5,6],
            show_first:false,
            show_last:false,
            show_last_num:false,
            aIndex:-1,
            cur_page:1
          }
      },
      computed:{
          search_content(){
            // this.cates_string=this.$store.state.imageGroup.search_content
            return this.$store.state.imageGroup.search_content
          },
          count(){
            return this.$store.state.imageGroup.search_count
          },
          page_num(){
            return Math.ceil(this.$store.state.imageGroup.search_count/8)
          }
          // cates(){
          //   return this.$store.state.imageGroup.title
          //  }
       },
      created(){
        // setTitle()
        this.getCates()
        this.$store.commit('SET_NEXT_SEARCH',`images/?search=${this.search_content}&page=1`)
        this.$store.dispatch('setImageGroupT').then(()=>{})
      },
      mounted(){
        this.$refs.format_radio[0].checked=true
        this.$refs.all.style.color='#9ad3e2'
        this.$refs.order[0].style.color='#9ad3e2'
        if(this.page_num>7){
          this.show_last=true
        }
        if(this.page_num>6){
          this.show_last_num=true
        }
      },
      methods:{
          getCates(){
            getTitle().then((res)=>{
              this.cates=res.data
              this.cates_=res.data
              console.log(this.cates)
            })
          },
          getImage(){
            this.$store.commit('SET_NEXT_SEARCH',`images/search=${this.search_content}&page=1`)
          },
        choiceCate(item,index){
          if(item.kids.length){
            if(this.cates_string)
            this.cates_string=item.name+','+this.cates_string
            else  this.cates_string=item.name
            if(item.name!==this.search_content){
              this.$store.commit('SET_NEXT_SEARCH',`images/?search=${this.search_content}&cates=${this.cates_string}`)
              this.$store.dispatch('setImageGroupT').then(()=>{})
            }
            //this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string}`)
            this.last_kids.push(index)
            this.position.push(item.name)
            this.first=false
            this.cates_=item.kids
          }else{
            if(item.name!==this.search_content){
              if(this.cates_string)
                this.cates_string=item.name+','+this.cates_string
              else  this.cates_string=item.name
              this.$store.commit('SET_NEXT_SEARCH',`images/?search=${this.search_content}&cates=${this.cates_string}`)
              this.$store.dispatch('setImageGroupT').then(()=>{})
              //this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string+','+item.name}`)
              this.setColor(index)
            }

          }
          this.$store.commit('SET_IMAGEGROUP');
          this.$store.dispatch('setCates').then(()=>{})
        },
        deletePosition(item){
            let position=this.last_kids
            this.last_kids.splice(position-1,1)
            console.log(this.last_kids)
            let len=this.last_kids.length
            if(len<2){
                this.cates_=this.cates
            }else{
              let kids=this.cates[position[0]].kids
              if(len<3){
                this.cates_=kids
              }else{
                for(let i=1;i<len-1;i++){
                  kids=kids[position[i]].kids
                }
                this.cates_=kids
              }
            }
          this.$refs.all.style.color='#9ad3e2'
          this.aIndex=-1
          this.position.splice(this.position.indexOf(item),1)
          this.cates_string=this.cates_string.replace(',','')
          this.cates_string=this.cates_string.split(item)
          if(this.cates_string.length>2)
            this.cates_string=this.cates_string.join(',')
          else this.cates_string=this.cates_string.join('')
          this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string}`)
          this.$store.commit('SET_IMAGEGROUP');
          this.$store.dispatch('setCates').then(()=>{})
        },
        searchAll(){
          this.$refs.all.style.color='#9ad3e2'
          this.aIndex=-1
          if(this.cates_string){
            this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string}`)
            this.$store.commit('SET_IMAGEGROUP');
            this.$store.dispatch('setCates').then(()=>{})
          }
        },
        setColor(index){
          this.$refs.all.style.color='#4a4a4a'
          this.aIndex=index
        },
        choiceFormat(item){
            // if(this.cates_string){
              if(item==='全部'){
                console.log('in')
                this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string}`)
              }else{
                this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string}&pattern=${item}`)
              }
              this.$store.commit('SET_IMAGEGROUP');
              this.$store.dispatch('setCates').then(()=>{})
            // }else{
            //   if(item==="全部"){
            //     this.$store.commit('SET_NEXT_SEARCH',`images/?search=${this.search_content}&page=1`)
            //   }else
            //   this.$store.commit('SET_NEXT_SEARCH',`images/?search=${this.search_content}&page=1&pattern=${item}`)
            //   this.$store.dispatch('setImageGroupT').then(()=>{})
            // }
        },
        choiceOrder(item,index){
          for(let i=0;i<3;i++){
            this.$refs.order[i].style.color='#4a4a4a'
          }
          this.$refs.order[index].style.color='#9ad3e2'
          switch(item){
            case '最新上传':{
              item='add_time';
              break
            }
            case '点赞最多':{
              item='like_nums';
              break
            }
            case '收藏最多':{
              item='collection_nums';
              break
            }
          }
            // if(this.cates_string){
              if(item==='默认'){
                this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string}`)
              }else {
                this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string}&ordering=${item}`)
                this.$store.commit('SET_IMAGEGROUP');
                this.$store.dispatch('setCates').then(()=>{})
              }
            // }else{
            //   this.$store.commit('SET_NEXT_SEARCH',`images/?search=${this.search_content}&page=1&ordering=${item}`)
            //   this.$store.dispatch('setImageGroupT').then(()=>{})
            // }
        },
        startSearch(){
          if(!this.search_content){
            this.$refs.search_input.style.border='0.0625rem solid #ff0000'
            return
          }else this.$refs.search_input.style.border='0.0625rem solid #cecece'
          const {href}=this.$router.resolve({
            name:'search_result',
            params:{search_content:this.search}
          })
          window.open(href)
        },
        choicePage(item){
            console.log(item)
            if(item<=0||item>this.page_num)
              return
            this.cur_page=item
              this.$store.commit('SET_NEXT_CATES',`cates=${this.cates_string}&page=${item}`)
              this.$store.commit('SET_IMAGEGROUP');
              this.$store.dispatch('setCates').then(()=>{})
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
              // this.$refs.last_page.style.background=
            }
          }


        }
      }
    }
</script>

<style scoped>
  .search_result{
    background: #f7fafb;
  }
  .top-items{
    text-align: left;
    background: #fff;
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
    background: #9ad3e2;
    color: #fff;
    height: 1.5625rem;
    display: inline-block;
    padding: 0 .5rem;
  }
  .position-item{
    background: #9ad3e2;
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
  }
  .position-item a:hover{
    background:#2cbec6;
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
    color: #9ad3e2;
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
    background:url(../assets/search_white.png) no-repeat center #9dd4e3;
    background-size:37.5%;
    cursor: pointer;
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
    line-height:3rem;
    margin:0 .375rem;
    cursor:pointer;
  }
  .cell:active{
    background:#9ad3e2;
  }
  .active{
    color:#9ad3e2;
  }
  .active_page{
    background:#9ad3e2;
    color:#4a4a4a;
  }
  .choice-page i{
    display: inline-block;
    width: 1.25rem;
    height: 1.25rem;
    -webkit-background-size:cover;
    background-size: cover;
    background: url(../assets/pull_down.png) no-repeat center;
  }
  .right{
    transform: rotate(90deg);
  }
  .left{
    transform: rotate(-90deg);
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
    background: #00a69c;
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
