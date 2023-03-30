import octoprint.plugin

class PrintQueuePlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.TemplatePlugin):

    def on_after_startup(self):
        self._queue = []

    def get_settings_defaults(self):
        return dict(
            colors=["red", "green", "blue"],
            max_queue_size=10
        )

    def get_assets(self):
        return dict(
            js=["js/printqueue.js"]
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False),
            dict(type="tab", name="Print Queue", template="printqueue.jinja2")
        ]

    def get_update_information(self):
        return dict(
            printqueue=dict(
                displayName="Print Queue",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="me8myself",
                repo="OctoPrint-PrintQueue",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/yourgithubusername/OctoPrint-PrintQueue/archive/{target_version}.zip"
            )
        )

    def on_event(self, event, payload):
        if event == "PrintStarted":
            # Remove the printed item from the queue
            self._queue.pop(0)
            self._update_ui()

    def add_to_queue(self, model_name, color, user_name):
        # Add the item to the queue
        self._queue.append(dict(
            model_name=model_name,
            color=color,
            user_name=user_name
        ))
        self._update_ui()

    def get_queue(self):
        # Return the current queue
        return self._queue

    def clear_queue(self):
        # Clear the queue
        self._queue = []
        self._update_ui()

    def _update_ui(self):
        # Notify the frontend that the queue has been updated
        self._plugin_manager.send_plugin_message(self._identifier, dict(
            queue=self.get_queue()
        ))
