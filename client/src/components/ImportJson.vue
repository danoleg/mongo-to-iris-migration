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
            <md-file v-model="uploaded_json_file_name" placeholder="Example: data.json" @change="handleFileUpload($event.target.files)"/>
        </md-field>

        <md-button class="md-raised md-primary" @click="importFile">Import</md-button>
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
                form_error: "",
                result: "",
                formdata: {}
            };
        },
        methods: {
            handleFileUpload(fileList) {
               this.uploaded_json_file = fileList[0];
            },
            importFile(){
                if (this.iris_global_name === ""){
                   this.form_error = "Global name required"
                }else if(this.uploaded_json_file === undefined){
                   this.form_error = "File required"
                }else{
                    this.formdata = {
                        name: this.iris_global_name
                    };
                    axios.post('http://127.0.0.1:8011/import-json-file-to-iris', this.formdata).then(response => (this.result = response.statusText));
                }


            }
        }
    }
</script>

<style scoped>

</style>