
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from plyer import gps
from jnius import autoclass
from kivy.uix.camera import Camera

class CameraApp(App):
    def build(self):
        # Request location permission if running on Android
        if self.is_android():
            self.request_android_permissions()

        layout = FloatLayout()

        # Check if the device has any cameras available
        if Camera.ids:
            # Create camera widget using the first camera (index 0)
            camera = Camera(index=-1)
            layout.add_widget(camera)
        else:
            print("No camera available on this device.")

        # Create label widget for displaying GPS coordinates
        self.label = Label(text="GPS Coordinates: ")
        layout.add_widget(self.label)

        # Create button widget for taking a photo
        button = Button(text="Take Photo", size_hint=(0.2, 0.1), pos_hint={'x': 0.4, 'y': 0.1})
        button.bind(on_release=self.take_photo)
        layout.add_widget(button)

        # Start GPS updates
        gps.configure(on_location=self.on_location)
        gps.start()

        return layout


    def is_android(self):
        try:
            from jnius import autoclass, jnius_config
            return jnius_config.vm_name == 'Dalvik'
        except ImportError:
            return False

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        permissions = [Permission.CAMERA, Permission.ACCESS_FINE_LOCATION]
        request_permissions(permissions)

    def take_photo(self, instance):
        # Capture photo
        camera = self.root.children[0]
        camera.export_to_png("photo.png")

    def on_location(self, **kwargs):
        # Update label with GPS coordinates
        self.label.text = "GPS Coordinates: {} {}".format(kwargs['lat'], kwargs['lon'])

    def update_arrow_angle(self, dt):
        # Get the orientation (in degrees) from the GPS or any other method you prefer
        # For demonstration purposes, we'll use a static value of 45 degrees here
        orientation = 45

        # Update the arrow widget with the new angle
        self.arrow.update_arrow(orientation)

class ArrowImage(Image):
    def __init__(self, **kwargs):
        super(ArrowImage, self).__init__(**kwargs)
        self.source = 'arrow_ahead_1.png'
        self.angle = 0

    def update_arrow(self, orientation):
        # Update the arrow's angle based on the user's orientation
        self.angle = orientation

if __name__ == '__main__':
    CameraApp().run()
