<template>
  <md-list>
    <md-list-item to="/">
      <md-icon>move_to_inbox</md-icon>
      <span class="md-list-item-text">Import from MongoDB</span>
    </md-list-item>

    <md-list-item to="/import/pgsql">
      <md-icon>move_to_inbox</md-icon>
      <span class="md-list-item-text">Import from PostgeSQL</span>
    </md-list-item>

    <md-list-item to="/import/custom-json">
      <md-icon>move_to_inbox</md-icon>
      <span class="md-list-item-text">Import from custom JSON</span>
    </md-list-item>

    <md-list-item to="/import/json">
      <md-icon>move_to_inbox</md-icon>
      <span class="md-list-item-text">Import from JSON file</span>
    </md-list-item>

    <md-list-item to="/export/json">
      <md-icon>file_download</md-icon>
      <span class="md-list-item-text">Export to JSON file</span>
    </md-list-item>

    <md-list-item to="/settings">
      <md-icon>settings</md-icon>
      <span class="md-list-item-text">Settings</span>
    </md-list-item>
  </md-list>
</template>

<script>
export default {
  name: "Navigation"
}
</script>

<style scoped>
a.router-link-active, li.router-link-active > a {
  color: red;
}
</style>