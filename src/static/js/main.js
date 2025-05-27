console.log('main.js loaded');

const 主页 = { template: '<div class="container mt-5"><h2>首页</h2><p>欢迎来到师能素质协会平台。</p></div>' };
const Activities = { template: '<div class="container mt-5"><h2>活动列表</h2><p>这里显示活动内容。</p></div>' };
const Login = { template: '<div class="container mt-5"><h2>登录页</h2><p>这里是登录表单。</p></div>' };

const routes = [
  { path: '/', component: 主页 },
  { path: '/activities', component: Activities },
  { path: '/login', component: Login }
];

const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes
});

const app = Vue.createApp({});
app.use(router);
app.mount('#app');
