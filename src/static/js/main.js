console.log('main.js loaded'); // 检查js是否生效

// --- 组件 ---
const Login = {
  template: `
    <div class="container mt-5">
      <h2>用户登录</h2>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">用户名</label>
          <input type="text" class="form-control" id="username" v-model="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">密码</label>
          <input type="password" class="form-control" id="password" v-model="password" required>
        </div>
        <button type="submit" class="btn btn-primary">登录</button>
      </form>
      <div class="mt-3 text-danger" v-if="error">{{ error }}</div>
    </div>
  `,
  data() {
    return {
      username: '',
      password: '',
      error: ''
    };
  },
  mounted() {
    console.log('Login component mounted');
  },
  methods: {
    async login() {
      try {
        const res = await axios.post('/api/auth/login', {
          username: this.username,
          password: this.password
        });
        if (res.data.success) {
          this.$router.push('/');
        } else {
          this.error = res.data.message || '登录失败';
        }
      } catch (e) {
        this.error = '服务器错误';
      }
    }
  }
};

const 主页 = {
  template: `<div class="container mt-5"><h2>首页</h2><p>欢迎来到师能素质协会平台。</p></div>`,
  mounted() { console.log('Home component mounted'); }
};

const Activities = {
  template: `<div class="container mt-5"><h2>活动列表</h2><p>这里显示活动内容。</p></div>`,
  mounted() { console.log('Activities component mounted'); }
};

// --- 路由 ---
const routes = [
  { path: '/', component: 主页 },
  { path: '/login', component: Login },
  { path: '/activities', component: Activities }
];

const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes
});

// --- Vue应用 ---
const app = Vue.createApp({});
app.use(router);
app.mount('#app');
