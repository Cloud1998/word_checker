import os  # 导入os模块
import sys
import json
import jieba
import jieba.posseg as pseg  # 确保导入jieba.posseg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QFileDialog, QLabel, QMessageBox  # 导入QMessageBox
from docx import Document
from docx.enum.text import WD_COLOR_INDEX

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件处理")
        self.resize(400, 200)

        layout = QVBoxLayout()

        # 加载省市区数据
        self.regions = self.load_regions_data()

        # 创建省、市、区的下拉菜单
        self.provinceComboBox = QComboBox()
        self.cityComboBox = QComboBox()
        self.districtComboBox = QComboBox()

        # 填充省份数据
        self.provinceComboBox.addItems([province['name'] for province in self.regions])
        self.provinceComboBox.currentIndexChanged.connect(self.on_province_changed)

        # 连接市的变化信号
        self.cityComboBox.currentIndexChanged.connect(self.on_city_changed)

        # 添加下拉菜单到布局
        layout.addWidget(self.provinceComboBox)
        layout.addWidget(self.cityComboBox)
        layout.addWidget(self.districtComboBox)

        # 创建一个按钮来选择文件
        self.fileButton = QPushButton("选择Word文件")
        self.fileButton.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.fileButton)

        # 用于显示选中的文件路径
        self.filePathLabel = QLabel()
        layout.addWidget(self.filePathLabel)

        # 添加一个“运行”按钮来处理Word文档
        self.runButton = QPushButton("运行")
        self.runButton.clicked.connect(self.process_word_document)
        layout.addWidget(self.runButton)

        self.setLayout(layout)

    def load_regions_data(self):
        with open('pca-code.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def on_province_changed(self, index):
        province = self.regions[index]
        self.cityComboBox.clear()
        self.cityComboBox.addItems([city['name'] for city in province.get('children', [])])
        self.on_city_changed(0)  # 更新区域数据

    def on_city_changed(self, index):
        if index >= 0:  # 检查索引，避免负值索引
            province_index = self.provinceComboBox.currentIndex()
            if province_index >= 0:
                city = self.regions[province_index]['children'][index]
                self.districtComboBox.clear()
                self.districtComboBox.addItems([district['name'] for district in city.get('children', [])])

    def openFileNameDialog(self):
        # 打开文件对话框并选择文件
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "选择Word文件", "", "Word Files (*.docx)", options=options)
        if filePath:
            self.filePathLabel.setText(filePath)

    # 检查region_name是否存在regions中，如果存在返回 True，否则返回 False
    def find_region(self, region_name):
        stack = list(self.regions)  # 使用列表作为栈
        while stack:
            region = stack.pop()  # 弹出栈顶元素
            if region["name"] == region_name:
                return True
            if "children" in region:
                stack.extend(region["children"])  # 将子区域压入栈
        return False

    def process_word_document(self):
        selected_province = self.provinceComboBox.currentText()
        selected_city = self.cityComboBox.currentText()
        selected_district = self.districtComboBox.currentText()
        
        file_path = self.filePathLabel.text()
        if not file_path:
            return

        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                words = pseg.cut(run.text)
                for word, flag in words:
                    if flag == "ns" and len(word) >= 2 and self.find_region(word):
                        # 判断地名是否与用户选择的省、市、区匹配
                        if word != selected_province and word != selected_city and word != selected_district:
                            # run.font.highlight_color = WD_COLOR_INDEX.RED
                            paragraph.add_comment('此处的地名可能存在问题')
                            

        # 生成新文件的名称
        base_name = os.path.basename(file_path)
        new_file_name = "modified_" + base_name
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        # 保存修改后的文档
        doc.save(new_file_path)

        # 弹出消息框通知用户文件已保存
        QMessageBox.information(self, "保存成功", f"文件已保存为: {new_file_name}，地址为{new_file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())