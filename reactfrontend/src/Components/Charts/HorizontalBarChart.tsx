import React, {useLayoutEffect, useState} from "react";
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Dark from "@amcharts/amcharts5/themes/Dark";

export default function HorizontalBarChart(props: any){
    const [data, setData] = useState(null);
    useLayoutEffect(()=> {
        let root = am5.Root.new(props.chartID);
        root.setThemes([am5themes_Dark.new(root)])
        let chart = root.container.children.push(
            am5xy.XYChart.new(root, {
                panY: false,
                layout: root.verticalLayout
            })
        );

        // Create Y-axis
        let yAxis = chart.yAxes.push(am5xy.CategoryAxis.new(root, {
            categoryField: "category",
            renderer: am5xy.AxisRendererY.new(root, {
                inversed: true,
            })
        }));
        yAxis.get("renderer").labels.template.setAll({
            fill:root.interfaceColors.get("text")
        });

        // Create X-Axis
        let xAxis = chart.xAxes.push(
            am5xy.ValueAxis.new(root, {
                renderer: am5xy.AxisRendererX.new(root, {}),
            })
        );
        yAxis.data.setAll(props.chartData);
        xAxis.get("renderer").labels.template.setAll({
            fill:root.interfaceColors.get("text")
        });

        // Create series
        let series1 = chart.series.push(
            am5xy.ColumnSeries.new(root, {
                name: "Series1",
                xAxis: xAxis,
                yAxis: yAxis,
                valueXField: "value1",
                categoryYField: "category"
            })
        );
        series1.data.setAll(props.chartData);

        let series2 = chart.series.push(
            am5xy.ColumnSeries.new(root, {
                name: "Series2",
                xAxis: xAxis,
                yAxis: yAxis,
                valueXField: "value2",
                categoryYField: "category"
            })
        );
        series2.data.setAll(props.chartData);

        // Add legend
        let legend = chart.children.push(am5.Legend.new(root, {}));
        legend.data.setAll(chart.series.values);
        root.interfaceColors.set("grid",am5.color(0xFFFFFF))

        // Add cursor
        chart.set("cursor", am5xy.XYCursor.new(root, {}));
        return () => {root.dispose();};
    }, [props.chartID])
    return (<div className={props.class} id={props.chartID}></div>);
}