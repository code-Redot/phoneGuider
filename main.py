import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy_garden.mapview.geojson import GeoJsonMapLayer, MapLayer
from gi.repository import Gst
import cv2
import time



kivy.require('2.0.0')

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    MapView:
        id: mapview
        lat: 0
        lon: 0
        zoom: 14
    FileChooserListView:
        id: filechooser
        on_selection: root.load_map()
    Camera:
        id: camera
        resolution: (1920, 1080)
        play: False
    ToggleButton:
        text: 'Play'
        on_press:
            camera.play = not camera.play
            if camera.play: root.start_gps()
            else: root.stop_gps()
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_release: root.capture()
''')


class CameraClick(BoxLayout):
    map_filename = StringProperty()

    def start_gps(self):
        mapview = self.ids.mapview
        mapview.start()

    def stop_gps(self):
        mapview = self.ids.mapview
        mapview.stop()

    def load_map(self):
        filechooser = self.ids.filechooser
        selected_file = filechooser.selection and filechooser.selection[0]
        if selected_file:
            print("Selected Map:", selected_file)
            self.map_filename = selected_file
            self.load_geojson()

    def load_geojson(self):
        mapview = self.ids.mapview
        mapview.remove_layer("geojson")
        if self.map_filename:
            try:
                geojson_layer = GeoJsonMapLayer(source=self.map_filename, name="geojson")
                mapview.add_layer(geojson_layer)
                mapview.center_on(*geojson_layer.bbox.center, zoom=14)
            except Exception as e:
                print("Error loading GeoJSON:", e)

    def capture(self):
        '''
        Function to capture the images and give them names
        based on the captured time and date.
        '''
        camera = self.ids.camera
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = f"IMG_{timestr}.png"
        camera.export_to_png(filename)
        print(f"Captured image: {filename}")


class TestCamera(App):
    def build(self):
        return CameraClick()


if __name__ == "__main__":
    try:
        from kivy.config import Config
        Config.set('kivy', 'log_level', 'debug')
        TestCamera().run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
