import sys, json

# Import necessary components from Pyside2.
from PySide2.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap

# Read JSON data.
with open("assets/mock_asset_data.json", "r") as f:
    data = json.load(f)

# Initialize application.
app = QApplication(sys.argv)

# Create table and set properties.
table = QTableWidget()
table.setRowCount(len(data))
table.setColumnCount(6)
table.setColumnWidth(1, 64)
# Label columns.
table.setHorizontalHeaderLabels(['Asset Name', 'Image', 'Created By', 'Date Created', 'Modified By', 'Date Modified', 'Approved'])

# Define main window class.
class MainWindow(QMainWindow):

    def __init__(self, table):
        super().__init__()
        self.setWindowTitle("Asset Manager - Ryan Amos")
        
        # Search and clear search functionality.
        self.searchBox = QLineEdit()
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(lambda:self.search())
        self.clearButton = QPushButton("Clear Search")
        self.clearButton.clicked.connect(lambda:self.clear())
        
        # Create a layout for the search box and buttons.
        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchBox)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addWidget(self.clearButton)

        # Create a layout for the table.
        tableLayout = QVBoxLayout()
        tableLayout.addWidget(table)
        
        # Create a main layout to hold the search and table layouts.
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(searchLayout)
        mainLayout.addLayout(tableLayout)

        # Set the main layout as the central widget of the main window.
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
            
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        for col in range(table.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
            
        self.table = table
        self.displayData()
                      
    # Define search method.
    def search(self):
        searchText = self.searchBox.text().lower()
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and searchText in item.text().lower():
                    table.setRowHidden(row, False)
                    break
                else:
                    table.setRowHidden(row, True)
    
    # Define clear search method.
    def clear(self):
        self.searchBox.clear()
        for row in range(table.rowCount()):
            table.setRowHidden(row, False)
        
    # Display JSON data.
    def displayData(self):
        for i, item in enumerate (data):
            table.setRowHeight(i,64)
            guid = item['guid']
            image_path = f"assets/data/{guid}.jpg"
            imageToShow = QTableWidgetItem()
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(64, 64)
            else:
                print("Failed to load image:", image_path)
            
            imageToShow.setData(Qt.DecorationRole, pixmap)
                
            table.setItem(i, 0, QTableWidgetItem(item['asset_name']))
            table.setItem(i, 1, imageToShow)
            table.setItem(i, 2, QTableWidgetItem(item['created_by']))
            table.setItem(i, 3, QTableWidgetItem(item['created']))
            table.setItem(i, 4, QTableWidgetItem(item['last_edit']))
            table.setItem(i, 5, QTableWidgetItem(item['modified']))

window = MainWindow(table)
window.setFixedSize(607, 1024)
window.show()

app.exec_()