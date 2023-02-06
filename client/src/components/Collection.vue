<template>
    <div class="md-layout md-gutter">
        <div class="md-layout-item">
            <md-toolbar :md-elevation="1">
                <span class="md-title" style="flex: 1">MongoDB</span>
                <md-button class="md-raised md-primary" @click="importToIris">Import To IRIS
                    <md-icon>forward</md-icon>
                </md-button>
            </md-toolbar>
            <br>
            <span class="md-subheading">Collection: {{collection}}</span><br>
            <span class="md-subheading">Collection size: <b>{{docs_count}}</b> documents</span><br><br>
            <span class="md-subheading">Document preview:<br></span>
            <tree-view :data="first_doc" :options="{maxDepth: 3}"></tree-view>

        </div>
        <div class="md-layout-item">
            <md-toolbar :md-elevation="1">
                <span class="md-title" style="flex: 1">IRIS</span>
                <md-button class="md-accent" @click="removeData" v-if="iris_root_nodes_count>0">Clear Global</md-button>
            </md-toolbar>
            <br>
            <span class="md-subheading">Global: ^{{collection}}</span><br>
            <span class="md-subheading">Number of nodes: <b>{{iris_root_nodes_count}}</b></span><br><br>
            <span class="md-subheading" v-if="iris_root_nodes_count>0">Node data preview:</span><br>
            <md-table v-if="iris_root_nodes_count>0">
                <md-table-row>
                    <md-table-head>Node</md-table-head>
                    <md-table-head>Value</md-table-head>
                </md-table-row>
                <md-table-row v-for="item in iris_data" :key="item.path_list">
                    <md-table-cell>
                        <span>^{{collection}}(</span>
                        <span v-for="(list, index) in item.path_list" :key="index">
                        <span>{{list}}</span><span v-if="index+1 < item.path_list.length">, </span>
                    </span>
                        <span>)</span>
                    </md-table-cell>
                    <md-table-cell>{{item.value}}</md-table-cell>
                </md-table-row>
            </md-table>
        </div>
        <md-dialog-alert :md-active.sync="saved_success" md-content="Imported successfully" md-confirm-text="OK"/>
        <md-dialog-alert :md-active.sync="removed_success" md-content="Data deleted successfully" md-confirm-text="OK"/>

        <md-dialog :md-active.sync="processing">
            <md-progress-spinner style="margin:0 auto;" md-mode="indeterminate"></md-progress-spinner>
            <div style="text-align: center">Processing...</div>
        </md-dialog>


        <!--        <md-button class="md-raised md-primary" >Import</md-button>-->
        <!--        <md-button class="md-accent" @click="removeData">Delete Global from IRIS</md-button>-->
    </div>
</template>

<script>
    import axios from 'axios';


    export default {
        name: "Collection",
        props: ['collection'],
        data() {
            return {
                docs_count: 0,
                iris_root_nodes_count: 0,
                first_doc: "",
                iris_data: [],
                formdata: {},
                saved_success: false,
                removed_success: false,
                processing: false
            };
        },
        mounted() {
            let that = this;
            axios.get('http://127.0.0.1:8011/mongodb-collections/' + this.collection).then(
                function (response) {
                    that.docs_count = response.data.docs_count;
                    that.iris_root_nodes_count = response.data.iris_root_nodes_count;
                    that.iris_data = response.data.iris_data;
                    that.first_doc = JSON.parse(response.data.first_doc);
                });
        },
        methods: {
            importToIris() {
                this.processing = true;
                this.formdata = {
                    collection_name: this.collection,
                };
                let that = this;
                axios.post('http://127.0.0.1:8011/mongodb-collections/to-iris', this.formdata).then(
                    function (response) {
                        that.iris_data = response.data.iris_data;
                        that.iris_root_nodes_count = response.data.iris_root_nodes_count;
                        that.processing = false;
                        that.saved_success = true;
                    });
            },
            removeData() {
                this.formdata = {
                    name: this.collection,
                };
                let that = this;
                axios.post('http://127.0.0.1:8011/remove-global-from-iris', this.formdata).then(
                    function () {
                        that.iris_data = [];
                        that.iris_root_nodes_count = 0;
                        that.removed_success = true;
                    });
            }
        }
    }
</script>

<style scoped>

</style>