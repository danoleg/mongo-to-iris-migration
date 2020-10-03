<template>
    <div>
        <md-content>
            <p style="color: orange">{{ form_error }}</p>
        </md-content>
        <md-field>
            <label>Global name</label>
            <md-input v-model="iris_global_name" required></md-input>
        </md-field>
        <md-field :class="messageClass">
            <label>JSON</label>
            <md-textarea v-model="uploaded_json" required></md-textarea>
        </md-field>

        <md-button class="md-raised md-primary" @click="sendData">Import</md-button>
        <md-button class="md-raised" @click="getData">Check data</md-button>
        <md-button class="md-accent" @click="removeData">Delete Global from IRIS</md-button>

        <md-table>
            <md-table-row>
                <md-table-head>Node</md-table-head>
                <md-table-head>Value</md-table-head>
            </md-table-row>

            <md-table-row v-for="item in iris_data" :key="item.path_list">
                <md-table-cell>
                    <span>^{{iris_global_name}}(</span>
                    <span v-for="(list, index) in item.path_list" :key="index">
                        <span>{{list}}</span><span v-if="index+1 < item.path_list.length">, </span>
                    </span>
                    <span>)</span>
                </md-table-cell>
                <md-table-cell>{{item.value}}</md-table-cell>
            </md-table-row>


        </md-table>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "ImportCustomJson",
        data() {
            return {
                iris_global_name: "",
                uploaded_json: '{\n' +
                    '"products_qty":100000,\n"users_qty":43\n' +
                    '}',
                form_error: "",
                iris_data: [],
                result: "",
                formdata: {},
                imported: false,
                deleted: false
            };
        },
        methods: {
            sendData() {
                if (this.iris_global_name === "") {
                    this.form_error = "Global name required"
                } else if (this.uploaded_json === "") {
                    this.form_error = "JSON required"
                } else {
                    this.formdata = {
                        name: this.iris_global_name,
                        json: this.uploaded_json
                    };
                    let that = this;
                    axios.post('http://127.0.0.1:8011/import-custom-json-to-iris', this.formdata).then(
                        function (response) {
                            that.form_error = response.data.message;
                            that.iris_data = response.data.iris_data;
                        });
                }
            },
            getData() {
                if (this.iris_global_name === "") {
                    this.form_error = "Global name required"
                } else {
                    this.formdata = {
                        name: this.iris_global_name
                    };
                    axios.post('http://127.0.0.1:8011/check-global-from-iris', this.formdata).then(response => (this.form_error = response.data.data + " root nodes in ^" + this.iris_global_name));

                }
            },
            removeData() {
                if (this.iris_global_name === "") {
                    this.form_error = "Global name required"
                } else {
                    this.formdata = {
                        name: this.iris_global_name,
                    };
                    axios.post('http://127.0.0.1:8011/remove-global-from-iris', this.formdata).then(response => (this.result = response.statusText));
                    this.form_error = "^" + this.iris_global_name + " removed successfully";
                    this.iris_data = []
                }
            }

        }
    }
</script>

<style scoped>

</style>