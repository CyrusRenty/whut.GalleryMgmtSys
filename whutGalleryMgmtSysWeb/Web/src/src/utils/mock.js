import Mock from 'mockjs'

var template={
  'collectPhotos|8':
    [
      {
        'image':[
          {'url':'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg'},
          {'url':'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg'},
          {'url':'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg'},
          {'url': 'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg'},
        ],
        'id|1-30':1,
        'user':'@cname',
        'desc':'@ctitle',
        'create_date|1-30':10,
        'update_date|1-30':10,
        'list_nums|50-100':10,
        'name':'@cname',
        'nums|1-30':0,
      }
    ],
  'photos':
      {
        'count|1-10':0,
        'results|8': [{
          'image':'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg',
          'cates':'@Csentence',
          'download_nums|50-100':10,
          'like|50-100':10,
          'collection|50-100':10,
          'name':'@cname',
          'id|1-20':0,
          'desc':'@csentence',
          'user':{'id|1-100':0,'username':'@cname','image':'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg'}
        }]
    },
  'download':{
    'count|1-10':0,
    'results|8': [{
      'image':{
        'image':'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg',
        'cates':'@Csentence',
        'download_nums|50-100':10,
        'like|50-100':10,
        'collection|50-100':10,
        'name':'@cname',
        'id|1-20':0,
        'user':{'username':'@sentence','image':'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg'}
      }
    }]
  },
  'comment|5-10':[{
    'user':{'image':'https://mir-s3-cdn-cf.behance.net/project_modules/1400/51b65664980791.5b030e5594f39.jpg','username':'@cname'},
    'content':'@csentence',
    'add_time':'@Date',
    'if_like':false,
    'like|1-1000':0,
    "kids|-2-10": [
      {
        "id": 11,
        "image": 8,
        "if_like": false,
        "user": {
          "image": "http://111.231.230.54/media/heads/2018/08/20180821215847_98.jpg",
          "id": 1,
          "username": "aiyane",
          "upload_nums": 21,
          "fan_nums": 2
        },
        "add_time": "2018-08-22",
        "content": "@csentence",
        "floor": 3,
        "is_add_info": true,
        "like|0-1000": 0,
        "num": 0,
        "reply": 'aiyane'
      }
    ]
  }]
}
var mockData=Mock.mock(template)

let mock={
  collect:mockData.collectPhotos,
  photos:mockData.photos,
  download:mockData.download,
  comment:mockData.comment
}
export default mock
