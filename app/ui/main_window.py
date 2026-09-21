import sys
from pathlib import Path
import cv2

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QStackedWidget, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox,
    QProgressBar, QSizePolicy, QScrollArea
)

from .theme import STYLE
from ..core.pipeline import SteelPipeline
from ..scheduling.scheduler import CraneScheduler


ROOT = Path(__file__).resolve().parents[2]
ASSET = ROOT / "assets"


class MetricCard(QFrame):
    def __init__(self, name, value):
        super().__init__()
        self.setStyleSheet("QFrame{background:#0A1B31;border:1px solid #193A5B;border-radius:8px;}")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 12, 16, 12)
        n = QLabel(name); n.setObjectName("MetricName")
        v = QLabel(value); v.setObjectName("MetricValue")
        lay.addWidget(n); lay.addWidget(v)


class MainWindow(QMainWindow):
    NAV = [
        ("仓储总览", 0),
        ("钢卷AI识别", 1),
        ("信息确认", 2),
        ("创建任务", 3),
        ("智能调度", 4),
        ("执行状态", 5),
        ("异常处理", 6),
        ("任务完成", 7),
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("钢智灵枢——面向钢铁仓储的多模态AI智能决策平台")
        self.resize(1360, 850)
        self.setMinimumSize(1180, 760)
        self.pipeline = SteelPipeline()
        self.scheduler = CraneScheduler(3)
        self.current_image = None
        self.current_result = None
        self.progress_value = 60
        self.nav_buttons = []
        self.pages = QStackedWidget()
        self.build_ui()

    def build_ui(self):
        root = QWidget(); self.setCentralWidget(root)
        root_lay = QVBoxLayout(root); root_lay.setContentsMargins(0, 0, 0, 0); root_lay.setSpacing(0)

        top = QFrame(); top.setObjectName("TopBar"); top.setFixedHeight(66)
        top_lay = QHBoxLayout(top); top_lay.setContentsMargins(22, 0, 22, 0)
        brand = QLabel("钢智灵枢"); brand.setObjectName("Brand")
        sub = QLabel("面向钢铁仓储的多模态AI智能决策平台"); sub.setObjectName("Subtitle")
        top_lay.addWidget(brand); top_lay.addSpacing(14); top_lay.addWidget(sub); top_lay.addStretch()
        status = QLabel("● 系统运行正常"); status.setObjectName("StatusGood")
        top_lay.addWidget(status)
        root_lay.addWidget(top)

        body = QHBoxLayout(); body.setContentsMargins(0, 0, 0, 0); body.setSpacing(0)
        sidebar = self.build_sidebar(); body.addWidget(sidebar)
        content = QFrame(); content.setObjectName("Content")
        content_lay = QVBoxLayout(content); content_lay.setContentsMargins(24, 20, 24, 18)
        content_lay.addWidget(self.pages)
        body.addWidget(content, 1)
        root_lay.addLayout(body, 1)

        self.build_pages()
        self.show_page(0)

    def build_sidebar(self):
        side = QFrame(); side.setObjectName("Sidebar"); side.setFixedWidth(190)
        lay = QVBoxLayout(side); lay.setContentsMargins(12, 20, 12, 16); lay.setSpacing(5)
        title = QLabel("钢智灵枢")
        title.setStyleSheet("font-size:17px;font-weight:700;color:#55D7FF;padding:8px 10px;")
        lay.addWidget(title)
        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setStyleSheet("color:#193A5B;")
        lay.addWidget(line)
        for text, idx in self.NAV:
            b = QPushButton(text); b.setObjectName("NavButton"); b.setCheckable(True)
            b.clicked.connect(lambda checked=False, i=idx: self.show_page(i))
            self.nav_buttons.append(b); lay.addWidget(b)
        lay.addStretch()
        foot = QLabel("AI感知 · 状态分析\n智能决策 · 执行反馈")
        foot.setStyleSheet("color:#54718C;font-size:11px;padding:10px;")
        lay.addWidget(foot)
        return side

    def page_header(self, step, title, desc):
        w = QWidget(); lay = QVBoxLayout(w); lay.setContentsMargins(0, 0, 0, 8); lay.setSpacing(6)
        row = QHBoxLayout(); row.setSpacing(10)
        badge = QLabel(str(step)); badge.setObjectName("StepBadge"); badge.setAlignment(Qt.AlignCenter); badge.setFixedSize(28, 28)
        row.addWidget(badge)
        t = QLabel(title); t.setObjectName("PageTitle"); row.addWidget(t); row.addStretch()
        lay.addLayout(row)
        d = QLabel(desc); d.setObjectName("PageDesc"); lay.addWidget(d)
        return w

    def panel(self):
        p = QFrame(); p.setStyleSheet("QFrame{background:#0A1B31;border:1px solid #193A5B;border-radius:8px;}")
        return p

    def build_pages(self):
        self.pages.addWidget(self.page_overview())
        self.pages.addWidget(self.page_recognition())
        self.pages.addWidget(self.page_confirm())
        self.pages.addWidget(self.page_create_task())
        self.pages.addWidget(self.page_schedule())
        self.pages.addWidget(self.page_execution())
        self.pages.addWidget(self.page_exception())
        self.pages.addWidget(self.page_complete())

    def page_overview(self):
        page = QWidget(); lay = QVBoxLayout(page)
        lay.addWidget(self.page_header(2, "查看仓储状态", "系统展示当前钢卷数量、库位状态、任务数量及天车运行状态。"))
        metrics = QGridLayout(); metrics.setSpacing(12)
        metrics.addWidget(MetricCard("钢卷总数", "1258"), 0, 0)
        metrics.addWidget(MetricCard("库位占用率", "76%"), 0, 1)
        metrics.addWidget(MetricCard("待处理任务", "18"), 0, 2)
        metrics.addWidget(MetricCard("天车状态", "正常"), 0, 3)
        lay.addLayout(metrics)
        twin = self.panel(); tl = QVBoxLayout(twin); tl.setContentsMargins(12, 12, 12, 12)
        cap = QLabel("钢卷仓储数字孪生 / 运行态势"); cap.setStyleSheet("color:#7FA4C2;font-weight:600;")
        tl.addWidget(cap)
        img = QLabel(); img.setAlignment(Qt.AlignCenter); img.setMinimumHeight(360)
        self.set_image_label(img, ASSET / "digital_twin.png", 1050, 390)
        tl.addWidget(img)
        st = QLabel("天车状态    "); st.setObjectName("StatusGood"); st.setText("● 正常   3台天车在线")
        tl.addWidget(st, alignment=Qt.AlignRight)
        lay.addWidget(twin, 1)
        return page

    def page_recognition(self):
        page = QWidget(); lay = QVBoxLayout(page)
        lay.addWidget(self.page_header(3, "钢卷AI识别", "系统自动识别钢卷、标签及二维码，并输出识别置信度与当前位置。"))
        row = QHBoxLayout(); row.setSpacing(14)
        left = self.panel(); ll = QVBoxLayout(left); ll.setContentsMargins(12, 12, 12, 12)
        self.rec_image = QLabel(); self.rec_image.setAlignment(Qt.AlignCenter); self.rec_image.setMinimumSize(700, 470)
        self.set_image_label(self.rec_image, ASSET / "steel_ai_demo.png", 760, 470)
        ll.addWidget(self.rec_image, 1)
        choose = QPushButton("选择钢卷图像"); choose.setObjectName("Secondary"); choose.clicked.connect(self.choose_image)
        ll.addWidget(choose)
        right = self.panel(); rl = QVBoxLayout(right); rl.setContentsMargins(18, 18, 18, 18)
        title = QLabel("AI识别结果"); title.setStyleSheet("color:#55D7FF;font-size:17px;font-weight:700;")
        rl.addWidget(title)
        self.rec_fields = {}
        for name, value in [("钢卷编号", "G2025001"), ("钢卷类型", "冷轧卷"), ("标签", "T-001"), ("二维码", "识别成功"), ("置信度", "0.92"), ("当前库位", "A区-03-02")]:
            box = QFrame(); box.setStyleSheet("QFrame{background:#0D243D;border:1px solid #193A5B;border-radius:5px;}")
            bl = QHBoxLayout(box); bl.setContentsMargins(10, 8, 10, 8)
            a = QLabel(name); a.setStyleSheet("color:#7E9AB3;"); b = QLabel(value); b.setStyleSheet("color:#55D7FF;font-weight:600;"); bl.addWidget(a); bl.addStretch(); bl.addWidget(b)
            rl.addWidget(box); self.rec_fields[name] = b
        rl.addStretch()
        run = QPushButton("执行AI识别"); run.setObjectName("Primary"); run.clicked.connect(self.recognize)
        rl.addWidget(run)
        row.addWidget(left, 3); row.addWidget(right, 1)
        lay.addLayout(row, 1)
        return page

    def form_field(self, name, widget):
        row = QHBoxLayout(); label = QLabel(name); label.setFixedWidth(100); label.setStyleSheet("color:#7894AE;")
        row.addWidget(label); row.addWidget(widget, 1); return row

    def page_confirm(self):
        page = QWidget(); lay = QVBoxLayout(page)
        lay.addWidget(self.page_header(4, "信息确认", "用户确认AI识别结果后进入入库/出库任务创建。"))
        panel = self.panel(); grid = QGridLayout(panel); grid.setContentsMargins(22, 22, 22, 22); grid.setHorizontalSpacing(18); grid.setVerticalSpacing(12)
        self.confirm = {}
        fields = [("钢卷编号", "G2025001"), ("规格", "Φ1200×1250"), ("材质", "Q235"), ("当前库位", "A区-03-02"), ("目标库位", "B区-05-03"), ("状态", "待入库")]
        for r,(n,v) in enumerate(fields):
            grid.addWidget(QLabel(n), r, 0); e = QLineEdit(v); grid.addWidget(e, r, 1); self.confirm[n]=e
        info = QLabel("AI识别置信度：92%   ·   二维码：识别成功")
        info.setStyleSheet("color:#55E6A5;padding:8px;"); grid.addWidget(info, 0, 2, 1, 2)
        image = QLabel(); image.setAlignment(Qt.AlignCenter); self.set_image_label(image, ASSET / "steel_ai_demo.png", 360, 250); grid.addWidget(image, 1, 2, 5, 2)
        btns = QHBoxLayout(); ok = QPushButton("确认"); ok.setObjectName("Primary"); ok.clicked.connect(lambda: self.show_page(3)); edit = QPushButton("修改"); edit.setObjectName("Secondary"); btns.addWidget(ok); btns.addWidget(edit)
        grid.addLayout(btns, 6, 0, 1, 2)
        lay.addWidget(panel, 1); return page

    def page_create_task(self):
        page = QWidget(); lay = QVBoxLayout(page)
        lay.addWidget(self.page_header(5, "创建任务", "根据业务需求创建入库或出库任务，系统自动关联钢卷、库位和优先级。"))
        panel = self.panel(); v = QVBoxLayout(panel); v.setContentsMargins(26, 24, 26, 24)
        self.task_type = QComboBox(); self.task_type.addItems(["入库任务", "出库任务"])
        self.task_coil = QLineEdit("G2025001")
        self.task_target = QLineEdit("B区-05-03")
        self.task_priority = QComboBox(); self.task_priority.addItems(["普通", "高", "紧急"]); self.task_priority.setCurrentText("高")
        v.addLayout(self.form_field("任务类型", self.task_type)); v.addLayout(self.form_field("钢卷编号", self.task_coil)); v.addLayout(self.form_field("目标库位", self.task_target)); v.addLayout(self.form_field("优先级", self.task_priority))
        v.addStretch()
        b = QPushButton("提交任务"); b.setObjectName("Primary"); b.clicked.connect(self.create_task); v.addWidget(b, alignment=Qt.AlignRight)
        lay.addWidget(panel, 1); return page

    def page_schedule(self):
        page = QWidget(); lay = QVBoxLayout(page)
        lay.addWidget(self.page_header(6, "智能调度", "系统根据任务优先级、天车负载及路径状态完成任务分配和冲突检测。"))
        panel = self.panel(); v = QVBoxLayout(panel); v.setContentsMargins(14, 14, 14, 14)
        self.schedule_table = QTableWidget(3, 4); self.schedule_table.setHorizontalHeaderLabels(["天车", "任务", "目标库位", "状态"]); self.schedule_table.horizontalHeader().setStretchLastSection(True)
        demo = [("天车1", "G2025001", "B区-05-03", "运行中"), ("天车2", "G2025002", "C区-04-02", "待命"), ("天车3", "G2025003", "A区-06-01", "已完成")]
        self.fill_schedule(demo)
        v.addWidget(self.schedule_table)
        row = QHBoxLayout(); row.addStretch(); run = QPushButton("执行智能调度"); run.setObjectName("Primary"); run.clicked.connect(self.schedule); row.addWidget(run); v.addLayout(row)
        lay.addWidget(panel, 1); return page

    def page_execution(self):
        page = QWidget(); lay = QVBoxLayout(page)
        lay.addWidget(self.page_header(7, "查看执行状态", "实时查看任务进度、天车运行状态及预计剩余时间。"))
        panel = self.panel(); v = QVBoxLayout(panel); v.setContentsMargins(18,18,18,18)
        rows = [("任务进度", "G2025001 进行中", "运行中"), ("天车状态", "天车1 运行中", "正常"), ("天车状态", "天车2 运行中", "正常"), ("天车状态", "天车3 空闲", "待命")]
        for n, val, state in rows:
            box = QFrame(); box.setStyleSheet("QFrame{background:#0D243D;border:1px solid #193A5B;border-radius:5px;}")
            h=QHBoxLayout(box); h.setContentsMargins(12,8,12,8); h.addWidget(QLabel(n)); x=QLabel(val); x.setStyleSheet("color:#CBE4F6;"); h.addWidget(x); h.addStretch(); z=QLabel("● "+state); z.setObjectName("StatusGood" if state in ["正常","运行中"] else "StatusWarn"); h.addWidget(z); v.addWidget(box)
        self.progress = QProgressBar(); self.progress.setValue(self.progress_value); v.addWidget(self.progress)
        bottom=QHBoxLayout(); bottom.addWidget(QLabel("任务进度 60%")); bottom.addStretch(); bottom.addWidget(QLabel("预计剩余 2 分钟")); v.addLayout(bottom)
        lay.addWidget(panel, 1); return page

    def page_exception(self):
        page = QWidget(); lay = QVBoxLayout(page)
        lay.addWidget(self.page_header(8, "异常处理", "系统检测识别置信度不足、天车路径冲突或库位异常，并提供人工确认入口。"))
        panel=self.panel(); v=QVBoxLayout(panel); v.setContentsMargins(18,18,18,18)
        items=[("⚠", "识别置信度过低：钢卷 G2025005", "StatusWarn"), ("⚠", "天车2 路径冲突，需要重新规划", "StatusWarn"), ("⚠", "库位状态异常：B区-05-02", "StatusBad")]
        for icon,text,sty in items:
            box=QFrame(); box.setStyleSheet("QFrame{background:#1B1720;border:1px solid #4A2C34;border-radius:6px;}"); h=QHBoxLayout(box); h.setContentsMargins(14,10,14,10); a=QLabel(icon); a.setStyleSheet("color:#FFB34C;font-size:18px;"); b=QLabel(text); b.setStyleSheet("color:#E9D8DD;"); h.addWidget(a); h.addWidget(b); h.addStretch(); v.addWidget(box)
        v.addStretch(); btn=QPushButton("查看详情"); btn.setObjectName("Secondary"); v.addWidget(btn,alignment=Qt.AlignRight)
        lay.addWidget(panel,1); return page

    def page_complete(self):
        page=QWidget(); lay=QVBoxLayout(page)
        lay.addWidget(self.page_header(9,"任务完成·状态更新","任务执行完成后，系统自动更新钢卷库位及仓储状态，形成完整闭环。"))
        panel=self.panel(); v=QVBoxLayout(panel); v.setContentsMargins(24,24,24,24)
        done=QLabel("✓"); done.setAlignment(Qt.AlignCenter); done.setStyleSheet("background:#123D34;color:#55E6A5;border-radius:40px;font-size:48px;font-weight:700;"); done.setFixedSize(84,84); v.addWidget(done,alignment=Qt.AlignCenter)
        title=QLabel("任务已完成"); title.setAlignment(Qt.AlignCenter); title.setStyleSheet("font-size:20px;color:#55E6A5;font-weight:700;"); v.addWidget(title)
        sub=QLabel("钢卷 G2025001 已入库"); sub.setAlignment(Qt.AlignCenter); sub.setStyleSheet("color:#A8C6DF;"); v.addWidget(sub)
        grid=QGridLayout();
        for c,(n,val) in enumerate([("库位状态","B区-05-03 已占用"),("任务状态","已完成"),("天车状态","运行中")]):
            box=QFrame(); box.setStyleSheet("QFrame{background:#0D243D;border:1px solid #193A5B;border-radius:6px;}"); q=QVBoxLayout(box); q.addWidget(QLabel(n)); x=QLabel(val); x.setStyleSheet("color:#55D7FF;font-weight:700;"); q.addWidget(x); grid.addWidget(box,0,c)
        v.addLayout(grid); v.addStretch(); lay.addWidget(panel,1); return page

    def set_image_label(self, label, path, w, h):
        if Path(path).exists():
            pix=QPixmap(str(path)); label.setPixmap(pix.scaled(w,h,Qt.KeepAspectRatio,Qt.SmoothTransformation))
        else:
            label.setText("钢智灵枢 AI视觉画面")

    def choose_image(self):
        p,_=QFileDialog.getOpenFileName(self,"选择钢卷图像","","Images (*.png *.jpg *.jpeg *.bmp)")
        if p: self.run_recognition(p)

    def recognize(self):
        self.choose_image()

    def run_recognition(self, path):
        frame=cv2.imread(path)
        if frame is None:
            QMessageBox.warning(self,"错误","无法读取图像")
            return
        vis,r=self.pipeline.process(frame,{"alpha":0,"beta":0,"zoom":1})
        self.current_image=vis; self.current_result=r
        rgb=cv2.cvtColor(vis,cv2.COLOR_BGR2RGB); h,w,c=rgb.shape
        q=QImage(rgb.data,w,h,c*w,QImage.Format_RGB888).copy()
        self.rec_image.setPixmap(QPixmap.fromImage(q).scaled(self.rec_image.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        dets=r.get("detections",[])
        if dets:
            d=dets[0]
            self.rec_fields["置信度"].setText(f"{float(d.get('confidence',0)):.2f}")
            self.rec_fields["当前库位"].setText(str(d.get("warehouse_position","A区-03-02")))
            self.rec_fields["二维码"].setText("识别成功" if d.get("qr_text") else "未识别")
        self.show_page(1)

    def create_task(self):
        self.confirm["钢卷编号"].setText(self.task_coil.text())
        self.confirm["目标库位"].setText(self.task_target.text())
        self.show_page(4)

    def fill_schedule(self, rows):
        self.schedule_table.setRowCount(0)
        for r,row in enumerate(rows):
            self.schedule_table.insertRow(r)
            for c,val in enumerate(row):
                item=QTableWidgetItem(str(val)); self.schedule_table.setItem(r,c,item)
                if c==3:
                    item.setTextAlignment(Qt.AlignCenter)

    def schedule(self):
        priority={"普通":1,"高":2,"紧急":3}.get(self.task_priority.currentText(),2) if hasattr(self,'task_priority') else 2
        tasks=[{"task_id":"T001","coil_id":self.task_coil.text() if hasattr(self,'task_coil') else "G2025001","target":self.task_target.text() if hasattr(self,'task_target') else "B区-05-03","priority":priority,"duration":5}]
        rows=self.scheduler.schedule(tasks,["天车1","天车2","天车3"])
        demo=[]
        for x in rows:
            demo.append((x["crane"],x["coil_id"],x["target"],x["status"]))
        demo += [("天车2","G2025002","C区-04-02","待命"),("天车3","G2025003","A区-06-01","已完成")]
        self.fill_schedule(demo[:3])
        self.show_page(4)

    def show_page(self, index):
        self.pages.setCurrentIndex(index)
        for i,b in enumerate(self.nav_buttons): b.setChecked(i==index)


def run_app():
    app=QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    w=MainWindow(); w.show()
    sys.exit(app.exec_())
