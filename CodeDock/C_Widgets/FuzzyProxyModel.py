from rapidfuzz import fuzz
from PyQt6 import QtWidgets,QtCore,QtGui
from rapidfuzz import fuzz
MATCH_ROLE = QtCore.Qt.ItemDataRole.UserRole + 1

class HighlightDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Copy option so we can use its rects
        opt = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        # Draw the item (background, icon, etc.)
        widget = opt.widget
        style = widget.style() if widget else QtWidgets.QApplication.style()
        style.drawControl(QtWidgets.QStyle.ControlElement.CE_ItemViewItem, opt, painter, widget)

        # Extract text and highlight pattern
        text = index.data(QtCore.Qt.ItemDataRole.DisplayRole) or ""
        pattern = index.data(MATCH_ROLE) or ""

        # Get text rectangle (this avoids overlapping the icon)
        text_rect = style.subElementRect(QtWidgets.QStyle.SubElement.SE_ItemViewItemText, opt, widget)

        # Prepare painter
        painter.save()
        painter.setFont(opt.font)
        fm = painter.fontMetrics()
        x = text_rect.x() +3
        y = text_rect.y() + fm.ascent() + (text_rect.height() - fm.height()) // 2

        # subsequence highlight
        pat = iter(pattern.lower())
        try:
            current = next(pat)
        except StopIteration:
            current = None

        for ch in text:
            char_width = fm.horizontalAdvance(ch)
            if current is not None and ch.lower() == current:
                painter.setPen(QtGui.QColor("red"))
                painter.drawText(x, y, ch)
                try:
                    current = next(pat)
                except StopIteration:
                    current = None
            else:
                painter.setPen(opt.palette.text().color())
                painter.drawText(x, y, ch)
            x += char_width

        painter.restore()



class FuzzyProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pattern = ""

    def setFilterFixedString(self, pattern: str):
        self.pattern = pattern
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if not self.pattern:
            return True

        index = self.sourceModel().index(source_row, 0, source_parent)
        text = self.sourceModel().data(index, QtCore.Qt.ItemDataRole.DisplayRole)

        if not text:
            return False

        # simple fuzzy match
        score = fuzz.partial_ratio(self.pattern.lower(), text.lower())
        return score > 50

    def lessThan(self, left, right):
        if not self.pattern:
            return super().lessThan(left, right)

        ltxt = self.sourceModel().data(left).lower()
        rtxt = self.sourceModel().data(right).lower()
        lscore = fuzz.ratio(self.pattern.lower(), ltxt)
        rscore = fuzz.ratio(self.pattern.lower(), rtxt)
        return lscore > rscore

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role == MATCH_ROLE:
            return self.pattern
        return super().data(index, role)