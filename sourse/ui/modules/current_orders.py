from sourse.ui.modules.base_qdockwidget_module import BaseUIModule
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from sourse.exchange_handlers import AbstractExchangeHandler
import datetime
import dataclasses
import typing


class CurrentOrdersModule(BaseUIModule):
    def _create_widgets(self):
        self.layout = QtWidgets.QHBoxLayout(self.base_widget)
        self.parent_widget.setWindowTitle("Orders")
        self.base_widget.setLayout(self.layout)

        self._order_dict = {}
        self._historical_order_dict = {}

        self.horizontalHeaderLabelsList = [
            "Order id",
            "Client order id",
            "Status",
            "Price",
            "Average price",
            "Fee",
            "Fee asset",
            "Volume",
            "Volume realized",
            "Time",
        ]

        self.table = QtWidgets.QTableWidget(
            len(self._order_dict), len(self.horizontalHeaderLabelsList)
        )
        self.table_historical = QtWidgets.QTableWidget(
            len(self._order_dict), len(self.horizontalHeaderLabelsList)
        )

        self.table.setSortingEnabled(True)
        self.table_historical.setSortingEnabled(True)
        self.table.setHorizontalHeaderLabels(self.horizontalHeaderLabelsList)
        self.table_historical.setHorizontalHeaderLabels(self.horizontalHeaderLabelsList)
        self.table.verticalHeader().hide()
        self.table_historical.verticalHeader().hide()

        header = self.table.horizontalHeader()
        header_historical = self.table_historical.horizontalHeader()
        for i in range(len(self.horizontalHeaderLabelsList)):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            header_historical.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.tabwidget = QtWidgets.QTabWidget()
        self.tabwidget.addTab(self.table, "Current orders")
        self.tabwidget.addTab(self.table_historical, "Historical orders")

        self.layout.addWidget(self.tabwidget)

    def add_order(self, order: AbstractExchangeHandler.OrderUpdate) -> str:
        order_id = order.client_orderID

        if order_id in self._order_dict.keys():
            return self._edit_order(order)
        else:
            self.table.setSortingEnabled(False)
            current_sorted_index = self.table.horizontalHeader().sortIndicatorSection()
            current_sorted_type = self.table.horizontalHeader().sortIndicatorOrder()

            self._order_dict[order_id] = (len(self._order_dict), order)

            self.table.setRowCount(len(self._order_dict))

            for i, value in enumerate(dataclasses.asdict(order).values()):
                self.table.setItem(
                    len(self._order_dict) - 1, i, self.createItem(str(value))
                )

            self.table.setSortingEnabled(True)

            return order_id

    def _edit_order(self, order: AbstractExchangeHandler.OrderUpdate) -> str:
        self.table.setSortingEnabled(False)

        order_id = order.client_orderID
        order_index = self._order_dict[order_id][0]

        for i, (key, value) in enumerate(dataclasses.asdict(order).items()):
            if key == "message":
                continue
            self.table.item(order_index, i).setText(str(value))

        self.table.setSortingEnabled(True)

        return order_id

    def remove_order(self, order_id: int) -> None:
        self.table.setSortingEnabled(False)

        del self._order_dict[order_id]
        self.table.removeRow(list(self._order_dict.keys()).index(order_id))

        self.table.setSortingEnabled(True)

    def remove_all_orders(self) -> None:
        self.table.setSortingEnabled(False)

        self._order_dict = {}
        self.table.setRowCount(0)

        self.table.setSortingEnabled(True)

    def _transfer_table(self) -> None:
        pass

    @staticmethod
    def createItem(text: str) -> QtWidgets.QTableWidgetItem:
        tableWidgetItem = QtWidgets.QTableWidgetItem(text)
        tableWidgetItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        return tableWidgetItem
