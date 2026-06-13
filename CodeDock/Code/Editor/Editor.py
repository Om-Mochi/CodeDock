from PyQt6 import QtWidgets,QtCore,QtGui
import re
impo
class Editor:
    
    class TextEditMinimap(QtWidgets.QPlainTextEdit):
        """ Minimap with a fixed viewport height and overlay for the visible area. """
        def __init__(self):
            super().__init__()
            self.editor = None
            self.subwindow = None
            self.dragging = False  # Track if the viewport is being dragged
            self.last_scroll_state=None
            self.ignore_sync = False  # Prevent unwanted sync loop
            
            self.minimap_bg = "#000000"
            self.brdr_width = 2
            self.vp_rgba =[0,0,0,80]
            self.vp_brdr_rgba=[121,225,123,255]
            self.vp_brdr_hover_rgba=[285,176,255,255]

            self.applyViewPortStyle()
            self.applyViewPortBorderStyle()
            self.applyMiniMapStyle()
            self.viewport_clr = QtGui.QColor(*self.vp_rgba)
            self.viewport_brdr_clr = QtGui.QColor(*self.vp_brdr_rgba)
            self.viewport_brdr_hover= QtGui.QColor(*self.vp_brdr_hover_rgba)


            self.setReadOnly(True)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  
            self.setFont(QtGui.QFont("Noto Mono", 2))  
            self.setFixedWidth(110)  
            self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)

            # Connect minimap scroll to editor scroll
            self.verticalScrollBar().valueChanged.connect(self.sync_editor_scroll)
            
        def getVarDict(self):
            return {
                'minimap_bg':self.minimap_bg,
                'vp_rgba':self.vp_rgba,
                'vp_brdr_rgba':self.vp_brdr_rgba,
                'vp_brdr_hover_rgba':self.vp_brdr_hover_rgba,
                'brdr_width':self.brdr_width,
            }
        
        def updateVar(self,TextEditMinimap,dict):
            TextEditMinimap.minimap_bg=dict["minimap_bg"]
            TextEditMinimap.vp_rgba=dict["vp_rgba"]
            TextEditMinimap.vp_brdr_rgba=dict["vp_brdr_rgba"]
            TextEditMinimap.vp_brdr_hover_rgba=dict["vp_brdr_hover_rgba"]
            TextEditMinimap.brdr_width=dict["brdr_width"]

        def applyViewPortStyle(self):
            if self.editor!=None and self.subwindow!=None:
                self.viewport_clr = QtGui.QColor(*self.vp_rgba)
                self.viewport().update()

        def applyViewPortBorderStyle(self):
            if self.editor!=None and self.subwindow!=None:
                self.viewport_brdr_clr = QtGui.QColor(*self.vp_brdr_rgba)
                self.viewport_brdr_hover= QtGui.QColor(*self.vp_brdr_hover_rgba)
                self.viewport().update()

        def applyMiniMapStyle(self):
            self.setStyleSheet(f"background-color:{self.minimap_bg};")

            
        def paintEvent(self, event):
            if self.editor!=None and self.subwindow!=None:
                #self.setStyleSheet("background-color:white;")
                

                super().paintEvent(event)
                
                painter_viewport = QtGui.QPainter(self.viewport())
                painter_lborder = QtGui.QPainter(self.viewport())
                editor_scroll = self.editor.verticalScrollBar()
            
                # Get total lines in editor
                total_lines = self.editor.blockCount()
                visible_lines = self.editor.viewport().height() / self.editor.fontMetrics().height()

                # Calculate overlay position and height


                font_metric=QtGui.QFontMetrics(self.font())
                line_height=font_metric.lineSpacing()  # Includes line spacing

                # Calculate the height of 20 visible lines
                
                self.viewport_height=int(line_height*visible_lines)


                scale_factor = self.editor.height() / total_lines
                self.viewport_y = int(editor_scroll.value() * scale_factor)
                #self.viewport_height = max(1, int(visible_lines*scale_factor))
                # Draw the overlay
                    
                painter_viewport.fillRect(QtCore.QRect(0, self.viewport_y, self.viewport().width(), self.viewport_height), self.viewport_clr)
                
                if self.dragging==True:
                    #painter_lborder=QtGui.QPainter(self.viewport())

                    painter_lborder.fillRect(QtCore.QRect(0, self.viewport_y,self.brdr_width,self.viewport_height),self.viewport_brdr_hover)
                else:
                    painter_lborder.fillRect(QtCore.QRect(0, self.viewport_y,self.brdr_width,self.viewport_height),self.viewport_brdr_clr)
                painter_viewport.end()
            else:pass

        def mouseReleaseEvent(self, event):
            """ Stops dragging when mouse button is released. """
            self.dragging = False
            self.viewport().update()
        def mousePressEvent(self, event):
            """ Detects when the viewport is clicked and starts dragging. """
            if self.editor is None:
                return

            click_y = event.position().y()
            if self.viewport_y <= click_y <= self.viewport_y + self.viewport_height:
                self.dragging = True
            else:
                # Move viewport immediately to follow cursor
                self.set_viewport_position(click_y)

            event.accept()

        def mouseMoveEvent(self, event):

            """ Moves the viewport to follow the cursor position. """
            if self.dragging and self.editor is not None:
                self.set_viewport_position(event.position().y())

        def set_viewport_position(self, cursor_y):
            """ Moves the viewport directly to the cursor position in the minimap. """
            minimap_scroll = self.verticalScrollBar()
            editor_scroll = self.editor.verticalScrollBar()
            
            #print("m scroll :",minimap_scroll.value())
            # Calculate the new scroll position based on cursor position
            total_lines = max(1, self.editor.blockCount())
            minimap_height = self.height()
            scale_factor = editor_scroll.maximum() / max(1, minimap_scroll.maximum())

            # Calculate target position
            new_scroll_value = int((cursor_y / minimap_height) * minimap_scroll.maximum())

            # Apply to minimap and editor
            if self.editor.verticalScrollBar().maximum()!=int(scale_factor):    
                
                minimap_scroll.setValue(new_scroll_value)
                editor_scroll.setValue(int(new_scroll_value * scale_factor))
            #print("new scrol :",new_scroll_value)
            self.viewport().update()  # Refresh the viewport

        def sync_editor_scroll(self, value):
            if self.editor is not None and self.subwindow is not None:
                if self.ignore_sync:
                    return

                editor_scroll = self.editor.verticalScrollBar()
                minimap_scroll = self.verticalScrollBar()
                    
                self.ignore_sync = True
                editor_scroll.valueChanged.disconnect(self.sync_minimap_scroll)

                scale_factor = editor_scroll.maximum() / max(1, minimap_scroll.maximum())
                if self.editor.verticalScrollBar().maximum()!=int(scale_factor):    
                    editor_scroll.setValue(int(value*scale_factor))
                editor_scroll.valueChanged.connect(self.sync_minimap_scroll)
                self.ignore_sync = False

                self.viewport().update()


        def sync_minimap_scroll(self, value):
            try:
                if self.editor is not None and self.subwindow is not None:
                    if self.ignore_sync:
                        return
            
                    editor_scroll = self.editor.verticalScrollBar()
                    
                    minimap_scroll = self.verticalScrollBar()

                    self.ignore_sync = True
                    minimap_scroll.valueChanged.disconnect(self.sync_editor_scroll)

                    scale_factor = minimap_scroll.maximum() / max(1, editor_scroll.maximum())
                    if self.editor.verticalScrollBar().maximum()!=int(scale_factor):    
                        minimap_scroll.setValue(int(value * scale_factor))
                    
                    minimap_scroll.valueChanged.connect(self.sync_editor_scroll)
                    self.ignore_sync = False

                    self.viewport().update()
            except:pass



    class LineNumberArea(QtWidgets.QWidget):
        def __init__(self, editor: QtWidgets.QPlainTextEdit):

            super().__init__(editor)
            
            self.editor = editor
            self.bg_clr="#000000"


            self.editor.viewport().installEventFilter(self)
            self.editor.blockCountChanged.connect(self.update_width)
            self.editor.updateRequest.connect(self.update_area)

            self.breakpoints = set()
            self.error_lines = set()

            self.breakpoint_icon = QtGui.QPixmap("/home/omx/Downloads/trip_origin_16dp_FFFF55_FILL0_wght400_GRAD0_opsz20.png")
            self.error_icon = QtGui.QPixmap("/home/omx/Downloads/warning_16dp_EA3323_FILL0_wght400_GRAD0_opsz20.png")
            self.set_errors({10,15})
            self.update_width(0)
            self.editor.cursorPositionChanged.connect(self.update)


        def update_width(self, _):
            digits = len(str(self.editor.blockCount()))
            width = 30 + self.fontMetrics().horizontalAdvance("9") * digits
            self.editor.setViewportMargins(width, 0, 0, 0)
            self.setFixedWidth(width)

        def update_area(self, rect, dy):
            if dy:
                self.scroll(0, dy)
            else:
                self.update(0, rect.y(), self.width(), rect.height())

            if rect.contains(self.editor.viewport().rect()):
                self.update_width(0)

        def resizeUpdate(self, event):
            cr = self.editor.contentsRect()
            self.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.width(), cr.height()))

        def eventFilter(self, obj, event):
            if event.type() == QtCore.QEvent.Type.Paint:
                self.update()
            return super().eventFilter(obj, event)

        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.fillRect(event.rect(), QtGui.QColor(self.bg_clr))

            block = self.editor.firstVisibleBlock()
            block_number = block.blockNumber()
            offset = self.editor.contentOffset()
            top = self.editor.blockBoundingGeometry(block).translated(offset).top()

            font_metrics = self.editor.fontMetrics()
            line_height = font_metrics.height()

            icon_size = 12  # You can scale this dynamically if needed
            
            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible():
                    line_num = block_number + 1
                    rect_top = int(top)

                    # Center icon vertically in the line
                    icon_y = rect_top + int((line_height - icon_size) / 2)
                    icon_x = 4

                    # Draw error or breakpoint icons
                    if line_num in self.error_lines:
                        painter.drawPixmap(icon_x, icon_y, icon_size, icon_size, self.error_icon)
                    elif line_num in self.breakpoints:
                        painter.drawPixmap(icon_x, icon_y, icon_size, icon_size, self.breakpoint_icon)

                    # Draw line number text
                    text_x = icon_x + icon_size + 4  # Leave space after icon
                    cursor_block_number = self.editor.textCursor().blockNumber() + 1

                    # Decide color based on cursor position
                    if line_num == cursor_block_number:
                        painter.setPen(QtGui.QColor("#7D8181"))  # Green color for active line
                    else:
                        painter.setPen(QtGui.QColor("#797979"))  # Normal color

                    painter.setFont(self.editor.font())
                    painter.drawText(-10, rect_top, self.width() - 4, line_height,
                        QtCore.Qt.AlignmentFlag.AlignRight, str(line_num))

                # Move to next block
                top += self.editor.blockBoundingRect(block).height()
                block = block.next()
                block_number += 1

            painter.end()

        def toggle_breakpoint(self, line: int):
            if line in self.breakpoints:
                self.breakpoints.remove(line)
            else:
                self.breakpoints.add(line)
            self.update()

        def set_errors(self, lines: set):
            self.error_lines = lines
            self.update()


        def mousePressEvent(self, event: QtGui.QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                # Calculate which line was clicked
                y = event.position().y()
                block = self.editor.firstVisibleBlock()
                top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
                bottom = top + self.editor.blockBoundingRect(block).height()
                line = block.blockNumber()

                while block.isValid() and top <= y:
                    if block.isVisible() and bottom >= y:
                        self.toggle_breakpoint(line + 1)
                        break
                    block = block.next()
                    top = bottom
                    bottom = top + self.editor.blockBoundingRect(block).height()
                    line += 1



    class TextEditor(QtWidgets.QPlainTextEdit):
    
        whenTextCursorHover=QtCore.pyqtSignal(list)
        whenMouseCursorHover=QtCore.pyqtSignal(str,int,int,QtCore.QPoint)
        whenMouseCursorLeaveHover=QtCore.pyqtSignal()
        whenGoToDefinitionRequest=QtCore.pyqtSignal(str,int,int,QtCore.QPoint)
        
        def __init__(self,parent=None):
            super().__init__(parent)
            
            self.features=Editor.Features()
            self.features.setEditor(self)
            
            self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
            #self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
            #self.setFont(QtGui.QFont("Courier New"))
            font = QtGui.QFont("Lucida Console")
            font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
            self.setFont(font)

            #font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
            self.setAcceptDrops(True)

            self.indent_rgba=[255, 255, 255,30]

            self.link_url=None
            self.last_completion=None
            self.connect_completion=lambda:...

            self.completer = QtWidgets.QCompleter(self)
            self.completer.setWidget(self)
            self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive) 
            self.completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)  
            self.completer.popup().setUniformItemSizes(True)  
            self.completer.activated.connect(self.insert_completion)

            self.proxy_model = QtCore.QSortFilterProxyModel(self)
            self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)  
            self.completer.setModel(self.proxy_model)
            self.textChanged.connect(self.update)
            self.popup=self.completer.popup()

            self.model=QtGui.QStandardItemModel(self)
            self.proxy_model.setSourceModel(self.model)
            
            self.kind={
            0:"/home/omx/key_o.png",
            3:"/home/omx/functionw_kind.png",
            6:"/home/omx/var_kind.png",
            7:"/home/omx/classw_kind.png"

            }

            self.setMouseTracking(True)
            #self.cursorPositionChanged.connect(self.onTextCursorMove)

            self.hover_timer_m = QtCore.QTimer()
            self.hover_timer_m.setInterval(100)
            self.hover_timer_m.setSingleShot(True)
            
            self.hover_timer_t = QtCore.QTimer()
            self.hover_timer_t.setInterval(100)
            self.hover_timer_t.setSingleShot(True)

            self.hover_timer_m.timeout.connect(self.handleMouseCursorHover)
            self.hover_timer_t.timeout.connect(self.handleTextCursorHover)
            
            self.last_word=""
            
            self.numpad_area = Editor.LineNumberArea(self)
            
            self.cursorPositionChanged.connect(self.highlightCurrentLine)
            self.highlightCurrentLine()
            

            

            

        def highlightCurrentLine(self):
            extra_selections = []

            if not self.isReadOnly():
                selection = QtWidgets.QTextEdit.ExtraSelection()
                line_color = QtGui.QColor("#333333")  # VS Code-like color
                selection.format.setBackground(line_color)
                selection.format.setProperty(QtGui.QTextFormat.Property.FullWidthSelection, True)
                selection.cursor = self.textCursor()
                selection.cursor.clearSelection()
                extra_selections.append(selection)

            self.setExtraSelections(extra_selections)

        
        def onTextCursorMove(self):
            
            self.hover_timer_t.start()


            
        def handleTextCursorHover(self):
            word,cursor=self.features.getWordUnderCursor()
            if not word:
                self.features.clear_highlighted_words()
                return
            """if word==self.last_word:
                return
            """
            self.last_word = word
            self.features.clear_highlighted_words()


            self.features.highlight_matching_words(word)
        
            #line = self.textCursor().blockNumber()
            #char = self.textCursor().columnNumber()


        def handleMouseCursorHover(self):

            if not hasattr(self, "mouse_pos") or self.mouse_pos is None:
                return
            
            cursor = self.cursorForPosition(self.mouse_pos)
            cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText()

            if not word:
                self.features.clear_highlight()
                self.whenMouseCursorLeaveHover.emit()
                return 
            """if word==self.last_word:
                return"""
            
            self.last_word = word
            self.features.clear_highlight()
            
            if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                start_cursor = QtGui.QTextCursor(cursor)
                start_cursor.setPosition(cursor.selectionStart())

                # Get the block (line) and column (position in block) of the word start
                line_number = start_cursor.blockNumber()
                column_number = start_cursor.positionInBlock()

                # Optional: get global screen position of the word's start (for popup)
                word_rect = self.cursorRect(start_cursor)
                global_pos = self.mapToGlobal(word_rect.bottomLeft())

                # Emit word, global_pos, line, and column
                self.whenMouseCursorHover.emit(word,line_number,column_number,global_pos)

                self.features.highlight_cursor(cursor)
                self.viewport().update()

            
            # Simulated hover content (replace with LSP hover request):
            line = cursor.blockNumber()
            char = cursor.positionInBlock()
            #QToolTip.showText(self.mapToGlobal(self.mouse_pos), hover_text)

        
        def resizeEvent(self, e):
            self.numpad_area.resizeUpdate(e)
            return super().resizeEvent(e)
        
        def mouseMoveEvent(self, event):

            self.mouse_pos = event.pos()  # Proper for PyQt6
            self.hover_timer_m.start()
            super().mouseMoveEvent(event)

        def paintEvent(self, event):
            super().paintEvent(event)
            painter = QtGui.QPainter(self.viewport())
            painter.setPen(QtGui.QColor(*self.indent_rgba))

            font_metrics = QtGui.QFontMetrics(self.font())
            char_width = font_metrics.horizontalAdvance(' ')
            block = self.firstVisibleBlock()

            visible_blocks = 0
            max_blocks = 100  # Limit to improve speed

            while block.isValid() and visible_blocks < max_blocks:
                text = block.text()
                indent_level = (len(text) - len(text.lstrip())) // 4

                if indent_level > 0:
                    rect = self.blockBoundingGeometry(block).translated(self.contentOffset())
                    for i in range(indent_level):
                        x_pos = i * char_width * 4
                        painter.drawLine(x_pos, int(rect.top()), x_pos, int(rect.bottom()))

                block = block.next()
                visible_blocks += 1

            painter.end()

        def setSuggestions(self, suggestions):
            self.model.clear()  # Clear old items

            for suggestion in suggestions:
                item = QtGui.QStandardItem()
                item.setText(suggestion[0])
                icon_path = self.kind.get(suggestion[1], self.kind[0])
                item.setIcon(QtGui.QIcon(icon_path))
                self.model.appendRow(item)

            if self.model.rowCount() > 0:
                first_index = self.model.index(0, 0)
                self.popup.setCurrentIndex(first_index)


            self.proxy_model.setSourceModel(self.model)
            """first_index=self.completer.popup().model().index(0,0)
            self.completer.popup().setCurrentIndex(first_index)
            first_index=self.completer.popup().model().index(0,0)
            self.completer.popup().setCurrentIndex(first_index)
            first_index=self.completer.popup().model().index(0,0)
            self.completer.popup().setCurrentIndex(first_index)
            first_index=self.completer.popup().model().index(0,0)
            self.completer.popup().setCurrentIndex(first_index)"""
            
        def dragEnterEvent(self,event:QtGui.QDragEnterEvent):
            
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
                
            elif event.mimeData().hasText():
                event.acceptProposedAction()
                
            
            else:
                event.ignore()

        def dragMoveEvent(self,event:QtGui.QDragEnterEvent):
            event.acceptProposedAction()

        def dropEvent(self,event:QtGui.QDropEvent):
            
            if event.mimeData().hasUrls():
                for url in event.mimeData().urls():
                    file_path=url.toLocalFile()
                    self.link_url(file_path)

                    with open(file_path,'r')as file:
                        self.setPlainText(file.read())
                        file.close()

                event.acceptProposedAction()
            
            elif event.mimeData().hasText():    
                dropped_text=event.mimeData().text()
                self.insertPlainText(dropped_text)
                event.acceptProposedAction()
        
            else:
                super().dropEvent(event)
        
        def insert_completion(self,completion):
            self.last_completion=completion
            self.connect_completion()
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.StartOfWord,cursor.MoveMode.KeepAnchor)
            cursor.insertText(completion)
            self.setTextCursor(cursor)

        def keyPressEvent(self, event):
            if self.completer.popup().isVisible():
                # If the completer popup is open, handle special keys
                if event.key() in (QtCore.Qt.Key.Key_Enter, QtCore.Qt.Key.Key_Return):
                    # Get the current item from the popup
                    current_index = self.completer.popup().currentIndex()
                    if current_index.isValid():
                        completion = current_index.data()
                        self.insert_completion(completion)
                          # Insert the selected completion
                    self.completer.popup().hide()  # Close the popup
                    return  # Consume the event to prevent default behavior
                elif event.key() == QtCore.Qt.Key.Key_Escape:
                    self.completer.popup().hide()  # Close the popup
                    return
                elif event.key() in (QtCore.Qt.Key.Key_Up, QtCore.Qt.Key.Key_Down):
                    # Allow navigation within the popup
                    return super().keyPressEvent(event)
                
            
            if event.key() in (
                QtCore.Qt.Key.Key_Up,
                QtCore.Qt.Key.Key_Down,
                QtCore.Qt.Key.Key_Left,
                QtCore.Qt.Key.Key_Right
                ):

                self.onTextCursorMove()
            else:
                
                self.features.clear_highlighted_words()
    
            if event.key()==QtCore.Qt.Key.Key_F12:
                self.features.goToDefinition()


            super().keyPressEvent(event)
    
            # Handle alphanumeric keys or other custom behavior
        def textChangedConnect(self):
            
            cursor = self.textCursor()
            #if cursor.block().text().isalnum():
            cursor.select(cursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText()
            
            #word=word.replace(' ','')
            word=word.strip()

            if word:
                
                self.completer.setCompletionPrefix(word)  # Update the completion prefix
                popup_rect = self.cursorRect()  # Get the cursor's rectangle
                #popup_rect.setY(popup_rect.y()+15)   
                popup_rect.setX(popup_rect.x()+15)
                popup_rect.setWidth(
                    self.completer.popup().sizeHintForColumn(0) +
                    self.completer.popup().verticalScrollBar().sizeHint().width()
                )
                
                self.completer.complete(popup_rect)
                
                if self.completer.model().rowCount() > 0:
                    first_index = self.completer.popup().model().index(0,0)
                    self.completer.popup().setCurrentIndex(first_index)
                
            
            else:
                self.completer.popup().hide()  # Hide the popup if no word is found

            # Pass other key events to the base class
        
            
        #def con(self,fl):print(fl)

    class TextEditPopup(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent, QtCore.Qt.WindowType.ToolTip)
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating)
            self.setWindowFlags(QtCore.Qt.WindowType.ToolTip)

            self.popup_text_edit=QtWidgets.QTextEdit()
            self.popup_text_edit.setReadOnly(True)
            self.popup_text_edit.setStyleSheet("""
                background-color: #2d2d30;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 6px;
                font-family: Consolas;
                font-size: 14px;
            """)

            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(self.popup_text_edit)
            layout.setContentsMargins(0, 0, 0, 0)

            #self.cursor_enter=False
            # Apply syntax highlighter
        def show_popup(self,text,pos):
            self.popup_text_edit.setPlainText(text)
            self.adjustSize()
            #cursor_pos = text_edit.mapToGlobal(text_edit.cursorRect().bottomRight())
            self.move(QtCore.QPoint(pos.x(),pos.y()+10))
            self.show()


        def leaveEvent(self, a0):
            self.hide()
            return super().leaveEvent(a0)
        

    class Features:

        def __init__(self):
            
            self.editor:QtWidgets.QPlainTextEdit=None
            
            self.last_cursor=None

            self.highlight_format = QtGui.QTextCharFormat()
            self.highlight_format.setBackground(QtGui.QColor("#5A5A48"))

            self.current_match_format = QtGui.QTextCharFormat()
            self.current_match_format.setBackground(QtGui.QColor("#503939"))

            self.highlighted_selections = []
            

            self._last_find_word=""
            self._find_results=[]
            self._find_index=-1
        
        def setEditor(self,editor):
            self.editor=editor

        def on_find_text_changed(self,word):
            self._last_find_word = ""  # Reset to re-find
            self._find_index = -1
            self._find_results = []
            self.highlight_matching_words(word)
        
        def on_find_enter(self):
            text = self.find_input.text()
            self.find_word_and_focus(text)


        def find_word_and_focus(self,word):
            if word != self._last_find_word:
                self._find_results = self.find_matching_words(word)
                self._find_index = -1
                self._last_find_word = word

            if not self._find_results:
                return

            self._find_index += 1
            if self._find_index >= len(self._find_results):
                self._find_index = 0

            current_cursor = self._find_results[self._find_index]
            self.editor.setTextCursor(current_cursor)
            self.editor.moveCursor(QtGui.QTextCursor.MoveOperation.NoMove) 
            self.editor.ensureCursorVisible()

            self.highlight_matching_words(word, current_cursor)




        def goToLine(self,line_number,set_cursor=False):

            line_number = max(1, line_number)
            doc = self.editor.document()
            block = doc.findBlockByNumber(line_number - 1)

            if not block.isValid():
                return

            cursor = QtGui.QTextCursor(block)
            
            if set_cursor==True:
                self.editor.setTextCursor(cursor)
                self.editor.setFocus()
            
            else:
                self.editor.setTextCursor(cursor)
            
            
            self.editor.centerCursor()


        def getWordUnderCursor(self):

            cursor = self.editor.textCursor()
            cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
            word=cursor.selectedText()
            
            if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                start_cursor = QtGui.QTextCursor(cursor)
                start_cursor.setPosition(cursor.selectionStart())

                # Get the block (line) and column (position in block) of the word start
                line_number = start_cursor.blockNumber()
                column_number = start_cursor.positionInBlock()

                # Optional: get global screen position of the word's start (for popup)
                word_rect = self.editor.cursorRect(start_cursor)
                global_pos = self.editor.mapToGlobal(word_rect.bottomLeft())

                # Emit word, global_pos, line, and column
                
                #self.whenMouseCursorHover.emit(word,line_number,column_number,global_pos)

            return word,line_number,column_number,global_pos
        
        def goToDefinition(self):
            word,line,column,pos=self.getWordUnderCursor()
            self.whenGoToDefinitionRequest.emit(word,line,column,pos)
            


        def highlight_cursor(self,cursor):
            
            self.blockSignals(True)
            fmt = QtGui.QTextCharFormat()
            fmt.setBackground(QtGui.QColor("#502929")) 
            
            cursor.setCharFormat(fmt)
            self.last_cursor = cursor

            self.blockSignals(False)

        def clear_highlight(self,cursor=None):
            if cursor==None:
                cursor=self.last_cursor
                
            self.editor.blockSignals(True)
            
            if cursor:
                fmt = QtGui.QTextCharFormat()
                fmt.setBackground(QtGui.QColor("transparent"))
                cursor.setCharFormat(fmt)
                cursor = None
            self.blockSignals(False)

        def find_matching_words(self,word):
            cursors = []
            if not word:
                return cursors

            pattern = r'\b' + re.escape(word)
            text=self.editor.toPlainText()
            for match in re.finditer(pattern, text):
                cursor = QtGui.QTextCursor(self.document())
                cursor.setPosition(match.start())
                cursor.setPosition(match.end(), QtGui.QTextCursor.MoveMode.KeepAnchor)
                cursors.append(cursor)
            return cursors
        
        def highlight_matching_words(self,word,current_cursor= None):

            self.clear_highlighted_words()
            if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                return

            cursors = self.find_matching_words(word)
            selections = []

            for cursor in cursors:
                selection = QtWidgets.QTextEdit.ExtraSelection()
                selection.cursor = cursor
                selection.format = self.highlight_format  # green
                selections.append(selection)

            if current_cursor:
                current_selection = QtWidgets.QTextEdit.ExtraSelection()
                current_selection.cursor = current_cursor
                current_selection.format = self.current_match_format  # red
                selections.append(current_selection)

            self.highlighted_selections = selections
            
            self.editor.setExtraSelections(selections)

            
        def clear_highlighted_words(self):
            self.editor.blockSignals(True)
            self.editor.setExtraSelections([])
            self.highlighted_selections.clear()
            self.editor.blockSignals(False)