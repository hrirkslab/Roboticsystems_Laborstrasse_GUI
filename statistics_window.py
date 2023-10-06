import pandas as pd
from PyQt6.QtWidgets import (QVBoxLayout, QWidget, QComboBox, QGroupBox,
                             QStackedWidget, QHBoxLayout, QPushButton,
                             QGraphicsView, QGraphicsScene, QGraphicsEllipseItem)
import pyqtgraph as pg
import numpy as np


class StatisticsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main Layout for the Statistics Widget
        main_layout = QVBoxLayout(self)
        
        # Group Box to hold the components
        group_box = QGroupBox("Experiment Statistics")
        layout = QVBoxLayout(group_box)
        
        # ComboBox for choosing experiments
        self.experiment_combobox = QComboBox()
        
        # ComboBox for choosing graph type
        self.graph_type_combobox = QComboBox()
        self.graph_type_combobox.addItems(['Bar Graph', 'Pie Chart', 'Line Graph'])
        
        # Layout for ComboBoxes
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.experiment_combobox)
        combo_layout.addWidget(self.graph_type_combobox)
        
        layout.addLayout(combo_layout)
        
        # Stacked Widget to hold different graphs
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Button to create the graph
        self.create_graph_button = QPushButton('Create Graph')
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.create_graph_button)
        layout.addLayout(button_layout)
        
        main_layout.addWidget(group_box)
        
        # Set Style and Margins
        self.setStyleSheet("background-color: #f0f0f0;")
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Read the CSV file
        file_path = 'logs/dummy_log_detail.csv'
        self.log_df = pd.read_csv(file_path)
        
        # Populate the ComboBox for experiments
        self.experiment_combobox.addItem("All Experiments")
        self.experiment_combobox.addItems(map(str, self.log_df['experiment_id'].unique()))
        
        # Connect the Create Graph button to the update_graph method
        self.create_graph_button.clicked.connect(self.update_graph)
        
    def update_graph(self):
        experiment_filter = self.experiment_combobox.currentText()
        if experiment_filter == "All Experiments":
            filtered_df = self.log_df
        else:
            filtered_df = self.log_df[self.log_df['experiment_id'] == int(experiment_filter)]
        
        graph_type = self.graph_type_combobox.currentText()
        
        # Clear existing widgets from the StackedWidget
        while self.stacked_widget.count():
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
        
        tube_columns = [f'tube{i}' for i in range(1, 33)]
        state_counts = filtered_df[tube_columns].apply(lambda x: x.value_counts(), axis=0).fillna(0).T.sum()
        
        if graph_type == 'Bar Graph':
            plot_widget = pg.PlotWidget()
            x = np.arange(len(state_counts.index))
            for i, state in enumerate(state_counts.index):
                plot_widget.addItem(pg.BarGraphItem(x=[i], height=[state_counts[state]], width=0.6, brush=pg.mkBrush(state)))
            plot_widget.getAxis('bottom').setTicks([list(zip(x, state_counts.index))])
            self.stacked_widget.addWidget(plot_widget)
            
        elif graph_type == 'Pie Chart':
            pie_widget = pg.GraphicsLayoutWidget()
            
            total = sum(state_counts)
            start_angle = 0
            for state in state_counts.index:
                span_angle = (state_counts[state] / total) * 360
                pie_slice = QGraphicsEllipseItem(-100, -100, 200, 200)
                pie_slice.setParentItem(pie_widget.graphicsItem())
                pie_slice.setStartAngle(start_angle * 16)
                pie_slice.setSpanAngle(span_angle * 16)
                pie_slice.setBrush(pg.mkBrush(state))
                start_angle += span_angle
            
            self.stacked_widget.addWidget(pie_widget)
            
        elif graph_type == 'Line Graph':
            plot_widget = pg.PlotWidget()
            x = np.arange(len(state_counts.index))
            plot_widget.plot(x, state_counts.values)
            plot_widget.getAxis('bottom').setTicks([list(zip(x, state_counts.index))])
            self.stacked_widget.addWidget(plot_widget)
