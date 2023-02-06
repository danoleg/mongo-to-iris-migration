<template>
    <div>
        <md-content>
          <p>{{ form_error }}</p>
        </md-content>
        <md-field>
            <label>Global name</label>
            <md-input v-model="iris_global_name"></md-input>
        </md-field>

        <md-button v-if="!loading" class="md-raised md-primary" @click="importFile">Export</md-button>
        <md-button v-if="loading" class="md-raised" disable>Exporting...</md-button>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: "ExportJson",
        data() {
            return {
                iris_global_name: "",
                uploaded_json_file_name: undefined,
                uploaded_json_file: undefined,
                form_error: "",
                download_href: "-",
                result: {},
                loading: false,
                formdata: {}
            };
        },
        methods: {
            handleFileUpload(fileList) {
               this.uploaded_json_file = fileList[0];
            },
            importFile(){
                this.loading = true
                if (this.iris_global_name === ""){
                   this.form_error = "Global name required"
                }else{
                    this.formdata = {
                        name: this.iris_global_name
                    };
                    let that = this;
                    axios.post('http://127.0.0.1:8011/export-iris-to-json', this.formdata).then(
                        function (response) {
                          that.result = response.data.result;
                          that.loading = false;

                          that.download(that.result);
                        });
                }
            },
          download(data) {
            if (this.iris_global_name === "") {
              this.form_error = "Global name required"
            } else {
              this.formdata = {
                name: this.iris_global_name
              };
              let that = this;
              axios.post('http://127.0.0.1:8011/check-global-from-iris', this.formdata).then(function (response) {

                if (response.data.data === 0){
                  that.form_error = "Global is empty or not found"
                }else{
                  let text = JSON.stringify(data);
                  let filename = that.iris_global_name+'.json';
                  let element = document.createElement('a');
                  element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(text));
                  element.setAttribute('download', filename);

                  element.style.display = 'none';
                  document.body.appendChild(element);

                  element.click();
                  document.body.removeChild(element);
                }
              });
            }

          }
        }
    }
</script>

<style scoped>

</style>