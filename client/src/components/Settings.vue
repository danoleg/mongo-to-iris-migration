<template>
    <div class="md-layout md-gutter">
        <div class="md-layout-item">
            <md-toolbar :md-elevation="1">
                <span class="md-title" style="flex: 1">MongoDB</span>
                <md-button class="md-primary" @click="saveMongo">Save</md-button>
            </md-toolbar>
            <md-field>
                <label>Connection string</label>
                <md-input v-model="mongo_connection_string"></md-input>
            </md-field>
            <md-field>
                <label>DB</label>
                <md-input v-model="mongo_db"></md-input>
            </md-field>

        </div>
        <div class="md-layout-item">
            <md-toolbar :md-elevation="1">
                <span class="md-title" style="flex: 1">IRIS</span>
                <md-button class="md-primary" @click="saveIris">Save</md-button>
            </md-toolbar>
            <md-field>
                <label>Host</label>
                <md-input v-model="iris_host"></md-input>
            </md-field>
            <md-field>
                <label>Port</label>
                <md-input v-model="iris_port"></md-input>
            </md-field>
            <md-field>
                <label>Namespace</label>
                <md-input v-model="iris_namespace"></md-input>
            </md-field>
            <md-field>
                <label>Username</label>
                <md-input v-model="iris_username"></md-input>
            </md-field>
            <md-field>
                <label>Password</label>
                <md-input type="password" v-model="iris_password"></md-input>
            </md-field>
        </div>
        <md-dialog-alert :md-active.sync="saved_success" md-content="Saved successfully" md-confirm-text="OK" />
    </div>

</template>

<script>
    import axios from 'axios';
    export default {
        name: "Settings",
        data() {
            return {
                mongo_connection_string: "",
                mongo_db: "",
                iris_host: "",
                iris_port: "",
                iris_namespace: "",
                iris_username: "",
                iris_password: "",
                saved_success: false
            };

        },
        mounted() {
            let that = this;
            axios.get('http://127.0.0.1:8011/settings').then(
                        function (response) {
                            that.mongo_connection_string = response.data.mongo_connection_string;
                            that.mongo_db = response.data.mongo_db;
                            that.iris_host = response.data.iris_host;
                            that.iris_port = response.data.iris_port;
                            that.iris_namespace = response.data.iris_namespace;
                            that.iris_username = response.data.iris_username;
                            that.iris_password = response.data.iris_password;
                        });
        },
        methods: {
            saveMongo() {
                this.formdata = {
                    mongo_connection_string: this.mongo_connection_string,
                    mongo_db: this.mongo_db
                };
                let that = this;
                axios.post('http://127.0.0.1:8011/settings/mongodb', this.formdata).then(
                    function (response) {
                        that.form_error = response.data.message;
                        that.iris_data = response.data.iris_data;
                        that.saved_success = true;
                    });

            },
            saveIris() {
                this.formdata = {
                    iris_host: this.iris_host,
                    iris_port: this.iris_port,
                    iris_namespace: this.iris_namespace,
                    iris_username: this.iris_username,
                    iris_password: this.iris_password
                };
                let that = this;
                axios.post('http://127.0.0.1:8011/settings/iris', this.formdata).then(
                    function (response) {
                        that.form_error = response.data.message;
                        that.iris_data = response.data.iris_data;
                        that.saved_success = true;
                    });

            },
        }
    }
</script>

<style scoped>

</style>