import os
# KIVY library for GUI 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView

class ImageApp(App):
    def build(self):
        self.image_folder = '/home/rantonio/Desktop/Images2'  # Replace with your image folder path
        self.images = [f for f in os.listdir(self.image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.current_index = 0

        # Create the main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Image display
        self.image_widget = AsyncImage(source=os.path.join(self.image_folder, self.images[self.current_index]))
        layout.add_widget(self.image_widget)

        # Buttons
        button_layout = BoxLayout(spacing=10)

        prev_button = Button(text='Previous', on_press=self.show_previous_image)
        next_button = Button(text='Next', on_press=self.show_next_image)
        add_button = Button(text='Add Image', on_press=self.add_image)
        delete_button = Button(text='Delete Image', on_press=self.delete_image)

        button_layout.add_widget(prev_button)
        button_layout.add_widget(next_button)
        button_layout.add_widget(add_button)
        button_layout.add_widget(delete_button)

        layout.add_widget(button_layout)

        return layout

    def show_previous_image(self, instance):
        self.current_index = (self.current_index - 1) % len(self.images)
        self.update_image()

    def show_next_image(self, instance):
        self.current_index = (self.current_index + 1) % len(self.images)
        self.update_image()

    def add_image(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.select_image_path)
        popup = BoxLayout(orientation='vertical')
        popup.add_widget(file_chooser)

        def dismiss_popup(_):
            popup.parent.dismiss()

        popup.add_widget(Button(text='Cancel', on_press=dismiss_popup))
        popup.parent = popup

        popup_window = self.root_window
        popup_window.add_widget(popup)
        popup_window.open()

    def select_image_path(self, instance, value):
        if value:
            self.images.append(os.path.basename(value[0]))
            self.update_image()
        instance.parent.parent.dismiss()

    def delete_image(self, instance):
        if self.images:
            os.remove(os.path.join(self.image_folder, self.images[self.current_index]))
            del self.images[self.current_index]
            self.current_index = min(self.current_index, len(self.images) - 1)
            self.update_image()

    def update_image(self):
        if self.images:
            self.image_widget.source = os.path.join(self.image_folder, self.images[self.current_index])
