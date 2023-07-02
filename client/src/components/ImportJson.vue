<template>
    <div>
        <md-content>
          <p>{{ form_error }}</p>
        </md-content>
        <md-field>
            <label>Global name</label>
            <md-input v-model="iris_global_name"></md-input>
        </md-field>

        <md-field>
            <label>Upload file</label>
            <md-file v-model="uploaded_json_file_name" placeholder="Example: data.json" @change="handleFileUpload"/>
        </md-field>

        <md-button class="md-raised md-primary" @click="importFile">Import</md-button>
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
        name: "ImportJson",
        data() {
            return {
                iris_global_name: "",
                uploaded_json_file_name: undefined,
                uploaded_json_file: undefined,
                uploaded_json: "",
                form_error: "",
                iris_data: [],
                result: "",
                formdata: {},
                imported: false,
                deleted: false
            };
        },
        methods: {
            handleFileUpload(event) {
               this.uploaded_json_file = event.target.files[0];
            },
            importFile(){
                if (this.iris_global_name === ""){
                   this.form_error = "Global name required"
                }else if(this.uploaded_json_file === undefined){
                   this.form_error = "File required"
                }else if(this.uploaded_json_file.type !== 'application/json'){
                   this.form_error = "File format error"
                }else{
                  const formData = new FormData();
                  formData.append('name', this.iris_global_name);
                  formData.append('file', this.uploaded_json_file);


                  axios.post('http://127.0.0.1:8011/import-json-file-to-iris', formData, {
                    headers: {
                      'Content-Type': 'multipart/form-data',
                    },
                  })
                  .then(response => {
                    this.form_error = response.data.message;
                    this.iris_data = response.data.iris_data;
                  })
                  .catch(error => {
                    this.form_error = "Error";
                    console.error(error);
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