import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import i18n from './composables/useI18n';

// Import CSS Design Tokens and Core Styles
import '@mdi/font/css/materialdesignicons.css';
import './styles/variables.css';
import './styles/base.css';
import './styles/animations.css';

const app = createApp(App);

app.use(router);
app.use(i18n);

app.mount('#app');
