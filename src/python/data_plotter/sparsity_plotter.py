
########################################################################
#
# AUTHOR:         TYLER A. REISER  
# CREATED:        SEPTEMBER   2023  
# MODIFIED:       NOVEMBER    2024
#
# COPYRIGHT (c) 2024 Tyler A. Reiser
#
########################################################################

import os
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


class DataProcessor:
    def __init__(self, data_processor=None, data=None):
        self.data_processor = data_processor
        self.data = data if data is not None else self.load_data()

    def load_data(self):
        if self.data_processor is not None and hasattr(
            self.data_processor, "process_all_buildings"
        ):
            return self.data_processor.process_all_buildings()
        else:
            return None

    def prepare_data(self):
        if not self.data:
            return None, None

        buildings = list(self.data[next(iter(self.data))].keys())
        prepared_data = {
            network: [
                df.get("zero_elements", [0])[0] if df is not None else 0
                for building, df in self.data[network].items()
            ]
            for i, network in enumerate(self.data)
            if i < 3 and network != "Sum"
        }
        return buildings, prepared_data


class DataPlotter:
    def __init__(
        self, data_processor, output_dir="./data/output/building-plots/all-buildings"
    ):
        self.data_processor = data_processor
        self.output_dir = output_dir

    def save_plot(self, filename):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            output_file = os.path.join(self.output_dir, filename)
            plt.savefig(output_file)
        except OSError as e:
            print(f"Could not save plot due to: {e}")

    def plot_sparsity(self, buildings, prepared_data, show_plot=True):
        if buildings is None or prepared_data is None:
            print("No data to plot.")
            return

        date_range = f"August 2019 to March 2021"

        fig, ax1 = plt.subplots(figsize=(18, 15))

        sorted_data = {
            k: v
            for k, v in sorted(
                prepared_data.items(), key=lambda item: item[1], reverse=True
            )
        }

        width = 0.75
        colors = {"Eduroam": "blue", "UCBGuest": "orange", "UCBWireless": "green"}

        for network in sorted_data:
            network_data = sorted_data[network]
            if isinstance(network_data, np.ndarray) and network_data.size > 1:
                for data in network_data:
                    ax1.barh(
                        buildings,
                        data,
                        width,
                        label=network,
                        color=colors.get(network, "black"),
                    )
            else:
                ax1.barh(
                    buildings,
                    network_data,
                    width,
                    label=network,
                    color=colors.get(network),
                )

        ax1.set_ylabel("Buildings")
        ax1.set_xlabel("Number of Zero Elements")

        ax1.set_title(
            f"Number of Zero Elements for Each Network for Every Building\nDate range: {date_range}"
        )
        ax1.legend()

        self.save_plot("sparsity_3networks-AllData.png")

        if show_plot:
            plt.show()

        plt.close(fig)

    def create_aggregate_bar_chart(self, fig, ax, width, colors, buildings, x, title):
        zero_elements_sum = []
        for building in buildings:
            if "Sum" in data and building in data["Sum"]:
                zero_elements_sum.append(data["Sum"][building]["zero_elements"])
            else:
                zero_elements_sum.append(0)

        x = np.ravel(x)
        zero_elements_sum = np.ravel(zero_elements_sum)
        color = [colors.get(building, "red") for building in buildings]
        ax.barh(x, zero_elements_sum, width, color=color)
        ax.set_ylabel("Building", fontsize=12)
        ax.set_xlabel("Number of Zero Elements", fontsize=12)

        start_datetime = "August 2019 "
        end_datetime = "March 2021"
        date_range = f"{start_datetime} to {end_datetime}"

        ax.set_title(f"{title}\nDate range: {date_range}", fontsize=14)
        ax.set_yticks(np.linspace(0, len(buildings) - 1, len(buildings)))
        ax.set_yticklabels(buildings, fontsize=10)
        ax.tick_params(axis="y", rotation=0, labelsize=10)
        ax.grid(axis="x", linestyle="--")

        for bar in ax.containers[0]:
            ax.text(
                bar.get_width() + 0.05 * bar.get_width(),
                bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.0f}",
                ha="left",
                va="center",
            )
        fig.tight_layout()

    def plot_sparsity_bar_chart(
        self,
        width=0.75,
        colors={"Sum": "red"},
        show_plot=True,
        output_dir="./data/output/building-plots/all-buildings",
    ):
        if data is not None:
            fig, ax = plt.subplots(figsize=(18, 15))
            if "Sum" in data:
                buildings = list(data["Sum"].keys())
            else:
                buildings = []

            x = np.arange(len(buildings))
            date_range = "default_date_range"
            output_dir = os.path.join(output_dir, date_range)

            self.create_aggregate_bar_chart(
                fig,
                ax,
                width,
                colors,
                buildings,
                x,
                "Number of Zero Elements for Each Building (Network Aggregate)",
            )

            if show_plot:
                plt.show()
            self.save_plot(os.path.join(output_dir, "sparsity_bar_chart.png"))
