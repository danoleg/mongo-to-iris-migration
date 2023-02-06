import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import Collections from './components/Collections.vue'
import PostgresList from './components/PostgresList.vue'
import PostgresTable from './components/PostgresTable.vue'
import Collection from './components/Collection.vue'
import ImportJson from './components/ImportJson.vue'
import ImportCustomJson from './components/ImportCustomJson.vue'
import Settings from './components/Settings.vue'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import TreeView from "vue-json-tree-view"
import ExportJson from "./components/ExportJson";



Vue.use(VueRouter);
Vue.use(VueMaterial);
Vue.use(TreeView);

Vue.config.productionTip = false;

const routes = [
    {path: '/', component: Collections},
    {path: '/import/custom-json', component: ImportCustomJson},
    { path: '/import/mongo/:collection', name: 'collection', component: Collection, props: true},
    { path: '/import/pgsql/:table', name: 'table', component: PostgresTable, props: true},
    {path: '/import/json', component: ImportJson},
    {path: '/export/json', component: ExportJson},
    { path: '/settings', component: Settings },
    {path: '/import/pgsql', component: PostgresList},
];

const router = new VueRouter({
    routes
});

new Vue({
    router,
    render: h => h(App),
    data() {
        return {
            iris_global_name: "",
            uploaded_json_file: ""
        };
    }
}).$mount('#app');
