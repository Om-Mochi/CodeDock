from PyQt6 import QtWidgets, QtCore, QtGui, QtSvg
import xml.etree.ElementTree as ET


class CDLoader:

    class SVGRenderThread(QtCore.QThread):
        rendered = QtCore.pyqtSignal(QtGui.QPixmap)

        def __init__(self, svg_file_path, size, active_layer, layer_color):
            super().__init__()
            self.svg_file_path = svg_file_path
            self.size = size
            self.active_layer = active_layer  # "layer1", "layer2", or None
            self.layer_color = layer_color
            self._running = True

        def run(self):
            if not self._running:
                return

            # Create the final pixmap
            final_pixmap = QtGui.QPixmap(self.size.width(), self.size.height())
            final_pixmap.fill(QtCore.Qt.GlobalColor.transparent)

            # Load the original SVG
            svg_renderer = QtSvg.QSvgRenderer(self.svg_file_path)
            
            # Create painter for final composition
            final_painter = QtGui.QPainter(final_pixmap)

            if self.active_layer is None:
                # Render original SVG without any coloring
                svg_renderer.render(final_painter)
            else:
                # Render the SVG in grayscale/original first
                original_pixmap = QtGui.QPixmap(self.size.width(), self.size.height())
                original_pixmap.fill(QtCore.Qt.GlobalColor.transparent)
                original_painter = QtGui.QPainter(original_pixmap)
                svg_renderer.render(original_painter)
                original_painter.end()

                # Create a mask for the active layer by rendering only that layer
                layer_mask = self.create_layer_mask(self.active_layer)
                
                if layer_mask and not layer_mask.isNull():
                    # Draw original SVG first
                    final_painter.drawPixmap(0, 0, original_pixmap)
                    
                    # Create colored overlay
                    color_overlay = QtGui.QPixmap(self.size.width(), self.size.height())
                    color_overlay.fill(self.layer_color)
                    
                    # Apply the layer mask to the color overlay
                    masked_color = QtGui.QPixmap(self.size.width(), self.size.height())
                    masked_color.fill(QtCore.Qt.GlobalColor.transparent)
                    mask_painter = QtGui.QPainter(masked_color)
                    mask_painter.drawPixmap(0, 0, color_overlay)
                    mask_painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn)
                    mask_painter.drawPixmap(0, 0, layer_mask)
                    mask_painter.end()
                    
                    # Composite the colored layer over the original
                    final_painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceAtop)
                    final_painter.drawPixmap(0, 0, masked_color)
                else:
                    # If mask creation failed, just render original
                    final_painter.drawPixmap(0, 0, original_pixmap)

            final_painter.end()

            if self._running:
                self.rendered.emit(final_pixmap)

        def create_layer_mask(self, layer_id):
            """Create a mask pixmap for a specific layer"""
            try:
                # Read SVG content
                with open(self.svg_file_path, 'r', encoding='utf-8') as file:
                    svg_content = file.read()

                # Parse SVG and create a version with only the target layer visible
                root = ET.fromstring(svg_content)
                
                # Hide all layers except the target one
                for element in root.iter():
                    element_id = element.get('id')
                    if element_id and (element_id == 'layer1' or element_id == 'layer2'):
                        if element_id != layer_id:
                            # Hide this layer
                            element.set('style', 'display:none')
                        else:
                            # Make sure target layer is visible and black (for mask)
                            current_style = element.get('style', '')
                            # Remove any display:none
                            current_style = current_style.replace('display:none', '').strip()
                            element.set('style', current_style)
                            # Set all paths in this layer to black for better masking
                            self.set_layer_black(element)

                # Convert back to SVG string
                modified_svg = ET.tostring(root, encoding='unicode')
                
                # Render the modified SVG
                temp_renderer = QtSvg.QSvgRenderer()
                temp_renderer.load(modified_svg.encode('utf-8'))
                
                mask_pixmap = QtGui.QPixmap(self.size.width(), self.size.height())
                mask_pixmap.fill(QtCore.Qt.GlobalColor.transparent)
                mask_painter = QtGui.QPainter(mask_pixmap)
                temp_renderer.render(mask_painter)
                mask_painter.end()
                
                return mask_pixmap
            except Exception as e:
                print(f"Error creating layer mask: {e}")
                return QtGui.QPixmap()

        def set_layer_black(self, element):
            """Set all drawable elements in a layer to black for masking"""
            if element.tag.endswith(('path', 'circle', 'rect', 'polygon', 'ellipse', 'line')):
                element.set('fill', '#000000')
                element.set('stroke', '#000000')
            
            # Process children
            for child in element:
                self.set_layer_black(child)

        def stop(self):
            self._running = False

    class ThreadedFadeColorSVGLoader(QtWidgets.QWidget):
        def __init__(self, w=32, h=20, parent=None):    
            super().__init__(parent)
            self.svg_width = w
            self.svg_height = h
            self.setFixedSize(self.svg_width, self.svg_height)

            self.label = QtWidgets.QLabel(self)
            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.resize(self.svg_width, self.svg_height)

            # SVG file path
            self.svg_file_path = None
             
           # Initialize with original SVG
            
        
        def setSvgAndInit(self,path):
            
            self.svg_file_path = path
            self.original_pixmap = self.render_original_svg()
            self.label.setPixmap(self.original_pixmap)

            self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.label)
            self.label.setGraphicsEffect(self.opacity_effect)

            self.fade_anim = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
            self.fade_anim.setDuration(500)
            self.fade_anim.setStartValue(0.0)
            self.fade_anim.setEndValue(1.0)
            self.fade_anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
            self.fade_anim.finished.connect(self.on_fade_finished)

            # Define colors for each layer
            self.layer_colors = [
                QtGui.QColor("#419F68"),  # Red for layer1
                QtGui.QColor("#B4AC55"),  # Teal for layer2
            ]
            
            self.layer_ids = ["layer1", "layer2"]
            self.animation_state = 0  # 0: layer1, 1: layer2, 2: original
            self.animating = False
            self.thread: CDLoader.SVGRenderThread | None = None
        
        def render_original_svg(self):
            """Render the original SVG without color modifications"""
            svg_renderer = QtSvg.QSvgRenderer(self.svg_file_path)
            pixmap = QtGui.QPixmap(self.svg_width, self.svg_height)
            pixmap.fill(QtCore.Qt.GlobalColor.transparent)
            painter = QtGui.QPainter(pixmap)
            svg_renderer.render(painter)
            painter.end()
            return pixmap

        def start_animation(self):
            if self.animating:
                return
            self.animating = True
            self.animation_state = 0  # Start with layer1
            self.fade_anim.setDirection(QtCore.QAbstractAnimation.Direction.Forward)
            self.fade_anim.start()

        def stop_animation(self):
            self.animating = False
            self.fade_anim.stop()

            if self.thread is not None:
                self.thread.stop()
                self.thread.quit()
                self.thread.wait()
                self.thread.deleteLater()
                self.thread = None

            self.label.setPixmap(self.original_pixmap)
            self.opacity_effect.setOpacity(1.0)
            self.animation_state = 0

        def on_fade_finished(self):
            if not self.animating:
                return

            if self.fade_anim.direction() == QtCore.QAbstractAnimation.Direction.Forward:
                self.fade_anim.setDirection(QtCore.QAbstractAnimation.Direction.Backward)
            else:
                self.fade_anim.setDirection(QtCore.QAbstractAnimation.Direction.Forward)
                self.next_animation_state()

            self.fade_anim.start()

        def next_animation_state(self):
            """Move to the next animation state and render accordingly"""
            if self.thread is not None:
                self.thread.stop()
                self.thread.quit()
                self.thread.wait()
                self.thread.deleteLater()
                self.thread = None

            # Determine current state
            if self.animation_state == 0:
                # Show layer1 colored
                active_layer = "layer1"
                layer_color = self.layer_colors[0]
            elif self.animation_state == 1:
                # Show layer2 colored
                active_layer = "layer2"
                layer_color = self.layer_colors[1]
            else:
                # Show original (both layers normal)
                active_layer = None
                layer_color = QtGui.QColor()

            # Move to next state
            self.animation_state = (self.animation_state + 1) % 3

            # Start rendering
            self.thread = CDLoader.SVGRenderThread(self.svg_file_path, self.size(), active_layer, layer_color)
            self.thread.rendered.connect(self.on_pixmap_ready)
            self.thread.start()

        def on_pixmap_ready(self, pixmap):
            if not self.animating:
                return
            self.label.setPixmap(pixmap)

        def set_layer_colors(self, colors):
            """Set the colors for each layer"""
            self.layer_colors = colors

        def set_fade_duration(self, duration_ms):
            """Set the fade animation duration"""
            self.fade_anim.setDuration(duration_ms)


# Example usage:
"""
app = QtWidgets.QApplication([])

# Create the loader
loader = CDLoader.ThreadedFadeColorSVGLoader(64, 64)

# Set custom colors
loader.set_layer_colors([
    QtGui.QColor("#FF0000"),  # Red for layer1
    QtGui.QColor("#00FF00"),  # Green for layer2
])

# Show widget
loader.show()

# Start animation
loader.start_animation()

app.exec()

# Animation sequence:
# 1. layer1 in red, layer2 normal → fade out
# 2. layer1 normal, layer2 in green → fade out  
# 3. both layers normal → fade out
# 4. repeat...
"""