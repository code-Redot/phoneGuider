import time

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivy_garden.mapview.geojson import GeoJsonMapLayer

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    MapView:
        id: mapview
        lat: 0
        lon: 0
        zoom: 14
    MDRectangleFlatButton:
        text: 'Select Map'
        on_release: root.open_file_manager()
        size_hint_y: None
        height: '48dp'

''')


class CameraClick(MDBoxLayout):
    map_filename = ""

    def open_file_manager(self):
        file_manager = MDFileManager(exit_manager=self.exit_file_manager, select_path=self.select_path)
        file_manager.show()

    def exit_file_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.map_filename = path
        self.load_geojson()
        self.file_manager.close()

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


class TestCamera(MDApp):
    def build(self):
        return CameraClick()


if __name__ == "__main__":
    try:
        TestCamera().run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
